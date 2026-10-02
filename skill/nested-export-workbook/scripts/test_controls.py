"""Meaningful rejection and saved-file corruption controls. Writes disposable copies."""
import argparse
import copy
import json
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from prepare import Held, load_source, make_plan
from check import NS, check, digest, read_xlsx


def controls(source, workbook, scratch):
    raw = source.read_bytes()
    original = json.loads(raw)
    before = digest(source)
    rejected = []
    invalid = {
        'malformed JSON': b'{"format":',
        'duplicate object key': raw.replace(b'"format":', b'"format":"first", "format":', 1),
        'escaped duplicate object key': raw.replace(b'"format":', b'"for\\u006dat":"first", "format":', 1),
        'non-finite number': raw.replace(b'"quantity": 0', b'"quantity": NaN', 1),
        'decimal conversion': raw.replace(b'"quantity": 0', b'"quantity": 0.1', 1),
        'large numeric value': raw.replace(b'"quantity": 0', b'"quantity": 9007199254740993', 1),
        'negative zero': raw.replace(b'"quantity": 0', b'"quantity": -0', 1),
        'wrong relationship type': raw.replace(b'"items": []', b'"items": {}', 1),
        'unknown schema field': raw.replace(b'"format":', b'"unused": 1, "format":', 1),
        'XML control character': raw.replace(b'"Washers"', b'"\\u0000"', 1),
        'unrepresentable cell length': raw.replace(b'"Washers"', b'"'+b'x'*32768+b'"', 1),
        'unsupported direct timestamp text': raw.replace(b'"Washers"', b'"2026-10-01T12:00:00Z"', 1),
        'unsupported quote-formula prefix': raw.replace(b'"Washers"', b'"\'=1+1"', 1)
    }
    for name, payload in invalid.items():
        trial = scratch / 'invalid.json'
        trial.write_bytes(payload)
        try:
            load_source(trial)
        except Held:
            rejected.append(name)
        else:
            raise AssertionError('Invalid input accepted: '+name)
        assert trial.read_bytes() == payload
    # Repeated business IDs and identical child values retain occurrences.
    repeated = copy.deepcopy(original)
    repeated['collections'][1]['id'] = repeated['collections'][0]['id']
    trial = scratch / 'repeated.json'
    trial.write_text(json.dumps(repeated), encoding='utf-8')
    repeated_raw, repeated_data = load_source(trial)
    plan = make_plan(trial.name, repeated_raw, repeated_data)
    assert plan['counts']['collections'] == 5 and plan['counts']['labels'] == 3
    assert plan['rows']['Collections'][0][1] == plan['rows']['Collections'][1][1]
    assert plan['rows']['Collections'][0][-1] != plan['rows']['Collections'][1][-1]

    detected = []
    sheet_files = {name: entry['xml'] for name, entry in read_xlsx(workbook).items()}
    mutations = [
        ('zero erased', 'Items', 'E2', None),
        ('long ID changed', 'Collections', 'B2', '000123456789012345678999'),
        ('wrong parent link', 'Items', 'J2', '/collections/1'),
        ('missing relabelled as null', 'Items', 'F4', 'NULL'),
        ('literal made into formula', 'Items', 'D3', ('formula', '1+1')),
        ('label occurrence removed', 'Labels', 'A3', ('remove-row', None)),
        ('source pointer altered', 'Source paths', 'B10', '/wrong'),
        ('unmapped review content', 'Items', 'K2', 'Unexpected value outside the mapped table'),
        ('unmapped metadata content', 'Read me', 'C2', 'Unexpected value outside the metadata area')
    ]
    for name, sheet, ref, change in mutations:
        target = sheet_files[sheet]
        with zipfile.ZipFile(workbook) as original_zip:
            root = ET.fromstring(original_zip.read(target))
            cell = root.find(f'.//s:c[@r="{ref}"]', NS)
            if cell is None:
                row_number = ''.join(c for c in ref if c.isdigit())
                row = root.find(f'.//s:row[@r="{row_number}"]', NS)
                assert row is not None
                cell = ET.SubElement(row, '{'+NS['s']+'}c', {'r': ref})
            if isinstance(change, tuple) and change[0] == 'remove-row':
                rows = root.find('s:sheetData', NS)
                rows.remove(root.find('.//s:row[@r="3"]', NS))
            else:
                for child in list(cell): cell.remove(child)
                if isinstance(change, tuple):
                    cell.attrib.pop('t', None)
                    ET.SubElement(cell, '{'+NS['s']+'}f').text = change[1]
                elif change is not None:
                    cell.set('t', 'inlineStr')
                    node = ET.SubElement(cell, '{'+NS['s']+'}is')
                    ET.SubElement(node, '{'+NS['s']+'}t').text = change
                else:
                    cell.attrib.pop('t', None)
            damaged = scratch / 'damaged.xlsx'
            with zipfile.ZipFile(damaged, 'w', zipfile.ZIP_DEFLATED) as output:
                for member in original_zip.infolist():
                    output.writestr(member, ET.tostring(root, encoding='utf-8') if member.filename == target else original_zip.read(member))
        try:
            check(source, damaged)
        except AssertionError:
            detected.append(name)
        else:
            raise AssertionError('Corruption not detected: '+name)
    assert digest(source) == before
    return {'rejected_inputs': rejected, 'detected_saved_file_corruptions': detected,
            'positive_controls': ['repeated business ID retained by source occurrence', 'repeated sibling label retained'],
            'source_unchanged': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('workbook', type=Path)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    result = controls(args.source, args.workbook, args.scratch)
    args.report.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
