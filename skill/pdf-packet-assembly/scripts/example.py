#!/usr/bin/env python3
"""Small original PDF packet example; not a general-purpose PDF preservation tool.

Commands: create NEW_DIRECTORY | check DIRECTORY | negatives DIRECTORY NEW_DIRECTORY
Requires installed pypdf, reportlab, Pillow and Poppler pdftoppm. No network use.
"""
import argparse
import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

import PIL
from PIL import Image, ImageChops, ImageDraw, ImageFont
import pypdf
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import (ArrayObject, DictionaryObject, Fit, NameObject,
                          NumberObject, TextStringObject)
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PLAN = [('source-a.pdf', 1), ('source-b.pdf', 2),
        ('source-a.pdf', 2), ('source-a.pdf', 3)]
BOXES = ('mediabox', 'cropbox', 'bleedbox', 'trimbox', 'artbox')
DPI = 100


class Hold(ValueError):
    """A decision or unsupported feature prevents safe assembly."""


def need(condition, message):
    if not condition:
        raise Hold(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': digest(data)}


def save_new(path, data):
    with path.open('xb') as stream:
        stream.write(data)


def write_json(path, value):
    save_new(path, (json.dumps(value, indent=2) + '\n').encode())


def page_state(page):
    stream = page.get_contents()
    return {
        'boxes': {key: [float(v) for v in getattr(page, key)] for key in BOXES},
        'rotation': int(page.get('/Rotate', 0)),
        'user_unit': float(page.get('/UserUnit', 1)),
        'text': page.extract_text(),
        'decoded_content_sha256': digest(stream.get_data() if stream is not None else b''),
    }


def destination_page(reader, dest):
    need(isinstance(dest, ArrayObject) and len(dest) == 2 and dest[1] == '/Fit',
         'Only a direct internal /Fit destination is supported by this example')
    ref = dest[0]
    for index, page in enumerate(reader.pages):
        if page.indirect_reference == ref:
            return index + 1
    raise Hold('Internal destination has no page in this source')


def preflight(reader):
    """Conservative support gate for these simple fixtures, not a security scan."""
    need(not reader.is_encrypted, 'Encrypted source: establish an authorized route')
    root = reader.root_object
    need('/AcroForm' not in root and '/Perms' not in root,
         'Form or signature indicators require a separate preservation decision')
    allowed_root = {'/Type', '/Pages', '/PageMode', '/Outlines'}
    need(not (set(root) - allowed_root),
         f'Unsupported catalog feature(s): {sorted(set(root) - allowed_root)}')
    need(root.get('/PageMode', '/UseNone') in ('/UseNone', '/UseOutlines'),
         'Unsupported initial viewer mode')
    links = []
    allowed_page = {'/Type', '/Parent', '/Resources', '/Contents', '/Annots',
                    '/MediaBox', '/CropBox', '/BleedBox', '/TrimBox', '/ArtBox',
                    '/Rotate', '/UserUnit', '/Trans'}
    allowed_link = {'/Type', '/Subtype', '/Rect', '/Border', '/Dest', '/Contents'}
    for number, page in enumerate(reader.pages, 1):
        need(not (set(page) - allowed_page),
             f'Unsupported page {number} feature(s): {sorted(set(page) - allowed_page)}')
        need(not page.get('/Trans'), 'Page transitions are not supported')
        need(int(page.get('/Rotate', 0)) in (0, 90, 180, 270), 'Unsupported rotation')
        need(float(page.get('/UserUnit', 1)) == 1, 'Non-default UserUnit is unsupported')
        for ref in page.get('/Annots', []):
            annot = ref.get_object()
            need(annot.get('/Subtype') == '/Link',
                 f'Page {number}: non-link annotation or widget requires a decision')
            need(not (set(annot) - allowed_link),
                 f'Page {number}: unsupported link feature(s): {sorted(set(annot) - allowed_link)}')
            need('/Dest' in annot, 'Only direct internal links are supported')
            need(len(annot['/Rect']) == 4, 'Invalid link rectangle')
            need(list(annot.get('/Border', [])) == [0, 0, 0],
                 'This example only supports invisible link borders')
            links.append({'page': number,
                          'target': destination_page(reader, annot['/Dest']),
                          'rect': [float(v) for v in annot['/Rect']],
                          'contents': str(annot.get('/Contents', ''))})
    outlines = []
    if '/Outlines' in root:
        node = root['/Outlines'].get('/First')
        seen = set()
        while node:
            marker = (node.idnum, node.generation)
            need(marker not in seen, 'Outline cycle')
            seen.add(marker)
            item = node.get_object()
            allowed = {'/Title', '/Dest', '/Parent', '/Prev', '/Next', '/Count'}
            need(not (set(item) - allowed), 'Only plain flat direct-destination outlines are supported')
            need('/Dest' in item and int(item.get('/Count', 0)) == 0,
                 'Nested, styled or action-based outlines need another route')
            outlines.append({'title': str(item['/Title']),
                             'target': destination_page(reader, item['/Dest'])})
            node = item.get('/Next')
    return {'page_count': len(reader.pages), 'links': links, 'outlines': outlines,
            'encryption': False, 'form_or_signature_indicators': False,
            'catalog_embedded_files_or_names': False,
            'unsupported_catalog_page_or_annotation_features': []}


def sources(folder):
    return {name: PdfReader(folder / name, strict=True)
            for name in dict.fromkeys(name for name, _ in PLAN)}


def assemble(folder, output, plan=PLAN):
    need(not output.exists(), f'Output already exists: {output.name}')
    readers = sources(folder)
    before = {name: identity(folder / name) for name in readers}
    inventories = {name: preflight(reader) for name, reader in readers.items()}
    need(len(set(plan)) == len(plan), 'Repeated source pages need an explicit link occurrence policy')
    positions = {pair: index for index, pair in enumerate(plan)}
    for name, page in plan:
        need(name in readers and 1 <= page <= len(readers[name].pages), 'Invalid source/page selection')
    # Resolve every selected link and every source outline before creating output bytes.
    for name, inventory in inventories.items():
        for link in inventory['links']:
            if (name, link['page']) in positions:
                need((name, link['target']) in positions,
                     f'Missing link target: {name} page {link["target"]}')
        for outline in inventory['outlines']:
            need((name, outline['target']) in positions,
                 f'Omitted outline target needs a decision: {name} page {outline["target"]}')
    writer = PdfWriter()
    for name, page in plan:
        # Do not clone stale annotation destinations. Rebuild the supported links below.
        candidate = copy.copy(readers[name].pages[page - 1])
        candidate.pop('/Annots', None)
        writer.add_page(candidate, excluded_keys=['/Annots'])
    for name, inventory in inventories.items():
        for link in inventory['links']:
            if (name, link['page']) not in positions:
                continue
            annotation = Link(rect=link['rect'], border=[0, 0, 0],
                              target_page_index=positions[(name, link['target'])], fit=Fit.fit())
            annotation[NameObject('/Contents')] = TextStringObject(link['contents'])
            added = writer.add_annotation(positions[(name, link['page'])], annotation)
            # A local explicit destination identifies an actual output page object.
            added[NameObject('/Dest')] = ArrayObject([
                writer.pages[positions[(name, link['target'])]].indirect_reference,
                NameObject('/Fit')])
    outlines = [(positions[(name, item['target'])], item['title'])
                for name, inv in inventories.items() for item in inv['outlines']]
    for position, title in sorted(outlines):
        writer.add_outline_item(title, position, fit=Fit.fit())
    writer.page_mode = '/UseOutlines'
    writer.add_metadata({'/Title': 'Pine Room setup packet',
                         '/Subject': 'Original fictional selected-page assembly example'})
    data = io.BytesIO()
    writer.write(data)
    need(before == {name: identity(folder / name) for name in readers},
         'Source bytes changed during assembly')
    save_new(output, data.getvalue())
    return inventories


def fixtures(folder):
    """All wording and vectors below are original and fictional."""
    fonts = Path(reportlab.__file__).parent / 'fonts'
    for name, filename in [('PacketSans', 'Vera.ttf'), ('PacketSans-Bold', 'VeraBd.ttf')]:
        need((fonts / filename).is_file(), f'ReportLab bundled font missing: {filename}')
        pdfmetrics.registerFont(TTFont(name, str(fonts / filename)))
    blue = (0.08, 0.24, 0.36)
    def begin(title, size=(612, 792)):
        buf = io.BytesIO()
        pdf = canvas.Canvas(buf, pagesize=size, invariant=1, pageCompression=1)
        pdf.setTitle(title)
        pdf.setAuthor('PDF packet assembly example')
        return buf, pdf
    def heading(pdf, label, title, height):
        pdf.setFillColorRGB(*blue)
        pdf.setFont('PacketSans', 11)
        pdf.drawString(48, height - 52, label)
        pdf.setFont('PacketSans-Bold', 28)
        pdf.drawString(48, height - 96, title)
        pdf.setStrokeColorRGB(*blue)
        pdf.line(48, height - 118, 564 if height == 792 else 744, height - 118)
    def lines(pdf, rows, y, step=26):
        pdf.setFillColorRGB(0.12, 0.16, 0.19)
        pdf.setFont('PacketSans', 15)
        for text in rows:
            pdf.drawString(48, y, text)
            y -= step
    buf, pdf = begin('Pine Room notes - source A')
    heading(pdf, 'SOURCE A / PHYSICAL PAGE 1', 'Pine Room setup', 792)
    lines(pdf, ['Fictional planning notes for a quiet reading session.',
                'Use the east table for supplies.',
                'Keep the door path clear.',
                'Chairs: 12. Table groups: 3.'], 622)
    pdf.setFillColorRGB(*blue)
    pdf.setFont('PacketSans-Bold', 16)
    pdf.drawString(48, 456, 'Open the equipment appendix')
    pdf.line(48, 452, 323, 452)
    pdf.linkRect('Open equipment appendix', 'appendix', (46, 450, 325, 474),
                 relative=0, thickness=0)
    pdf.bookmarkPage('summary', fit='Fit')
    pdf.addOutlineEntry('Setup summary', 'summary', level=0)
    lines(pdf, ['Original source numbering is retained in this packet.',
                'Source A page 2 is an intentionally blank divider.'], 360)
    pdf.showPage()
    # Deliberately no ink, labels or annotation on the selected blank page.
    pdf.showPage()
    heading(pdf, 'SOURCE A / PHYSICAL PAGE 3', 'Equipment appendix', 792)
    lines(pdf, ['Bring these items to the east table:',
                '12 chairs', '3 table markers', '1 supply tray',
                'No power equipment is needed.'], 622)
    pdf.bookmarkPage('appendix', fit='Fit')
    pdf.addOutlineEntry('Equipment appendix', 'appendix', level=0)
    pdf.showPage()
    pdf.save()
    save_new(folder / 'source-a.pdf', buf.getvalue())
    buf, pdf = begin('Pine Room layout - source B')
    heading(pdf, 'SOURCE B / PHYSICAL PAGE 1 / EXCLUDED', 'Draft layout', 792)
    lines(pdf, ['Superseded fictional sketch notes.',
                'This page is not part of the requested packet.'], 622)
    pdf.showPage()
    pdf.setPageSize((792, 612))
    heading(pdf, 'SOURCE B / PHYSICAL PAGE 2', 'Reading room layout', 612)
    pdf.setStrokeColorRGB(*blue)
    pdf.setLineWidth(2)
    pdf.rect(48, 128, 696, 324, fill=0)
    pdf.setFont('PacketSans-Bold', 14)
    for x, label in [(104, 'Table 1'), (310, 'Table 2'), (516, 'Table 3')]:
        pdf.setFillColorRGB(0.9, 0.95, 0.96)
        pdf.roundRect(x, 280, 156, 86, 10, fill=1)
        pdf.setFillColorRGB(*blue)
        pdf.drawCentredString(x + 78, 316, label)
    pdf.setFont('PacketSans', 14)
    pdf.drawString(66, 186, 'Clear door path')
    pdf.line(66, 170, 670, 170)
    pdf.line(658, 178, 670, 170)
    pdf.line(658, 162, 670, 170)
    pdf.drawString(544, 416, 'East supply table')
    pdf.setFont('PacketSans', 12)
    pdf.drawString(48, 70, 'Fictional diagram. Landscape page retained at its original size.')
    pdf.bookmarkPage('layout', fit='Fit')
    pdf.addOutlineEntry('Reading room layout', 'layout', level=0)
    pdf.showPage()
    pdf.save()
    save_new(folder / 'source-b.pdf', buf.getvalue())


def check(folder, output=None):
    check_record = output is None
    output = output or folder / 'packet.pdf'
    readers = sources(folder)
    result = PdfReader(output, strict=True)
    need(len(result.pages) == len(PLAN), 'Output page count differs from the selection')
    for index, (name, page) in enumerate(PLAN):
        need(page_state(readers[name].pages[page - 1]) == page_state(result.pages[index]),
             f'Content, boxes or rotation mismatch at output page {index + 1}')
    # Native annotation inspection; nothing here opens a URL or executes an action.
    expected_links = []
    positions = {pair: index + 1 for index, pair in enumerate(PLAN)}
    for name, reader in readers.items():
        inv = preflight(reader)
        for link in inv['links']:
            if (name, link['page']) in positions:
                expected_links.append({'page': positions[(name, link['page'])],
                    'target': positions[(name, link['target'])],
                    'rect': link['rect'], 'contents': link['contents']})
    actual_links = []
    for number, page in enumerate(result.pages, 1):
        for ref in page.get('/Annots', []):
            a = ref.get_object()
            need(a.get('/Subtype') == '/Link' and '/A' not in a, 'Unexpected output annotation/action')
            dest = a['/Dest']
            target = destination_page(result, dest)
            need(len(dest) == 2 and dest[1] == '/Fit', 'Unexpected output destination fit')
            need(list(a.get('/Border', [])) == [0, 0, 0], 'Changed link border')
            actual_links.append({'page': number, 'target': target,
                                 'rect': [float(v) for v in a['/Rect']],
                                 'contents': str(a.get('/Contents', ''))})
    need(actual_links == expected_links, 'Output internal link target/rectangle mismatch')
    actual_outlines = []
    for item in result.outline:
        need(not isinstance(item, list), 'Unexpected nested output outline')
        target = result.get_destination_page_number(item)
        need(target is not None, 'Unresolved output outline')
        actual_outlines.append({'title': item.title, 'output_page': target + 1})
    expected_outlines = sorted(
        ({'title': item['title'], 'output_page': positions[(name, item['target'])]}
         for name, reader in readers.items() for item in preflight(reader)['outlines']),
        key=lambda item: item['output_page'])
    need(actual_outlines == expected_outlines, 'Output outline target/order mismatch')
    record_path = folder / 'verification.json'
    if check_record and record_path.exists():
        record = json.loads(record_path.read_text())
        for name, expected in record['files'].items():
            need(identity(folder / name) == expected, f'Saved identity mismatch: {name}')
        page_map = json.loads((folder / 'page-map.json').read_text())
        need([(item['source'], item['source_physical_page']) for item in page_map] == PLAN,
             'Page map selection/order differs')
        for index, item in enumerate(page_map):
            need(item['output_page'] == index + 1 and
                 item['source_identity'] == identity(folder / item['source']), 'Page map lineage differs')
            need(all(item[key] == value for key, value in page_state(result.pages[index]).items()),
                 'Page map content/geometry differs')
    return {'page_count': len(result.pages), 'page_content_text_boxes_rotation': 'pass',
            'internal_links': actual_links, 'outlines': actual_outlines}


def render_and_compare(folder, target):
    target.mkdir()
    paths = {}
    for name in ['source-a.pdf', 'source-b.pdf', 'packet.pdf']:
        prefix = target / Path(name).stem
        subprocess.run(['pdftoppm', '-r', str(DPI), '-png', str(folder / name), str(prefix)],
                       check=True, capture_output=True)
        paths[name] = sorted(target.glob(prefix.name + '-*.png'))
    results = []
    for index, (name, page) in enumerate(PLAN):
        with Image.open(paths[name][page - 1]) as src, Image.open(paths['packet.pdf'][index]) as out:
            need(src.size == out.size and ImageChops.difference(src.convert('RGB'), out.convert('RGB')).getbbox() is None,
                 f'Render mismatch on output page {index + 1}')
            results.append({'output_page': index + 1, 'same_rgb_pixels': True,
                            'render_size': list(out.size)})
    with Image.open(paths['packet.pdf'][2]) as blank:
        need(blank.convert('RGB').getextrema() == ((255, 255),) * 3,
             'Selected divider is not blank in the saved output render')
    # Contact sheet: labels are outside the PDF page images, including the true blank.
    sheet = Image.new('RGB', (1100, 1490), '#e7edf0')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=18)
    labels = ['1 | A1 - summary', '2 | B2 - landscape diagram',
              '3 | A2 - intentional blank', '4 | A3 - appendix']
    for index, path in enumerate(paths['packet.pdf']):
        x, y = 20 + (index % 2) * 550, 18 + (index // 2) * 745
        draw.text((x, y), labels[index], fill='#123d51', font=font)
        with Image.open(path) as img:
            img.thumbnail((510, 690))
            sheet.paste(img, (x, y + 32))
            draw.rectangle((x, y + 32, x + img.width, y + 32 + img.height), outline='#96a9b4')
    sheet.save(folder / 'preview.png')
    return results


def negatives(folder, target):
    target.mkdir()
    results = []
    def expect_hold(label, call, absent=None):
        try:
            call()
        except Hold as error:
            need(absent is None or not absent.exists(), f'{label} wrote an output before holding')
            results.append({'test': label, 'result': 'caught', 'reason': str(error)})
        else:
            raise AssertionError(f'{label}: failure was not caught')
    missing = target / 'missing-target.pdf'
    expect_hold('omitted internal-link target',
                lambda: assemble(folder, missing, PLAN[:-1]), missing)
    before = identity(folder / 'packet.pdf')
    expect_hold('existing output', lambda: assemble(folder, folder / 'packet.pdf'))
    need(identity(folder / 'packet.pdf') == before, 'Existing output was modified')
    # Harmless optional-content marker: unsupported, no script or action is executed.
    unsupported = target / 'unsupported-copy.pdf'
    writer = PdfWriter(clone_from=folder / 'source-a.pdf')
    writer.root_object[NameObject('/OCProperties')] = DictionaryObject()
    with unsupported.open('xb') as stream:
        writer.write(stream)
    expect_hold('unsupported optional-content catalog',
                lambda: preflight(PdfReader(unsupported, strict=True)))
    for label in ['wrong order', 'dropped blank', 'changed rotation', 'changed crop box',
                  'broken link', 'graphics-only content change']:
        writer = PdfWriter(clone_from=folder / 'packet.pdf')
        if label == 'wrong order':
            pages = list(writer.pages)
            writer = PdfWriter()
            for index in [1, 0, 2, 3]:
                writer.add_page(pages[index])
        elif label == 'dropped blank':
            del writer.pages[2]
        elif label == 'changed rotation':
            writer.pages[1].rotate(90)
        elif label == 'changed crop box':
            writer.pages[1].cropbox.upper_right = (700, 600)
        elif label == 'broken link':
            annot = writer.pages[0]['/Annots'][0].get_object()
            annot[NameObject('/Dest')] = ArrayObject([writer.pages[1].indirect_reference, NameObject('/Fit')])
        else:
            stream = writer.pages[1].get_contents()
            need(stream is not None, 'Graphics mutation requires a content stream')
            stream.set_data(stream.get_data() + b'\nq 1 0 0 RG 4 w 60 140 m 730 430 l S Q\n')
            writer.pages[1].replace_contents(stream)
        path = target / (label.replace(' ', '-') + '.pdf')
        with path.open('xb') as stream:
            writer.write(stream)
        if label == 'graphics-only content change':
            original = page_state(PdfReader(folder / 'packet.pdf').pages[1])
            mutated = page_state(PdfReader(path).pages[1])
            need(original['text'] == mutated['text'], 'Graphics-only mutation changed text')
            need(all(original[key] == mutated[key] for key in ('boxes', 'rotation', 'user_unit')),
                 'Graphics-only mutation changed page geometry')
            need(original['decoded_content_sha256'] != mutated['decoded_content_sha256'],
                 'Graphics-only mutation did not change the native-content hash')
        expect_hold(label, lambda: check(folder, path))
        if label == 'graphics-only content change':
            results[-1]['extracted_text_unchanged'] = True
            results[-1]['decoded_content_hash_changed'] = True
    write_json(target / 'negative-results.json', results)
    return results


def create(folder):
    folder.mkdir()
    fixtures(folder)
    source_ids = {name: identity(folder / name) for name in ('source-a.pdf', 'source-b.pdf')}
    inventories = assemble(folder, folder / 'packet.pdf')
    result = check(folder)
    result['renders'] = render_and_compare(folder, folder / 'renders')
    need(source_ids == {name: identity(folder / name) for name in source_ids}, 'Source changed')
    page_map = [{'output_page': index + 1, 'source': name, 'source_physical_page': page,
                 'source_identity': source_ids[name],
                 'intentional_blank': (name, page) == ('source-a.pdf', 2),
                 **page_state(sources(folder)[name].pages[page - 1])}
                for index, (name, page) in enumerate(PLAN)]
    write_json(folder / 'page-map.json', page_map)
    result.update({'tools': {'python': sys.version.split()[0], 'pypdf': pypdf.__version__,
                  'reportlab': reportlab.Version, 'Pillow': PIL.__version__,
                  'pdftoppm': subprocess.run(['pdftoppm', '-v'], capture_output=True,
                                           text=True, check=True).stderr.splitlines()[0]},
                  'render_dpi': DPI, 'preflight': inventories,
                  'files': {name: identity(folder / name) for name in
                            ['source-a.pdf', 'source-b.pdf', 'packet.pdf', 'preview.png']},
                  'originals_unchanged': True,
                  'manual_visual_review': 'pending; automation does not certify visual quality',
                  'viewer_click_test': 'not performed',
                  'scope': 'Four original fixture pages; same-renderer pixels and direct navigation only'})
    write_json(folder / 'verification.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['create', 'check', 'negatives'])
    parser.add_argument('directory', type=Path)
    parser.add_argument('negative_directory', type=Path, nargs='?')
    args = parser.parse_args()
    if args.command == 'create':
        result = create(args.directory)
    elif args.command == 'check':
        result = check(args.directory)
    else:
        parser.error('negatives requires a new directory') if args.negative_directory is None else None
        result = negatives(args.directory, args.negative_directory)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
