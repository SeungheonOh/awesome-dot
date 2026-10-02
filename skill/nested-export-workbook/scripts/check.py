"""Read-only XLSX checks using Python's ZIP/XML libraries, independent of the writer."""
import argparse
import copy
import hashlib
import json
import posixpath
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
PACKAGE = '{http://schemas.openxmlformats.org/package/2006/relationships}'


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def digest(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def read_xlsx(path):
    sheets = {}
    with zipfile.ZipFile(path) as archive:
        require(not any('vbaProject' in n or n.startswith('xl/externalLinks/') or n == 'xl/connections.xml' for n in archive.namelist()), 'Unexpected active content')
        for member in archive.namelist():
            if member.endswith('.rels'):
                rels = ET.fromstring(archive.read(member))
                require(not any(r.get('TargetMode') == 'External' for r in rels), 'External relationship')
        shared = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            root = ET.fromstring(archive.read('xl/sharedStrings.xml'))
            shared = [''.join(si.itertext()) for si in root]
        rels = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
        targets = {r.get('Id'): r.get('Target') for r in rels}
        book = ET.fromstring(archive.read('xl/workbook.xml'))
        for s in book.find('s:sheets', NS):
            target = targets[s.get('{'+NS['r']+'}id')]
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join('xl', target))
            root = ET.fromstring(archive.read(target))
            require(not root.findall('.//s:f', NS), 'Formula found in data-only workbook')
            cells = {}
            types = {}
            for c in root.findall('.//s:sheetData/s:row/s:c', NS):
                t, v = c.get('t'), c.find('s:v', NS)
                if t == 's':
                    value = shared[int(v.text)]
                elif t == 'inlineStr':
                    value = ''.join(c.find('s:is', NS).itertext())
                elif t == 'str':
                    value = v.text if v is not None else ''
                elif v is None or v.text is None:
                    value = None
                elif t == 'b':
                    value = v.text == '1'
                elif t == 'e':
                    raise AssertionError('Spreadsheet error cell: '+c.get('r'))
                else:
                    # Reject silent fractional or exponential rendering of IDs/counts.
                    try:
                        value = int(v.text)
                    except ValueError as exc:
                        raise AssertionError('Unexpected non-integer numeric cell') from exc
                cells[c.get('r')] = value
                types[c.get('r')] = t
            tables = []
            sheet_rels = posixpath.join(posixpath.dirname(target), '_rels', posixpath.basename(target)+'.rels')
            if sheet_rels in archive.namelist():
                for r in ET.fromstring(archive.read(sheet_rels)):
                    if r.get('Type', '').endswith('/table'):
                        dest = r.get('Target')
                        dest = dest.lstrip('/') if dest.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(target), dest))
                        table = ET.fromstring(archive.read(dest))
                        tables.append({'ref': table.get('ref'), 'filter': table.find('s:autoFilter', NS) is not None})
            pane = root.find('.//s:pane', NS)
            sheets[s.get('name')] = {'cells': cells, 'types': types, 'tables': tables, 'xml': target,
                                     'pane': pane.attrib if pane is not None else {}}
    return sheets


def col(n):
    result = ''
    while n:
        n, r = divmod(n-1, 26)
        result = chr(65+r) + result
    return result


def records(sheet, width):
    cells = sheet['cells']
    present = sorted({int(''.join(c for c in ref if c.isdigit())) for ref, value in cells.items() if value is not None})
    require(present and present == list(range(1, max(present)+1)), 'Unexpected blank/missing row')
    return [[cells.get(f'{col(c)}{r}') for c in range(1, width+1)] for r in range(2, max(present)+1)]


def blank(value):
    return value is None or value == ''


def kind(value):
    if value is None: return 'NULL'
    if type(value) is str: return 'EMPTY_STRING' if value == '' else 'STRING'
    if type(value) is int: return 'INTEGER'
    if type(value) is list: return 'ARRAY' if value else 'EMPTY_ARRAY'
    if type(value) is dict: return 'OBJECT'
    raise AssertionError('Unsupported JSON type')


def field(obj, key):
    return kind(obj[key]) if key in obj else 'MISSING'


def walk(value, pointer='', parent='', key=''):
    yield [pointer, parent, str(key), kind(value), value]
    if type(value) is dict:
        for k, v in value.items():
            yield from walk(v, pointer+'/'+k.replace('~', '~0').replace('/', '~1'), pointer, k)
    if type(value) is list:
        for k, v in enumerate(value):
            yield from walk(v, pointer+'/'+str(k), pointer, k)


