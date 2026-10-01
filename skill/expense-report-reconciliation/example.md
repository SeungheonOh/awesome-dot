# Fictional exhibit-demo expense reconciliation

All records, policy clauses and business activity below are invented. The fixture uses text transcriptions, not receipt images. It neither contacts a provider nor submits a claim.

## Request and supplied rules

“Prepare a new CSV expense report for the Lumen prototype demonstration and save it privately. Use these receipts, posted-card records and policy. I took the rail journey, ate the listed meal alone during the demonstration visit, and bought the display materials for that project. I have not supplied a purpose for the taxi. Do not submit anything.”

Fictional policy P1, applicable to these transactions:

- R1: documented demonstration transit and display materials are eligible at gross cost
- R2: one claimant's documented business meal is capped at EUR 25.00 gross; alcohol is excluded
- R3: itemized personal and cap-excess amounts are excluded; unknown business purpose stays unresolved
- R4: report in EUR, using evidenced posted-card amounts for foreign charges and credits. Round report allocations to cents with decimal half-up rounding. This fixture requires no fractional-cent split
- R5: exact copies add no expense. A credit reverses the identifiable refunded item allocation; include posted credits even when their conversion differs from the purchase
- R6: tax is retained as source information; this gross-cost report makes no recoverability or deductibility claim

Card evidence C1 shows EUR 54.00 posted for the USD 60.00 materials purchase; C2 shows EUR -17.90 posted for the USD -20.00 item credit. Each card record corroborates its transaction and adds zero extra expense. Purpose statement U1 is the quoted user account above. Policy P1 and U1 are retained as non-monetary rule/purpose evidence.

## Original transaction records

| Source | Date | Evidence | Original gross | Source tax | Reporting amount |
| --- | --- | --- | ---: | ---: | ---: |
| S1 | 2026-09-18 | Rail RT-101, net 40.00 + tax 8.00 | EUR 48.00 | EUR 8.00 | EUR 48.00 |
| S2 | 2026-09-18 | Byte-identical copy of S1 | EUR 48.00 | EUR 8.00 | Zero incremental amount |
| S3 | 2026-09-18 | Meal ML-209: food 30.00 including tax 5.00; wine 12.00 including tax 2.00 | EUR 42.00 | EUR 7.00 | EUR 42.00 |
| S4 | 2026-09-17 | Materials MT-310: net 54.00 + tax 6.00; C1 posted amount | USD 60.00 | USD 6.00 | EUR 54.00 |
| S5 | 2026-09-20 | Credit CR-311 for one returned MT-310 material item: net -18.00 + tax -2.00; C2 posted amount | USD -20.00 | USD -2.00 | EUR -17.90 |
| S6 | 2026-09-21 | Taxi TX-412; purpose absent; tax not stated | EUR 18.00 | Unknown | EUR 18.00 |

The unique EUR receipts total 108.00; the unique USD purchase and credit net to 40.00. Do not add 108.00 and 40.00 as a monetary total. S2 remains preserved and excluded as duplicate evidence. The expense report retains S3's tax once in its source register; it does not invent a tax split for the capped EUR 25.00 allowance.

## Expected saved allocation detail

| Line | Source | Disposition | Original allocation | EUR allocation | Basis |
| --- | --- | --- | ---: | ---: | --- |
| L1 | S1, corroborated by S2 | Allowed | EUR 48.00 | 48.00 | U1 + P1/R1; S2 adds zero |
| L2 | S3 | Allowed | EUR 25.00 | 25.00 | U1 + P1/R2 |
| L3 | S3 | Disallowed | EUR 5.00 | 5.00 | P1/R2 meal cap excess |
| L4 | S3 | Disallowed | EUR 12.00 | 12.00 | P1/R2 alcohol |
| L5 | S4 + C1 | Allowed | USD 60.00 | 54.00 | U1 + P1/R1/R4 |
| L6 | S5 + C2 | Allowed, negative adjustment | USD -20.00 | -17.90 | S4 item link + P1/R4/R5 |
| L7 | S6 | Unresolved | EUR 18.00 | 18.00 | P1/R3; purpose absent |

