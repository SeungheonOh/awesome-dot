#!/usr/bin/env python3
"""Narrow checks for the included HarborDesk fixture, not a general DOCX validator."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/package/2006/relationships}'
URLS = [
    'https://example.com/harbordesk/releases/2.4.1?rev=3#checks',
    'https://example.com/harbordesk/issues/new?template=delivery',
]
EXPECTED_ROWS = [
    ['Platform', 'Passed', 'Failed', 'Build identifier'],
    ['Windows 11 x64', '18', '0', 'HD-0241-WIN'],
    ['macOS 14 ARM64', '14', '0', 'HD-0241-MAC'],
    ['Ubuntu 24.04 x64', '12', '0', 'HD-0241-LNX'],
    ['Total', '44', '0', '3 platform runs'],
]

def norm(text):
    # Normalize whitespace only; keep accents, signs, identifiers and punctuation.
    return ' '.join(text.split())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def source_report(path):
    issues = []
    with ZipFile(path) as z:
        members = z.namelist()
        if len(members) != len(set(members)):
            raise ValueError('Duplicate package member names require review')
        roots = {n: ET.fromstring(z.read(n)) for n in members if n.endswith('.xml')}
        doc = roots['word/document.xml']
        paragraphs = [norm(''.join(t.text or '' for t in p.iter(W+'t')))
                      for p in doc.iter(W+'p')]
        paragraphs = [p for p in paragraphs if p]
        rows = [[norm(''.join(t.text or '' for t in cell.iter(W+'t')))
                 for cell in row.findall(W+'tc')]
                for table in doc.iter(W+'tbl') for row in table.findall(W+'tr')]
        fields = [e.get(W+'instr', '').strip() for root in roots.values()
                  for e in root.iter(W+'fldSimple')]
        complex_fields = [e.text or '' for root in roots.values() for e in root.iter(W+'instrText')]
        review_tags = Counter(e.tag.split('}')[-1] for root in roots.values() for e in root.iter()
            if e.tag.startswith(W) and (e.tag.split('}')[-1] in {
                'ins','del','moveFrom','moveTo','commentRangeStart','commentReference',
                'object','altChunk','sdt','vanish','webHidden','documentProtection',
                'drawing','pict','footnoteReference','endnoteReference'}
                or e.tag.split('}')[-1].endswith('PrChange')))
        external = []
        for n in members:
            if n.endswith('.rels'):
                for e in ET.fromstring(z.read(n)):
                    if e.get('TargetMode') == 'External':
                        external.append({'type':e.get('Type','').rsplit('/',1)[-1], 'target':e.get('Target')})
        active_parts = [n for n in members if any(t in n.lower() for t in
                        ('vbaproject','activex','embeddings/','_xmlsignatures/'))]
        if rows != EXPECTED_ROWS: issues.append('Source table differs from the fixture contract')
        if Counter(fields) != Counter(['PAGE','NUMPAGES']) or complex_fields:
            issues.append('Unexpected or unresolved source fields')
        if review_tags or active_parts: issues.append('Source features need review before conversion')
        if external != [{'type':'hyperlink','target':u} for u in URLS]:
            issues.append('External relationship inventory differs from approved links')
        page_breaks = sum(e.get(W+'type') == 'page' for e in doc.iter(W+'br'))
        if page_breaks != 1: issues.append('Expected one explicit page break')
        if len(list(doc.iter(W+'tbl'))) != 1: issues.append('Expected one native table')
        if not any('General availability remains on hold' in p for p in paragraphs):
            issues.append('Source release condition is missing')
        report = {'source_sha256':digest(path), 'source_bytes':path.stat().st_size,
            'body_paragraphs_including_cells':len(paragraphs), 'table_rows':rows,
            'explicit_page_breaks':page_breaks, 'fields':fields,
            'review_feature_indicators':dict(review_tags), 'active_part_indicators':active_parts,
            'external_relationships':external,
            'custom_xml_parts':[n for n in members if n.startswith('customXml/') and n.endswith('.xml')],
            'issues':issues}
    return report, paragraphs

def pdf_report(path, paragraphs):
    from pypdf import PdfReader
    reader = PdfReader(path)
    issues = []
    pages = [norm(p.extract_text() or '') for p in reader.pages]
    all_text = ' '.join(pages)
    missing = [p for p in paragraphs if p not in all_text]
    if missing: issues.append('Source paragraphs or cells missing/changed in extracted PDF text')
    cursor = 0
    ordered = True
    for paragraph in paragraphs:
        position = all_text.find(paragraph, cursor)
        if position < 0:
            ordered = False
            break
        cursor = position + len(paragraph)
    if not ordered: issues.append('Source body/table paragraph order was not preserved')
    table_block = ' '.join(' '.join(row) for row in EXPECTED_ROWS)
    table_preserved = bool(pages and table_block in pages[0])
    if not table_preserved: issues.append('Ordered table rows/cell associations missing on page 1')
    if len(pages) != 2: issues.append('Expected exactly two pages')
    anchors = ['HarborDesk release delivery brief', 'Recipient delivery checks']
    for i, anchor in enumerate(anchors):
        if i >= len(pages) or anchor not in pages[i]: issues.append('Page anchor mismatch: '+anchor)
    for i, text in enumerate(pages, 1):
        for expected in ['HARBORDESK / RELEASE DELIVERY', f'HD-0241-R3 | Page {i} of 2']:
            if expected not in text: issues.append(f'Page {i}: missing header/footer '+expected)
    unicode_sample = 'Zoë; café; Δ latency = −12 ms; 99.5%; ticket HD-1847; version v2.4.1+rc.03.'
    if unicode_sample not in all_text: issues.append('Unicode or identifier copy check failed')
    links=[]
    for i,page in enumerate(reader.pages,1):
        for ref in page.get('/Annots',[]):
            annotation=ref.get_object(); action=annotation.get('/A',{})
            if action: action=action.get_object()
            if annotation.get('/Subtype') == '/Link':
                links.append({'page':i,'uri':action.get('/URI'), 'action':action.get('/S'),
                              'rect':[float(x) for x in annotation.get('/Rect',[])]})
    if [(l['page'],l['uri'],l['action']) for l in links] != [(1,URLS[0],'/URI'),(2,URLS[1],'/URI')]:
        issues.append('PDF link targets, pages or action types differ')
    boxes=[[float(x) for x in p.mediabox] for p in reader.pages]
    if any(b != [0.0,0.0,612.0,792.0] for b in boxes): issues.append('Expected Letter portrait pages')
    for link in links:
        rect=link['rect']
        if len(rect)!=4 or not (0 <= rect[0] < rect[2] <= 612 and 0 <= rect[1] < rect[3] <= 792):
            issues.append('Link rectangle missing or outside page')
    root=reader.trailer['/Root']
    names=root.get('/Names',{})
    if names: names=names.get_object()
    active={key:bool(root.get(key)) for key in ('/OpenAction','/AA','/AcroForm')}
    active.update({key:bool(names.get(key)) for key in ('/JavaScript','/EmbeddedFiles')})
    if any(active.values()): issues.append('Unexpected PDF action/form/attachment indicators')
    return {'pdf_sha256':digest(path),'pdf_bytes':path.stat().st_size,'pages':len(pages),
        'media_boxes':boxes,'links':links,'source_paragraphs_matched':len(paragraphs)-len(missing),
        'ordered_body_and_table_paragraphs_preserved':ordered, 'ordered_table_block_preserved':table_preserved,
        'missing_or_changed_paragraphs':missing,'active_feature_indicators':active,
        'structure_tree_present':bool(root.get('/StructTreeRoot')),
        'visual_review':'REQUIRED: not performed by this script',
        'accessibility_and_word_compatibility':'NOT ESTABLISHED', 'issues':issues}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('pdf',type=Path,nargs='?')
    args=parser.parse_args()
    source, paragraphs=source_report(args.source)
    report={'source':source}
    if args.pdf: report['pdf']=pdf_report(args.pdf,paragraphs)
    report['machine_checks_passed']=not any(r['issues'] for r in report.values())
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return 0 if report['machine_checks_passed'] else 1

if __name__ == '__main__':
    try: sys.exit(main())
    except Exception as e:
        print(json.dumps({'machine_checks_passed':False,'error':str(e)}),file=sys.stderr)
        sys.exit(2)