def same(actual, expected, detail):
    require(len(actual) == len(expected), detail+' row count')
    for r, (a, b) in enumerate(zip(actual, expected), 2):
        require(len(a) == len(b), detail+' column count')
        for c, (av, bv) in enumerate(zip(a, b), 1):
            if bv is None or bv == '':
                require(blank(av), f'{detail}!{col(c)}{r} should be blank')
            else:
                require(type(av) is type(bv) and av == bv, f'{detail}!{col(c)}{r} mismatch: {av!r} != {bv!r}')


def check(source, workbook):
    # JSON is independently decoded for comparison, never through the workbook builder.
    raw = source.read_bytes()
    data = json.loads(raw)
    sheets = read_xlsx(workbook)
    require(list(sheets) == ['Collections', 'Items', 'Labels', 'Source paths', 'Read me'], 'Sheet names/order')
    headers = {
        'Collections': ['Source order', 'Collection ID', 'Name', 'Note', 'Note state', 'Items state', 'Items count', 'Labels state', 'Labels count', 'Source pointer'],
        'Items': ['Parent order', 'Item order', 'Item ID', 'Name', 'Quantity', 'Quantity state', 'Note', 'Note state', 'Source pointer', 'Parent pointer'],
        'Labels': ['Parent order', 'Label order', 'Label', 'Source pointer', 'Parent pointer'],
        'Source paths': ['Node order', 'Source pointer', 'Parent pointer', 'Key/index', 'State', 'Scalar JSON', 'View cells']
    }
    for name, expected_headers in headers.items():
        require([sheets[name]['cells'].get(f'{col(i)}1') for i in range(1, len(expected_headers)+1)] == expected_headers, name+' headers')
        require(float(sheets[name]['pane'].get('ySplit', 0)) == 1, name+' frozen header')
        require(float(sheets[name]['pane'].get('xSplit', 0)) == (2 if name == 'Source paths' else 1), name+' frozen identifiers')
    expected = {'Collections': [], 'Items': [], 'Labels': []}
    absent = {}
    mapping = {}
    for p, parent in enumerate(data['collections']):
        ptr = f'/collections/{p}'
        row = p + 2
        mapping[ptr] = f'Collections!A{row}:J{row}'
        for f, c in [('id', 'B'), ('name', 'C'), ('note', 'D'), ('items', 'F'), ('labels', 'H')]:
            mapping[ptr+'/'+f] = f'Collections!{c}{row}'
        expected['Collections'].append([p, parent['id'], parent['name'], parent.get('note'), field(parent, 'note'),
                                        field(parent, 'items'), len(parent['items']) if type(parent.get('items')) is list else None,
                                        field(parent, 'labels'), len(parent['labels']) if type(parent.get('labels')) is list else None, ptr])
        for f in ['note', 'items', 'labels']:
            if f not in parent: absent[ptr+'/'+f] = (ptr, f)
        for i, item in enumerate(parent.get('items') or []):
            iptr = f'{ptr}/items/{i}'
            row = len(expected['Items']) + 2
            mapping[iptr] = f'Items!A{row}:J{row}'
            for f, c in [('id', 'C'), ('name', 'D'), ('quantity', 'E'), ('note', 'G')]:
                mapping[iptr+'/'+f] = f'Items!{c}{row}'
            expected['Items'].append([p, i, item['id'], item['name'], item.get('quantity'), field(item, 'quantity'),
                                      item.get('note'), field(item, 'note'), iptr, ptr])
            for f in ['note', 'quantity']:
                if f not in item: absent[iptr+'/'+f] = (iptr, f)
        for i, label in enumerate(parent.get('labels') or []):
            mapping[f'{ptr}/labels/{i}'] = f"Labels!C{len(expected['Labels'])+2}"
            expected['Labels'].append([p, i, label, f'{ptr}/labels/{i}', ptr])
    for name, width in [('Collections', 10), ('Items', 10), ('Labels', 5)]:
        same(records(sheets[name], width), expected[name], name)
        require(sheets[name]['tables'] == [{'ref': f'A1:{col(width)}{len(expected[name])+1}', 'filter': True}], name+' filter/table range')
        require(sheets[name]['pane'], name+' freeze pane')
    nodes = records(sheets['Source paths'], 7)
    actual = [r for r in nodes if r[4] != 'MISSING']
    missing = [r for r in nodes if r[4] == 'MISSING']
    source_nodes = list(walk(data))
    require(len(actual) == len(source_nodes), 'Source node count')
    rebuilt = {}
    for ordinal, (row, original) in enumerate(zip(actual, source_nodes)):
        number, ptr, parent, key, state, token, target = row
        ptr, parent, key = ptr or '', parent or '', key or ''
        require((target or None) == mapping.get(ptr), 'Source-to-view mapping mismatch')
        optr, oparent, okey, ostate, original_value = original
        require(number == ordinal and (ptr, parent, key, state) == (optr, oparent, okey, ostate), 'Source pointer/order/state mismatch')
        if state == 'OBJECT': restored = {}
        elif state in ('ARRAY', 'EMPTY_ARRAY'): restored = []
        else:
            require(token == json.dumps(original_value, ensure_ascii=False, separators=(',', ':')), 'Scalar token mismatch')
            restored = json.loads(token)
            require(type(restored) is type(original_value) and restored == original_value, 'Scalar value mismatch')
        if state in ('OBJECT', 'ARRAY', 'EMPTY_ARRAY'):
            require(blank(token), 'Container has an invented scalar')
        rebuilt[ptr] = restored
        if ptr:
            owner = rebuilt[parent]
            if type(owner) is list:
                require(int(key) == len(owner), 'Array order mismatch')
                owner.append(restored)
            else:
                owner[key] = restored
        if not blank(target):
            name, address = target.split('!')
            require(name in sheets, 'Invalid mapping sheet')
            start = address.split(':')[0]
            require(start in sheets[name]['cells'], 'Invalid mapped cell')
            if state in ('STRING', 'INTEGER', 'EMPTY_STRING', 'NULL') and '/' in ptr:
                actual_cell = sheets[name]['cells'][start]
                if ptr.endswith(('/items', '/labels')):
                    require(actual_cell == state, 'Relationship state mapping')
                else:
                    require((blank(actual_cell) and blank(restored)) or actual_cell == restored, 'Mapped value mismatch')
    require(rebuilt[''] == data, 'Reconstructed JSON differs')
    require([(p, k, t) for p, _, k, t, _ in walk(rebuilt[''])] == [(p, k, t) for p, _, k, t, _ in source_nodes], 'Object/array order differs')
    require({r[1]: (r[2], r[3]) for r in missing} == absent and len(missing) == len(absent), 'Missing field coverage')
    require(all(r[6] == mapping[r[1]] for r in missing), 'Missing field mapping mismatch')
    require(all(blank(r[0]) and blank(r[5]) for r in missing), 'Missing observation has invented value/order')
    require(len({r[1] or '' for r in nodes}) == len(nodes), 'Duplicate source pointer')
    require(sheets['Source paths']['tables'] == [{'ref': f'A1:G{len(nodes)+1}', 'filter': True}] and sheets['Source paths']['pane'], 'Source path table/filter/pane')
    regions = {'Collections': (len(expected['Collections'])+1, 10),
               'Items': (len(expected['Items'])+1, 10),
               'Labels': (len(expected['Labels'])+1, 5),
               'Source paths': (len(source_nodes)+len(absent)+1, 7),
               'Read me': (16, 2)}
    for name, (height, width) in regions.items():
        allowed = {f'{col(c)}{r}' for r in range(1, height+1) for c in range(1, width+1)}
        require(all(ref in allowed or blank(value) for ref, value in sheets[name]['cells'].items()),
                name+' has content outside its declared review area')
    metadata = sheets['Read me']['cells']
    require(metadata.get('B2') == source.name and metadata.get('B3') == len(raw) and metadata.get('B4') == hashlib.sha256(raw).hexdigest(), 'Source metadata mismatch')
    require(metadata.get('B7') == json.dumps(data['exportedAt']), 'Timestamp inferred/changed')
    return {'source': {'file': source.name, **digest(source)}, 'workbook': {'file': workbook.name, **digest(workbook)},
            'counts': {**{name.lower(): len(rows) for name, rows in expected.items()}, 'actual_source_nodes': len(actual), 'missing_schema_fields': len(missing)},
            'checks': ['all source node paths, states, values and order reconstructed', 'parent/child rows and sibling arrays reconciled',
                       'identifiers and date-like strings retained as text', 'zero/null/empty/missing distinctions retained',
                       'no formulas, external relationships, macros or spreadsheet errors', 'tables, filter ranges and frozen panes checked', 'source identity metadata matched']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('workbook', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check(args.source, args.workbook)
    if args.report:
        with args.report.open('x', encoding='utf-8') as file:
            json.dump(result, file, indent=2)
            file.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