Reporting reconciliation: 144.10 = 109.10 allowed + 17.00 disallowed + 18.00 unresolved. The proposed supported claim subtotal is EUR 109.10; the taxi is excluded from it pending purpose evidence. This is a saved private draft, with no submission or approval claim.

## Repeatable local check

Run this Python 3 block in any empty working directory. It uses only the standard library, creates a temporary allocation CSV and a companion JSON report, reopens both, then removes the temporary directory. The JSON preserves all ten synthetic source texts and digests, source metadata/tax, monetary-source mappings, policy and purpose evidence, transaction relationships, exceptions and reconciled totals. All originals start as synthetic in-memory evidence; the saved companion makes the report independently inspectable while the temporary destination exists. The exact duplicate and every original evidence digest are checked, including C1, C2, U1 and P1; no real files are modified.

```python
import csv
import hashlib
import json
import tempfile
from collections import Counter, defaultdict
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

raw = {
    'S1': 'RT-101|2026-09-18|EUR|net=40.00|tax=8.00|gross=48.00',
    'S2': 'RT-101|2026-09-18|EUR|net=40.00|tax=8.00|gross=48.00',
    'S3': 'ML-209|2026-09-18|EUR|food=30.00,tax=5.00|wine=12.00,tax=2.00',
    'S4': 'MT-310|2026-09-17|USD|net=54.00|tax=6.00|gross=60.00',
    'S5': 'CR-311|2026-09-20|USD|MT-310 item refund|net=-18.00|tax=-2.00|gross=-20.00',
    'S6': 'TX-412|2026-09-21|EUR|gross=18.00|tax not stated',
    'C1': 'posted|MT-310|EUR|54.00',
    'C2': 'posted|CR-311|EUR|-17.90',
    'U1': 'Prepare a new CSV expense report for the Lumen prototype demonstration and save it privately. Use these receipts, posted-card records and policy. I took the rail journey, ate the listed meal alone during the demonstration visit, and bought the display materials for that project. I have not supplied a purpose for the taxi. Do not submit anything.',
    'P1': '\n'.join([
        'R1: documented demonstration transit and display materials are eligible at gross cost',
        "R2: one claimant's documented business meal is capped at EUR 25.00 gross; alcohol is excluded",
        'R3: itemized personal and cap-excess amounts are excluded; unknown business purpose stays unresolved',
        'R4: report in EUR, using evidenced posted-card amounts for foreign charges and credits. Round report allocations to cents with decimal half-up rounding. This fixture requires no fractional-cent split',
        'R5: exact copies add no expense. A credit reverses the identifiable refunded item allocation; include posted credits even when their conversion differs from the purchase',
        'R6: tax is retained as source information; this gross-cost report makes no recoverability or deductibility claim',
    ]),
}

def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()

hashes = {key: digest(value) for key, value in raw.items()}
# Values below transcribe the fictional table; this is not a receipt parser.
transactions = {
    'T1': ('EUR', D('48.00'), D('48.00')),
    'T2': ('EUR', D('42.00'), D('42.00')),
    'T3': ('USD', D('60.00'), D('54.00')),
    'T4': ('USD', D('-20.00'), D('-17.90')),
    'T5': ('EUR', D('18.00'), D('18.00')),
}
header = ['line', 'transaction', 'sources', 'status', 'currency', 'original', 'eur', 'basis']
rows = [
    ['L1', 'T1', 'S1;S2', 'allowed', 'EUR', '48.00', '48.00', 'U1;P1/R1'],
    ['L2', 'T2', 'S3', 'allowed', 'EUR', '25.00', '25.00', 'U1;P1/R2'],
    ['L3', 'T2', 'S3', 'disallowed', 'EUR', '5.00', '5.00', 'P1/R2 cap'],
    ['L4', 'T2', 'S3', 'disallowed', 'EUR', '12.00', '12.00', 'P1/R2 alcohol'],
    ['L5', 'T3', 'S4;C1', 'allowed', 'USD', '60.00', '54.00', 'U1;P1/R1/R4'],
    ['L6', 'T4', 'S5;C2', 'allowed', 'USD', '-20.00', '-17.90', 'T3 item;P1/R4/R5'],
    ['L7', 'T5', 'S6', 'unresolved', 'EUR', '18.00', '18.00', 'P1/R3 purpose missing'],
]
coverage = {
    'S1': ('allowed', ['L1']), 'S2': ('disallowed duplicate, incremental 0', ['L1']),
    'S3': ('allowed/disallowed split', ['L2', 'L3', 'L4']),
    'S4': ('allowed', ['L5']), 'S5': ('allowed negative', ['L6']),
    'S6': ('unresolved', ['L7']), 'C1': ('allowed corroboration, incremental 0', ['L5']),
    'C2': ('allowed corroboration, incremental 0', ['L6']),
}
assert hashes['S1'] == hashes['S2']
assert set(raw) == set(coverage) | {'P1', 'U1'}
assert D('40.00') + D('8.00') == transactions['T1'][1]
assert D('30.00') + D('12.00') == transactions['T2'][1]
assert D('54.00') + D('6.00') == transactions['T3'][1]
assert D('-18.00') + D('-2.00') == transactions['T4'][1]
assert D('5.00') + D('2.00') == D('7.00')  # source tax once
assert D(rows[1][6]) == min(D('30.00'), D('25.00'))
assert D(rows[2][6]) == max(D('30.00') - D('25.00'), D('0'))


def validate(saved):
    assert len(saved) == 7 and len({r['line'] for r in saved}) == 7
    assert Counter(r['transaction'] for r in saved) == Counter({'T1': 1, 'T2': 3, 'T3': 1, 'T4': 1, 'T5': 1})
    for key, (currency, original, eur) in transactions.items():
        group = [r for r in saved if r['transaction'] == key]
        assert all(r['currency'] == currency for r in group)
        assert sum(D(r['original']) for r in group) == original
        assert sum(D(r['eur']) for r in group) == eur
    for source, (_, lines) in coverage.items():
        assert set(lines) == {r['line'] for r in saved if source in r['sources'].split(';')}
    original_totals = defaultdict(lambda: D('0'))
    for currency, amount, _ in transactions.values():
        original_totals[currency] += amount
    assert dict(original_totals) == {'EUR': D('108.00'), 'USD': D('40.00')}
    totals = {s: sum(D(r['eur']) for r in saved if r['status'] == s)
              for s in ('allowed', 'disallowed', 'unresolved')}
    assert totals == {'allowed': D('109.10'), 'disallowed': D('17.00'), 'unresolved': D('18.00')}
    assert sum(totals.values()) == sum(t[2] for t in transactions.values()) == D('144.10')
    assert all(D(r['eur']) == D(r['eur']).quantize(D('.01'), rounding=ROUND_HALF_UP) for r in saved)
    assert next(r for r in saved if r['line'] == 'L7')['status'] == 'unresolved'
    assert next(r for r in saved if r['line'] == 'L6')['eur'] == '-17.90'
    assert D(raw['C1'].split('|')[-1]) == transactions['T3'][2]
    assert D(raw['C2'].split('|')[-1]) == transactions['T4'][2]
    return {key: str(value) for key, value in totals.items()}

# Metadata is an explicit transcription of the source table, not inferred OCR.
source_details = {
    'S1': {'date': '2026-09-18', 'document_id': 'RT-101', 'currency': 'EUR', 'gross': '48.00', 'tax': '8.00', 'tax_status': 'stated'},
    'S2': {'date': '2026-09-18', 'document_id': 'RT-101', 'currency': 'EUR', 'gross': '48.00', 'tax': '8.00', 'tax_status': 'stated', 'duplicate_of': 'S1'},
    'S3': {'date': '2026-09-18', 'document_id': 'ML-209', 'currency': 'EUR', 'gross': '42.00', 'tax': '7.00', 'tax_status': 'stated',
           'items': [{'item': 'food', 'gross': '30.00', 'tax': '5.00'}, {'item': 'wine', 'gross': '12.00', 'tax': '2.00'}]},
    'S4': {'date': '2026-09-17', 'document_id': 'MT-310', 'currency': 'USD', 'gross': '60.00', 'tax': '6.00', 'tax_status': 'stated', 'posted_evidence': 'C1'},
    'S5': {'date': '2026-09-20', 'document_id': 'CR-311', 'currency': 'USD', 'gross': '-20.00', 'tax': '-2.00', 'tax_status': 'stated', 'credit_for': 'S4', 'posted_evidence': 'C2'},
    'S6': {'date': '2026-09-21', 'document_id': 'TX-412', 'currency': 'EUR', 'gross': '18.00', 'tax': None, 'tax_status': 'not stated'},
    'C1': {'document_id': 'MT-310', 'currency': 'EUR', 'posted': '54.00', 'supports': 'S4', 'incremental_expense': '0.00'},
    'C2': {'document_id': 'CR-311', 'currency': 'EUR', 'posted': '-17.90', 'supports': 'S5', 'incremental_expense': '0.00'},
    'U1': {'role': 'user purpose statement and preparation-only authority'},
    'P1': {'role': 'supplied fictional policy'},
}
source_mapping = {key: {'disposition': status, 'lines': lines}
                  for key, (status, lines) in coverage.items()}
transaction_record = {
    key: {'currency': currency, 'original': str(amount), 'eur': str(eur),
          'purpose_status': 'missing' if key == 'T5' else 'documented by user',
          'purpose_source': None if key == 'T5' else 'U1'}
    for key, (currency, amount, eur) in transactions.items()
}
transaction_record['T4']['credit_for'] = 'T3'
exceptions = [{'line': 'L7', 'source': 'S6', 'eur': '18.00',
               'reason': 'Business purpose not supplied; excluded from supported claim pending evidence'}]


def validate_companion(packet, saved, csv_bytes):
    assert packet['status'] == 'private draft; not submitted'
    assert packet['report_currency'] == 'EUR'
    assert packet['allocation_artifact'] == {
        'filename': 'private-expense-draft.csv',
        'sha256': hashlib.sha256(csv_bytes).hexdigest(),
    }
    assert set(packet['sources']) == set(raw)
    for key, entry in packet['sources'].items():
        assert entry['raw_evidence'] == raw[key]
        assert entry['sha256'] == digest(entry['raw_evidence']) == hashes[key]
        assert entry['metadata'] == source_details[key]
    assert packet['source_mapping'] == source_mapping
    assert packet['transactions'] == transaction_record
    assert packet['exceptions'] == exceptions
    summary = packet['reconciliation']
    assert summary['eur_dispositions'] == validate(saved)
    assert summary['original_currency_net'] == {'EUR': '108.00', 'USD': '40.00'}
    assert D(summary['reporting_net']) == sum(D(t['eur']) for t in packet['transactions'].values()) == D('144.10')
    assert D(summary['supported_claim']) == D(summary['eur_dispositions']['allowed']) == D('109.10')
    assert D(summary['reporting_net']) == sum(D(v) for v in summary['eur_dispositions'].values())
    # Check tax preservation, unknown-vs-zero and evidence linkage from readback.
    sources = packet['sources']
    meal = sources['S3']['metadata']
    assert D(meal['tax']) == sum(D(item['tax']) for item in meal['items']) == D('7.00')
    assert D(meal['gross']) == sum(D(item['gross']) for item in meal['items']) == D('42.00')
    assert sources['S6']['metadata']['tax'] is None
    assert sources['S6']['metadata']['tax_status'] == 'not stated'
    assert packet['transactions']['T5']['purpose_source'] is None
    assert packet['transactions']['T5']['purpose_status'] == 'missing'
    for key in ('S1', 'S2', 'S3', 'S4', 'S5', 'S6'):
        metadata = sources[key]['metadata']
        assert metadata['document_id'] in sources[key]['raw_evidence']
        assert metadata['date'] in sources[key]['raw_evidence']
    assert sources['S1']['sha256'] == sources['S2']['sha256']
    assert sources['S5']['metadata']['credit_for'] == 'S4'
    assert sources['C2']['metadata']['posted'] == packet['transactions']['T4']['eur'] == '-17.90'
    assert 'Do not submit anything.' in sources['U1']['raw_evidence']
    assert len(sources['P1']['raw_evidence'].splitlines()) == 6
    return True

with tempfile.TemporaryDirectory() as directory:
    output = Path(directory) / 'private-expense-draft.csv'
    with output.open('w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)
    with output.open(newline='') as handle:
        saved = list(csv.DictReader(handle))
    totals = validate(saved)
    report = {
        'status': 'private draft; not submitted', 'report_currency': 'EUR',
        'allocation_artifact': {'filename': output.name, 'sha256': hashlib.sha256(output.read_bytes()).hexdigest()},
        'sources': {key: {'raw_evidence': value, 'sha256': hashes[key], 'metadata': source_details[key]}
                    for key, value in raw.items()},
        'source_mapping': source_mapping, 'transactions': transaction_record, 'exceptions': exceptions,
        'reconciliation': {'original_currency_net': {'EUR': '108.00', 'USD': '40.00'},
                           'reporting_net': '144.10', 'eur_dispositions': totals, 'supported_claim': '109.10'},
    }
    companion = Path(directory) / 'private-expense-draft-report.json'
    companion.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    reopened = json.loads(companion.read_text(encoding='utf-8'))
    assert validate_companion(reopened, saved, output.read_bytes())
    # A changed credit sign and a changed unresolved amount must fail.
    for line_id, column, bad_value in [('L6', 'eur', '17.90'), ('L7', 'eur', '0.00')]:
        changed = [dict(row) for row in saved]
        next(row for row in changed if row['line'] == line_id)[column] = bad_value
        try:
            validate(changed)
        except AssertionError:
            pass
        else:
            raise AssertionError('corrupted fixture was accepted')
    # Persist and reopen each corrupted companion to test saved-artifact validation.
    corruptions = [
        (['sources', 'S3', 'metadata', 'tax'], None),
        (['sources', 'S1', 'metadata', 'date'], '2026-09-19'),
        (['sources', 'U1', 'raw_evidence'], 'Taxi was for the project.'),
        (['reconciliation', 'supported_claim'], '127.10'),
        (['source_mapping', 'S2', 'lines'], []),
        (['transactions', 'T5', 'purpose_source'], 'U1'),
        (['transactions', 'T4', 'eur'], '-18.00'),
    ]
    corrupt_path = Path(directory) / 'corrupt-companion.json'
    for path, bad_value in corruptions:
        changed = json.loads(companion.read_text(encoding='utf-8'))
        target = changed
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = bad_value
        corrupt_path.write_text(json.dumps(changed), encoding='utf-8')
        try:
            validate_companion(json.loads(corrupt_path.read_text(encoding='utf-8')), saved, output.read_bytes())
        except AssertionError:
            pass
        else:
            raise AssertionError('corrupted companion was accepted: ' + '.'.join(path))
    assert validate_companion(json.loads(companion.read_text(encoding='utf-8')), saved, output.read_bytes())
assert all(digest(raw[key]) == value for key, value in hashes.items())
print(json.dumps({'eur_totals': totals, 'originals_unchanged': len(hashes),
                  'source_coverage': len(coverage), 'status': 'private draft; not submitted'}, sort_keys=True))
print('PASS: CSV and complete companion JSON readback; source texts/digests, dates/IDs, tax, purpose/policy, coverage, signed credit and reconciliation preserved')
print('PASS: two allocation corruptions and seven saved companion corruptions rejected; original report remains valid')
```

Observed on 2026-10-01 in the repository’s Linux environment with Python 3.12.14: exit status 0, ten original evidence digests unchanged, eight monetary-source mappings, seven allocation lines, the stated three EUR disposition totals, and both PASS lines. CSV and companion JSON readbacks preserve the original policy/purpose texts, receipt identifiers/dates, S3 tax and itemization, S6 unknown tax/purpose, linked credit, coverage and reconciled summary. Two allocation corruptions and seven saved-and-reopened companion corruptions were rejected; the original saved report remained valid. Both outputs and corrupted test copies were confined to the temporary fixture destination and removed when the check ended; no persistent expense report or external submission was created.

This fixture does not demonstrate OCR, native workbook preservation, a live expense portal, actual exchange-rate retrieval, tax review or employer approval. The check validates a declared allocation against independent fixture amounts; it is not a general policy-classification engine.
