"""Fixed JSON test format. This module never loads candidate code."""
from bounded_json import exact, bounded_text, reject


def validate(payload):
    exact(payload, ('version', 'cases'))
    if type(payload['version']) is not int or payload['version'] != 1:
        reject('unsupported version')
    cases = payload['cases']
    if type(cases) is not list or not 1 <= len(cases) <= 24:
        reject('require 1..24 cases')
    ids = set()
    for case in cases:
        exact(case, ('id', 'entry_point', 'records', 'expected'))
        bounded_text(case['id'], 48)
        if case['id'] in ids: reject('duplicate case id')
        ids.add(case['id'])
        if case['entry_point'] not in ('export_rows', 'download_selected'):
            reject('unknown public entry point')
        rows = case['records']
        if type(rows) is not list or len(rows) > 32: reject('record bound exceeded')
        for row in rows:
            if type(row) is not dict or not {'code', 'selected'} <= set(row) or not set(row) <= {'code', 'selected', 'units'}:
                reject('invalid record keys')
            bounded_text(row['code'], 32)
            if type(row['selected']) is not bool: reject('selected must be boolean')
            if 'units' in row and row['units'] is not None and (type(row['units']) is not int or not -1000 <= row['units'] <= 1000):
                reject('invalid units')
        exact(case['expected'], ('items',))
        items = case['expected']['items']
        if type(items) is not list or len(items) > 32: reject('expected items must be bounded list')
        for item in items:
            exact(item, ('code', 'units'))
            bounded_text(item['code'], 32)
            if item['units'] is not None and (type(item['units']) is not int or not -1000 <= item['units'] <= 1000):
                reject('invalid expected units')
    return cases
