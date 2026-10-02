#!/usr/bin/env python3
"""Reassemble reviewed snapshot components. Offline, deliberately narrow profile."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from hashlib import sha256
from importlib.metadata import version
import io
import json
from pathlib import Path
import platform
import sys

try:
    from icalendar import Calendar
    from dateutil.rrule import rrulestr
    from dateutil.tz import datetime_ambiguous, datetime_exists, tzical
except ImportError as exc:
    raise SystemExit('Needs icalendar and python-dateutil; see example.md. No files written.') from exc

ALLOWED = {'UID', 'SEQUENCE', 'DTSTAMP', 'DTSTART', 'DTEND', 'SUMMARY',
           'DESCRIPTION', 'LOCATION', 'STATUS', 'RRULE', 'RDATE', 'EXDATE',
           'RECURRENCE-ID', 'X-EXAMPLE-COLOR'}
UTC = timezone.utc


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def one(component, name, required=False):
    value = component.get(name)
    demand(not isinstance(value, list), f'Repeated singleton {name}')
    demand(value is not None or not required, f'Missing {name}')
    return value


def raw(value):
    if isinstance(value, list):
        return [raw(item) for item in value]
    return value.to_ical().decode('utf-8')


def params(value):
    return {str(k): str(v) for k, v in sorted(value.params.items())}


def prop(value):
    return {'value': raw(value), 'parameters': params(value)}


def properties(event):
    return {name: [prop(v) for v in (value if isinstance(value, list) else [value])]
            for name, value in sorted(event.items())}


def identity(event):
    rid = one(event, 'RECURRENCE-ID')
    return (str(one(event, 'UID', True)),
            json.dumps(prop(rid), sort_keys=True) if rid is not None else 'MASTER')


def canonical(event):
    return event.to_ical(sorted=True)


def form(value):
    item = value.dt
    if type(item) is date:
        demand(value.params.get('VALUE') == 'DATE' and 'TZID' not in value.params,
               'DATE needs VALUE=DATE and no TZID')
        return ('DATE', '')
    demand(isinstance(item, datetime), 'Only DATE or DATE-TIME supported')
    if value.params.get('TZID'):
        return ('TZID', str(value.params['TZID']))
    if raw(value).endswith('Z'):
        return ('UTC', '')
    return ('FLOATING', '')


def instant(value, zones):
    kind, name = form(value)
    demand(kind != 'FLOATING', 'Floating time needs an explicit transfer decision')
    if kind == 'DATE':
        return value.dt
    if kind == 'UTC':
        demand(value.dt.tzinfo is not None, 'UTC value parsed without a zone')
        return value.dt.astimezone(UTC)
    demand(name in zones, f'Missing embedded VTIMEZONE for {name}')
    demand(date(2026, 1, 1) <= value.dt.date() < date(2027, 1, 1),
           'The worked VTIMEZONE coverage is limited to calendar year 2026')
    local = value.dt.replace(tzinfo=None).replace(tzinfo=zones[name])
    demand(datetime_exists(local) and not datetime_ambiguous(local),
           'Skipped or repeated local time needs an explicit interpretation')
    demand(value.dt.utcoffset() == local.utcoffset(),
           'Parser and embedded VTIMEZONE disagree')
    return local


def date_list(event, name, zones):
    entries = event.get(name, [])
    if not isinstance(entries, list):
        entries = [entries]
    result = []
    for entry in entries:
        for value in entry.dts:
            # date-list parameters apply to every value in the property.
            value = deepcopy(value)
            value.params.update(entry.params)
            demand(form(value) == form(event['DTSTART']), f'{name} form differs from DTSTART')
            result.append(instant(value, zones))
    return result


def validate(event, zones):
    demand(not event.subcomponents, 'Nested components such as alarms are outside this profile')
    demand(set(event) <= ALLOWED, f'Unsupported properties: {sorted(set(event) - ALLOWED)}')
    for name in set(event) - {'RDATE', 'EXDATE'}:
        one(event, name)
    for name in ('UID', 'SEQUENCE', 'DTSTAMP', 'DTSTART', 'DTEND'):
        one(event, name, True)
    demand(int(event['SEQUENCE']) >= 0, 'Negative SEQUENCE')
    demand(form(event['DTSTAMP']) == ('UTC', ''), 'DTSTAMP must be UTC')
    demand(str(event.get('STATUS', 'CONFIRMED')) in {'CONFIRMED', 'TENTATIVE'},
           'Cancellation is held; it is not an instruction to restore an older event')
    start, end = event['DTSTART'], event['DTEND']
    demand(form(start) == form(end), 'DTSTART and DTEND forms differ')
    a, b = instant(start, zones), instant(end, zones)
    demand(b > a, 'DTEND must be after DTSTART')
    rid = event.get('RECURRENCE-ID')
    if rid is not None:
        demand(not rid.params.get('RANGE'), 'RANGE changes are outside this profile')
        demand(form(rid) == form(start), 'RECURRENCE-ID form differs from DTSTART')
        instant(rid, zones)
        demand(not any(n in event for n in ('RRULE', 'RDATE', 'EXDATE')),
               'Override recurrence rules are outside this profile')
    rule = event.get('RRULE')
    if rule is not None:
        demand(isinstance(a, datetime), 'Recurring DATE events are outside this profile')
        demand(set(rule) == {'FREQ', 'COUNT'} and rule['FREQ'] == ['WEEKLY'],
               'Only FREQ=WEEKLY;COUNT=n is supported by this projection')
        demand(len(rule['COUNT']) == 1 and 1 <= int(rule['COUNT'][0]) <= 100,
               'COUNT must be between 1 and 100')
    elif rid is None:
        demand(not any(n in event for n in ('RDATE', 'EXDATE')),
               'RDATE/EXDATE without a weekly master is outside this profile')
    date_list(event, 'RDATE', zones)
    date_list(event, 'EXDATE', zones)
    return a, b


def project(events, zones):
    """Finite weekly projection, not a full iCalendar recurrence implementation."""
    by_uid = defaultdict(list)
    for event in events:
        validate(event, zones)
        by_uid[str(event['UID'])].append(event)
    rows = []
    for uid, group in sorted(by_uid.items()):
        masters = [e for e in group if 'RECURRENCE-ID' not in e]
        demand(len(masters) == 1, 'Every included UID needs exactly one master')
        master = masters[0]
        start, end = validate(master, zones)
        overrides = [e for e in group if 'RECURRENCE-ID' in e]
        demand(not overrides or 'RRULE' in master, 'Detached override has no recurring master')
        if 'RRULE' not in master:
            starts = {start}
        else:
            starts = set(rrulestr(raw(master['RRULE']), dtstart=start))
            starts.update(date_list(master, 'RDATE', zones))
            starts.difference_update(date_list(master, 'EXDATE', zones))
        replacement = {}
        for override in overrides:
            rid = instant(override['RECURRENCE-ID'], zones)
            demand(form(override['RECURRENCE-ID']) == form(master['DTSTART']),
                   'Override identity form differs from master')
            demand(rid in starts, 'Override does not identify an included original occurrence')
            demand(rid not in replacement, 'Two overrides target one occurrence')
            replacement[rid] = override
        # This profile verifies one-hour events only for recurring instants.
        # It does not choose elapsed versus wall duration across a transition.
        if 'RRULE' in master:
            demand(end - start == timedelta(hours=1), 'Recurring duration must be one hour')
        for occurrence in sorted(starts):
            chosen = replacement.get(occurrence, master)
            if chosen is master:
                actual_start, actual_end = occurrence, occurrence + (end - start)
            else:
                actual_start, actual_end = validate(chosen, zones)
            row = {'uid': uid, 'original_occurrence': occurrence.isoformat(),
                   'start': actual_start.isoformat(), 'end_exclusive': actual_end.isoformat(),
                   'overridden': chosen is not master}
            if isinstance(actual_start, datetime):
                if form(master['DTSTART'])[0] == 'TZID':
                    demand(actual_start.year == actual_end.year == 2026,
                           'Projected occurrence exceeds worked VTIMEZONE coverage')
                demand(datetime_exists(actual_start) and not datetime_ambiguous(actual_start)
                       and datetime_exists(actual_end) and not datetime_ambiguous(actual_end),
                       'Projected occurrence crosses an unresolved local time')
                demand(actual_start.utcoffset() == actual_end.utcoffset(),
                       'Occurrence spanning an offset transition is outside this profile')
                row['start_utc'] = actual_start.astimezone(UTC).isoformat()
                row['end_utc'] = actual_end.astimezone(UTC).isoformat()
            else:
                row['calendar_days'] = (actual_end - actual_start).days
            rows.append(row)
    return rows


def run(fixtures, output):
    plan = json.loads((fixtures / 'selection.json').read_text())
    demand(plan['contract'] == 'offline-event-snapshot-v1', 'Unknown contract')
    demand(not output.exists(), 'Use a new output directory; existing files are never overwritten')
    evidence = plan['evidence_file']
    demand(Path(evidence).name == evidence, 'Evidence must be a filename inside fixtures')
    demand(sha256((fixtures / evidence).read_bytes()).hexdigest() == plan['evidence_sha256'],
           'Selection evidence changed; review the decisions again')
    records, tz_components, zones = [], {}, {}
    for filename, expected in plan['sources'].items():
        demand(Path(filename).name == filename, 'Source must be a filename inside fixtures')
        data = (fixtures / filename).read_bytes()
        demand(sha256(data).hexdigest() == expected, f'Source changed: {filename}')
        calendar = Calendar.from_ical(data)
        demand(str(one(calendar, 'VERSION', True)) == '2.0', 'Needs VERSION:2.0')
        one(calendar, 'PRODID', True)
        scale = one(calendar, 'CALSCALE')
        demand(scale is None or str(scale) == 'GREGORIAN', 'Only Gregorian calendar dates are supported')
        demand(set(calendar) <= {'VERSION', 'PRODID', 'CALSCALE'},
               'METHOD or unsupported calendar metadata requires separate review')
        for component in calendar.walk():
            demand(not component.errors, f'Parser reported errors in {filename}')
        event_index = 0
        for component in calendar.subcomponents:
            if component.name == 'VTIMEZONE':
                name = str(one(component, 'TZID', True))
                encoded = canonical(component)
                demand(name not in tz_components or canonical(tz_components[name]) == encoded,
                       f'Conflicting VTIMEZONE definitions for {name}')
                tz_components[name] = component
                zones[name] = tzical(io.StringIO(encoded.decode())).get(name)
            else:
                demand(component.name == 'VEVENT', f'Unsupported component {component.name}')
                event_index += 1
                key = identity(component)
                sequence = int(one(component, 'SEQUENCE', True))
                records.append({'ref': f'{filename}#{event_index}', 'key': key,
                                'event': component, 'sequence': sequence,
                                'digest': sha256(canonical(component)).hexdigest()})
    refs = {r['ref']: r for r in records}
    decisions = {d['uid']: d for d in plan['decisions']}
    demand(len(decisions) == len(plan['decisions']), 'Duplicate UID decision')
    demand(set(decisions) == {r['key'][0] for r in records}, 'Every source UID needs one decision')
    selected, ledger, holds, changes = [], [], [], []
    for uid, decision in decisions.items():
        group = [r for r in records if r['key'][0] == uid]
        if decision['action'] == 'hold':
            demand(bool(decision.get('reason')), 'A hold needs a reason')
            holds.append({'uid': uid, 'reason': decision['reason'], 'sources': [r['ref'] for r in group]})
            ledger.extend({'source': r['ref'], 'uid': uid, 'disposition': 'held'} for r in group)
            continue
        demand(decision['action'] == 'include' and decision.get('evidence'),
               'Include needs documented selection evidence')
        chosen = [refs[ref] for ref in decision['select']]
        demand(all(r['key'][0] == uid for r in chosen), 'Selection names a different UID')
        chosen_keys = {r['key']: r for r in chosen}
        demand(len(chosen_keys) == len(chosen), 'Two selected components have one identity')
        demand(set(chosen_keys) == {r['key'] for r in group},
               'A recurrence identity would be silently omitted; hold the UID')
        for record in group:
            keep = chosen_keys[record['key']]
            if record['ref'] == keep['ref']:
                disposition = 'kept'
                selected.append(deepcopy(record['event']))
            elif record['digest'] == keep['digest']:
                disposition = 'duplicate'
            else:
                demand(record['sequence'] < keep['sequence'],
                       'A conflicting equal/newer revision cannot be silently superseded')
                disposition = 'superseded'
                before, after = properties(record['event']), properties(keep['event'])
                changes.append({'before_source': record['ref'], 'selected_source': keep['ref'],
                                'uid': uid, 'evidence': decision['evidence'],
                                'fields': {k: {'before': before.get(k), 'after': after.get(k)}
                                           for k in sorted(set(before) | set(after))
                                           if before.get(k) != after.get(k)}})
            ledger.append({'source': record['ref'], 'uid': uid, 'disposition': disposition,
                           'selected_source': keep['ref']})
    demand(bool(selected),
           'No candidate: all source groups are held. Keep the originals and review the hold reasons '
           'in selection.json; no ICS file or output directory was created.')
    projection = project(selected, zones)
    candidate = Calendar()
    candidate.add('prodid', '-//Calendar File Reconciliation//Reviewed Snapshot//EN')
    candidate.add('version', '2.0')
    candidate.add('calscale', 'GREGORIAN')
    used_zones = {str(value.params['TZID']) for event in selected
                  for value in event.values() if hasattr(value, 'params') and 'TZID' in value.params}
    for name in sorted(used_zones):
        candidate.add_component(deepcopy(tz_components[name]))
    for event in sorted(selected, key=identity):
        candidate.add_component(event)
    data = candidate.to_ical()
    reopened = Calendar.from_ical(data)
    readback_events = reopened.walk('VEVENT')
    demand(Counter(canonical(e) for e in selected) == Counter(canonical(e) for e in readback_events),
           'Serialization changed selected component semantics')
    demand(project(readback_events, zones) == projection, 'Saved projection differs')
    counts = dict(Counter(row['disposition'] for row in ledger))
    report = {'status': 'partial; parser-verified; no live import performed',
              'contract': plan['contract'], 'source_sha256': plan['sources'],
              'evidence_sha256': plan['evidence_sha256'],
              'candidate_sha256': sha256(data).hexdigest(),
              'parser': {'python': platform.python_version(), 'icalendar': version('icalendar'),
                         'python-dateutil': version('python-dateutil')},
              'source_components': len(records), 'output_components': len(readback_events),
              'counts': counts, 'ledger': ledger, 'changes': changes, 'holds': holds,
              'projection': projection}
    demand(sum(counts.values()) == len(records), 'Source accounting failed')
    output.mkdir(parents=True)
    (output / 'reconciled.ics').write_bytes(data)
    saved_data = (output / 'reconciled.ics').read_bytes()
    demand(saved_data == data, 'Saved bytes differ from the verified candidate')
    saved_calendar = Calendar.from_ical(saved_data)
    demand(Counter(canonical(e) for e in selected)
           == Counter(canonical(e) for e in saved_calendar.walk('VEVENT')),
           'Saved-file readback differs from selected components')
    demand(project(saved_calendar.walk('VEVENT'), zones) == projection,
           'Saved-file occurrence projection differs')
    (output / 'reconciliation.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    review = ['# Reviewed calendar file', '', report['status'], '',
              f"{len(records)} source components → {len(readback_events)} output components; "
              + ', '.join(f'{n} {k}' for k, n in sorted(counts.items())), '',
              'The held groups are absent from this partial file. This is not a cancellation or deletion request.', '',
              '## Included occurrences', '']
    for row in projection:
        text = f"- {row['uid']}: {row['start']} to {row['end_exclusive']} (exclusive end)"
        if row.get('overridden'):
            text += f"; original recurrence identity {row['original_occurrence']}"
        if 'calendar_days' in row:
            text += f"; {row['calendar_days']} calendar days"
        review.append(text)
    review.extend(['', '## Held groups', ''])
    review.extend(f"- {h['uid']}: {h['reason']}" for h in holds)
    review.extend(['', 'The JSON report accounts for every source component and shows selected revision changes.',
                   'UIDs, revision metadata, recurrence identities and selected event content are preserved.',
                   'No target application, duplicate policy, invitation behavior or live import was tested.', ''])
    (output / 'review.md').write_text('\n'.join(review))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures', type=Path, default=Path(__file__).resolve().parents[1] / 'fixtures')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = run(args.fixtures, args.output)
    except (ValueError, KeyError, TypeError) as exc:
        print(f'Blocked: {exc}', file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps({k: result[k] for k in ('status', 'source_components', 'output_components', 'counts')}, indent=2))
