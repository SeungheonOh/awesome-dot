#!/usr/bin/env python3
"""Validate the fictional content and optionally its exported PPTX package.

Standard library only. This does not author or render slides and does not
establish behavior in PowerPoint, Google Slides or assistive technology.
"""
import argparse
import copy
import hashlib
import io
import json
import re
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
    's': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalized(text):
    return ' '.join(text.split())


def element_text(root):
    return normalized(' '.join(n.text or '' for n in root.findall('.//a:t', NS)))


def check_content(spec):
    packet = (HERE / 'source-packet.md').read_text(encoding='utf-8')
    script = (HERE / 'slide-script.md').read_text(encoding='utf-8')
    require(spec['fictional'] is True, 'Fictional disclosure missing')
    identity = re.search(r'Packet version: (\d+), dated (\d{4}-\d{2}-\d{2})', packet)
    require(identity is not None, 'Missing packet version and date')
    require(int(identity.group(1)) == spec['source_packet']['version'] == spec['packet_version'],
            'Packet version changed')
    require(identity.group(2) == spec['source_packet']['date'], 'Packet date changed')
    require(hashlib.sha256((HERE / 'source-packet.md').read_bytes()).hexdigest() == spec['source_packet']['sha256'],
            'Source packet snapshot hash changed')
    for key, relative in spec['sources'].items():
        expected_url = 'https://github.com/SeungheonOh/dot-skills/blob/main/skill/source-backed-presentation/' + relative
        require(spec['artifact_source_urls'][key] == expected_url, 'Unexpected public source URL')
    require(spec['slide_count'] == len(spec['slides']) == 5, 'Expected exactly five slides')
    require([s['number'] for s in spec['slides']] == list(range(1, 6)), 'Slide order changed')
    require(len(spec['rejected_claims']) == 3, 'Rejected claims missing')
    for key, link in spec['sources'].items():
        filename, anchor = link.split('#', 1)
        require(filename == 'source-packet.md', f'Unexpected source file: {key}')
        require(f'id="{anchor}"' in packet, f'Missing source anchor: {key}')
    for s in spec['slides']:
        require(s['title'] and s['notes'] and s['sources'] and s['caveat'], 'Incomplete slide')
        require(spec['source_packet']['sha256'] in s['notes'] and
                spec['source_packet']['date'] in s['notes'] and
                'main branch and may change' in s['notes'], 'Missing source snapshot disclosure')
        require(s['title'] in script and s['notes'] in script, 'Script/specification mismatch')
        for key in s['sources']:
            require(key in spec['sources'], f'Unknown source: {key}')
            require(f'[{key}]({spec["sources"][key]})' in script, f'Missing script link: {key}')
    chart = spec['slides'][1]['chart']
    # Parse the fixture's supplied summary medians, not individual durations.
    row = next(x for x in packet.splitlines() if x.startswith('| Median elapsed time'))
    values = [int(re.search(r'\d+', x).group()) for x in row.split('|')[2:4]]
    require(chart['values'] == values == [18, 12], 'Chart differs from the supplied medians')
    require(chart['minimum'] == 0 and chart['maximum'] == 24 and chart['major_unit'] == 6,
            'Expected a zero-based 0–24-hour axis in six-hour steps')
    require(values[0] - values[1] == 6, 'Observed six-hour difference changed')
    row = next(x for x in packet.splitlines() if x.startswith('| Completed requests'))
    counts = [int(x.strip()) for x in row.split('|')[2:4]]
    row = next(x for x in packet.splitlines() if x.startswith('| Requests reopened'))
    reopened = [int(x.strip()) for x in row.split('|')[2:4]]
    for i, comparison in enumerate(spec['slides'][2]['comparisons']):
        require(comparison['value'] == f'{reopened[i]} / {counts[i]}', 'Reopening count changed')
        require(comparison['detail'].startswith(f'{100 * reopened[i] / counts[i]:.1f}%'),
                'Reopening percentage or rounding changed')
    require('unapproved' in spec['status'].lower(), 'Approval state changed')
    return {'slides': 5, 'source_sections': len(spec['sources']),
            'derived_checks': ['18 - 12 = 6 hours', '4/40 = 10.0%', '7/60 rounds to 11.7%']}


