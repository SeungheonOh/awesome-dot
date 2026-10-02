#!/usr/bin/env python3
"""Independent UTF-8 / JSON-member preflight, using only Python's standard library.
Reads fixtures; writes nothing. It deliberately does not duplicate the JS schema.
"""
import json
from pathlib import Path


def unique_members(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f'duplicate JSON member: {key}')
        value[key] = item
    return value


def load(raw):
    return json.loads(raw.decode('utf-8', errors='strict'),
                      object_pairs_hook=unique_members,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f'non-JSON constant: {x}')))


base = Path(__file__).resolve().parent
for name in ('source.en-US.json', 'target.fr-FR.json', 'contract.json'):
    load((base / name).read_bytes())
for malformed in (b'{"name":1,"name":2}', b'{"x":"\\q"}', b'{"x":NaN}', b'{"x":"\xff"}'):
    try:
        load(malformed)
    except (ValueError, UnicodeError):
        continue
    raise AssertionError('malformed control unexpectedly accepted')
print('PASS: 3 saved UTF-8 JSON files; duplicate-member, malformed-escape, non-JSON-number and invalid-UTF-8 controls rejected; no writes.')