def check_package(path, spec):
    with ZipFile(path) as z:
        require(z.testzip() is None, 'Corrupt ZIP member')
        names = z.namelist()
        slides = sorted(n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml', n))
        notes = sorted(n for n in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n))
        require(len(slides) == len(notes) == 5, 'Wrong slide or notes count')
        require(not any('/comments/' in n or n.endswith('vbaProject.bin') for n in names),
                'Unexpected comments or macros')
        presentation = ET.fromstring(z.read('ppt/presentation.xml'))
        size = presentation.find('p:sldSz', NS)
        require((size.get('cx'), size.get('cy')) == ('12192000', '6858000'), 'Wrong canvas')
        native_text_counts = []
        actual_links = []
        for s in spec['slides']:
            i = s['number']
            root = ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
            text = element_text(root)
            require(root.get('show') != '0', f'Slide {i} is hidden')
            require(not root.findall('.//p:pic', NS), f'Slide {i} contains a raster picture')
            require(root.find('.//p:ph[@type="title"]', NS) is not None, f'Slide {i} has no native title')
            native_text_counts.append(len(root.findall('.//p:sp', NS)))
            required_text = [s['title'], s['lead'], s['caveat']] + s['body']
            for comparison in s.get('comparisons', []):
                required_text.extend(comparison.values())
            for value in required_text:
                require(normalized(value) in text, f'Slide {i} misses authored text: {value}')
            note_root = ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
            note_text = element_text(note_root)
            require(normalized(s['notes']) in note_text, f'Slide {i} notes differ')
            rels = ET.fromstring(z.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
            external = [r.get('Target') for r in rels if r.get('TargetMode') == 'External']
            expected = [spec['artifact_source_urls'][key] for key in s['sources']]
            require(sorted(external) == sorted(expected), f'Slide {i} source links differ')
            actual_links.extend(external)
            for link in expected:
                require(link in note_text, f'Slide {i} notes miss a source locator')
        chart_names = [n for n in names if re.search(r'/charts/chart\d+\.xml$', n)]
        require(len(chart_names) == 1, 'Expected one native chart')
        chart = ET.fromstring(z.read(chart_names[0]))
        require(chart.find('.//c:barChart', NS) is not None, 'Missing native bar chart')
        values = [float(n.text) for n in chart.findall('.//c:val/c:numRef/c:numCache/c:pt/c:v', NS)]
        categories = [n.text for n in chart.findall('.//c:cat/c:strRef/c:strCache/c:pt/c:v', NS)]
        expected = spec['slides'][1]['chart']
        require(values == expected['values'], 'Native chart values differ')
        require(categories == expected['categories'], 'Native chart category order differs')
        slide2 = ET.fromstring(z.read('ppt/slides/slide2.xml'))
        require(slide2.find('.//c:chart', NS) is not None, 'Chart missing from slide 2')
        alt = slide2.find('.//p:nvGraphicFramePr/p:cNvPr', NS)
        require(alt is not None and 'Baseline: 18 hours' in alt.get('descr', ''), 'Chart alt text missing')
        workbooks = [n for n in names if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')]
        require(len(workbooks) == 1, 'Expected one embedded chart-data workbook')
        with ZipFile(io.BytesIO(z.read(workbooks[0]))) as workbook:
            strings = []
            if 'xl/sharedStrings.xml' in workbook.namelist():
                ss = ET.fromstring(workbook.read('xl/sharedStrings.xml'))
                strings = [''.join(t.text or '' for t in si.findall('.//s:t', NS)) for si in ss]
            numbers, labels = [], []
            for member in workbook.namelist():
                if re.fullmatch(r'xl/worksheets/sheet\d+\.xml', member):
                    sheet = ET.fromstring(workbook.read(member))
                    for cell in sheet.findall('.//s:c', NS):
                        v = cell.find('s:v', NS)
                        if cell.get('t') == 'inlineStr':
                            labels.append(''.join(n.text or '' for n in cell.findall('.//s:t', NS)))
                        elif cell.get('t') == 's' and v is not None:
                            labels.append(strings[int(v.text)])
                        elif v is not None and cell.get('t') in (None, 'n'):
                            numbers.append(float(v.text))
            require(numbers == expected['values'], 'Embedded workbook numbers differ')
            require([x for x in labels if x in expected['categories']] == expected['categories'],
                    'Embedded workbook category order differs')
            inspect_hygiene(workbook, set())
        inspect_hygiene(z, set(actual_links))
        core = ET.fromstring(z.read('docProps/core.xml'))
        for node in core:
            if node.tag.rsplit('}', 1)[-1] in ('creator', 'lastModifiedBy'):
                require(node.text == 'Fictional workflow example', 'Unexpected authorship metadata')
        return {'slides': 5, 'notes_parts': 5, 'native_text_shapes_per_slide': native_text_counts,
                'native_charts': 1, 'embedded_workbooks': 1, 'public_source_links': len(actual_links),
                'raster_slide_pictures': 0, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'bytes': path.stat().st_size,
                'boundary': 'Package checks only. No visual or application-level verification by this script.'}


def inspect_hygiene(z, allowed_external):
    for name in z.namelist():
        if not name.endswith(('.xml', '.rels')):
            continue
        raw = z.read(name).decode('utf-8-sig')
        root = ET.fromstring(raw)
        require(not re.search(r'(?:file:/|[A-Za-z]:\\|/(?:home|Users|workspace|tmp|opt|root)/)', raw),
                f'Local path in {name}')
        if name.endswith('.rels'):
            for rel in root:
                if rel.get('TargetMode') == 'External':
                    require(rel.get('Target') in allowed_external, f'Unexpected external target in {name}')
        if name.startswith('docProps/'):
            for node in root.iter():
                if node.tag.rsplit('}', 1)[-1] == 'Application':
                    require(not node.text, 'Unexpected software metadata')


def self_test(spec):
    bad = copy.deepcopy(spec)
    bad['slides'][1]['chart']['values'][1] = 10
    try:
        check_content(bad)
    except ValueError:
        pass
    else:
        raise ValueError('Changed chart value was not rejected')
    bad = copy.deepcopy(spec)
    bad['sources']['S1'] = 'source-packet.md#missing-section'
    try:
        check_content(bad)
    except ValueError:
        pass
    else:
        raise ValueError('Broken source anchor was not rejected')
    return ['Changed chart value rejected', 'Broken source anchor rejected']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pptx', type=Path, nargs='?')
    args = parser.parse_args()
    spec = json.loads((HERE / 'deck-spec.json').read_text(encoding='utf-8'))
    result = {'content': check_content(spec), 'negative_checks': self_test(spec)}
    if args.pptx:
        result['package'] = check_package(args.pptx, spec)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
