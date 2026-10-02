#!/usr/bin/env python3
"""Behavioral checks for the fictional, offline snapshot-reconciliation profile."""
from contextlib import contextmanager
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from hashlib import sha256
import io
import json
from pathlib import Path
import shutil
import socket
import tempfile
from unittest.mock import patch
from zoneinfo import ZoneInfo

from icalendar import Calendar, vDDDTypes
from dateutil.tz import datetime_exists, tzical
import reconcile

ROOT = Path(__file__).resolve().parents[1]


def check(condition, message):
    if not condition:
        raise AssertionError(message)


@contextmanager
def case():
    with tempfile.TemporaryDirectory(prefix='calendar-file-check-') as tmp:
        root = Path(tmp)
        fixtures = root / 'fixtures'
        shutil.copytree(ROOT / 'fixtures', fixtures)
        yield fixtures, root / 'output'


def edit_plan(fixtures, mutate):
    path = fixtures / 'selection.json'
    plan = json.loads(path.read_text())
    mutate(plan)
    path.write_text(json.dumps(plan, indent=2) + '\n')


def edit_calendar(fixtures, name, mutate, update_hash=True):
    path = fixtures / name
    cal = Calendar.from_ical(path.read_bytes())
    mutate(cal)
    path.write_bytes(cal.to_ical())
    if update_hash:
        edit_plan(fixtures, lambda p: p['sources'].__setitem__(name, sha256(path.read_bytes()).hexdigest()))


def include(plan, uid, refs):
    for index, decision in enumerate(plan['decisions']):
        if decision['uid'] == uid + '@example.invalid':
            plan['decisions'][index] = {'uid': decision['uid'], 'action': 'include',
                                        'select': refs, 'evidence': 'Negative test selection'}
            return
    raise AssertionError('Missing fixture UID')


def blocked(mutate, expected):
    with case() as (fixtures, output):
        mutate(fixtures)
        try:
            reconcile.run(fixtures, output)
        except ValueError as exc:
            check(expected in str(exc), f'Wrong failure: {exc}')
        else:
            raise AssertionError(f'Expected rejection: {expected}')
        check(not output.exists(), 'Failure wrote an output directory')


def hold_all(plan):
    plan['decisions'] = [{'uid': d['uid'], 'action': 'hold',
                          'reason': 'Every group needs more evidence in this regression'}
                         for d in plan['decisions']]


def local_spring_event(calendar, hour):
    event = calendar.walk('VEVENT')[2]
    for name, minute in (('DTSTART', 30), ('DTEND', 45)):
        value = vDDDTypes(datetime(2026, 3, 29, hour, minute,
                                  tzinfo=ZoneInfo('Europe/London')))
        value.params['TZID'] = 'Europe/London'
        event[name] = value


def check_spring_transition(calendars):
    reference = ZoneInfo('Europe/London')
    for calendar in calendars:
        component = calendar.walk('VTIMEZONE')[0]
        daylight = component.walk('DAYLIGHT')[0]
        check(daylight['DTSTART'].dt == datetime(2026, 3, 29, 1),
              'Spring onset must use the 01:00 pre-transition local clock')
        embedded = tzical(io.StringIO(component.to_ical().decode())).get('Europe/London')
        for hour, expected_exists in ((0, True), (1, False), (2, True)):
            wall = datetime(2026, 3, 29, hour, 30)
            check(datetime_exists(wall, embedded) == expected_exists,
                  f'Embedded definition misplaces the spring gap at {wall}')
            check(datetime_exists(wall, reference) == expected_exists,
                  f'ZoneInfo disagrees with the expected spring gap at {wall}')
            if expected_exists:
                check(wall.replace(tzinfo=embedded).utcoffset()
                      == wall.replace(tzinfo=reference).utcoffset(),
                      'Embedded and ZoneInfo offsets disagree beside the gap')
        for utc_time, local_time in ((datetime(2026, 3, 29, 0, 59, tzinfo=timezone.utc),
                                      datetime(2026, 3, 29, 0, 59)),
                                     (datetime(2026, 3, 29, 1, tzinfo=timezone.utc),
                                      datetime(2026, 3, 29, 2))):
            check(utc_time.astimezone(embedded).replace(tzinfo=None) == local_time
                  and utc_time.astimezone(reference).replace(tzinfo=None) == local_time,
                  'The UTC transition boundary does not match the London rule')


def main():
    tests = []
    # Any accidental network socket attempt fails before a connection is made.
    with patch.object(socket, 'socket', side_effect=AssertionError('Network is prohibited in this check')):
        with case() as (fixtures, output):
            before = {p.name: sha256(p.read_bytes()).hexdigest() for p in fixtures.iterdir()}
            result = reconcile.run(fixtures, output)
            after = {p.name: sha256(p.read_bytes()).hexdigest() for p in fixtures.iterdir()}
            check(before == after, 'Source files changed')
            check(result['counts'] == {'superseded': 2, 'kept': 4, 'duplicate': 1, 'held': 5},
                  'Every source component must have the right disposition')
            check(len(result['ledger']) == 12 and len({r['source'] for r in result['ledger']}) == 12,
                  'Source accounting is incomplete')
            data = (output / 'reconciled.ics').read_bytes()
            check(b'\r\n ' in data, 'The actual output should exercise folded text')
            check(data.endswith(b'\r\n') and b'\n' not in data.replace(b'\r\n', b''), 'Expected CRLF')
            cal = Calendar.from_ical(data)
            check_spring_transition([Calendar.from_ical((fixtures / name).read_bytes())
                                     for name in ('earlier.ics', 'revised.ics')] + [cal])
            events = cal.walk('VEVENT')
            check(len(events) == 4, 'Wrong component count')
            check(len([e for e in events if str(e['SUMMARY']) == 'Open source office hour']) == 3,
                  'Same-title distinct UID or moved component was lost')
            master = next(e for e in events if str(e['UID']) == 'office-hour@example.invalid'
                          and 'RECURRENCE-ID' not in e)
            override = next(e for e in events if 'RECURRENCE-ID' in e)
            check(str(master['X-EXAMPLE-COLOR']) == 'blue', 'Extension field lost')
            check(str(master['DESCRIPTION']) == 'Bring a laptop, charger; and notes.\nCafé room opens early. Use the side entrance beside the repair desk.',
                  'Escapes, Unicode or folded text changed')
            check(override['RECURRENCE-ID'].to_ical() == b'20261026T090000'
                  and override['DTSTART'].to_ical() == b'20261026T100000'
                  and int(override['SEQUENCE']) == 3, 'Moved identity or revision changed')
            series = [r for r in result['projection'] if r['uid'] == 'office-hour@example.invalid']
            check([r['start_utc'] for r in series] == ['2026-10-19T08:00:00+00:00',
                                                     '2026-10-26T10:00:00+00:00',
                                                     '2026-11-03T09:00:00+00:00'],
                  'Clock-change, override, EXDATE or RDATE semantics wrong')
            allday = next(e for e in events if str(e['UID']) == 'swap-weekend@example.invalid')
            check(type(allday['DTSTART'].dt) is date and allday['DTSTART'].dt == date(2026, 10, 24)
                  and allday['DTEND'].dt == date(2026, 10, 27), 'All-day inclusive days changed')
            check({h['uid'] for h in result['holds']} == {'repair-appointment@example.invalid',
                                                         'design-review@example.invalid',
                                                         'repair-clinic@example.invalid'}, 'Holds incomplete')
            check(not any(str(e['UID']) in {h['uid'] for h in result['holds']} for e in events),
                  'Held event leaked into the candidate')
            # Repeated runs in fresh locations must yield the same candidate bytes.
            other = output.parent / 'second-output'
            reconcile.run(fixtures, other)
            check(data == (other / 'reconciled.ics').read_bytes(), 'Reconciliation is not reproducible')
            try:
                reconcile.run(fixtures, output)
            except ValueError as exc:
                check('new output directory' in str(exc), 'Unexpected overwrite rejection')
            else:
                raise AssertionError('Existing result was overwritten')
        tests.append('baseline: 12 components, exact dispositions, identities, text, recurrence and source preservation')
        tests.append('spring gap: both source definitions and saved definition agree with ZoneInfo')
        with case() as (fixtures, output):
            edit_calendar(fixtures, 'earlier.ics', lambda c: local_spring_event(c, 2))
            result = reconcile.run(fixtures, output)
            row = next(r for r in result['projection']
                       if r['uid'] == 'separate-office-hour@example.invalid')
            check(row['start_utc'] == '2026-03-29T01:30:00+00:00'
                  and row['end_utc'] == '2026-03-29T01:45:00+00:00',
                  'A valid 02:30 London spring occurrence was shifted or blocked')
        tests.append('valid spring 02:30 occurrence is accepted at the correct UTC instant')
        cases = [
            ('all groups held', lambda f: edit_plan(f, hold_all), 'No candidate: all source groups are held'),
            ('spring gap 01:30 occurrence', lambda f: edit_calendar(f, 'earlier.ics', lambda c: local_spring_event(c, 1)), 'Skipped or repeated'),
            ('changed source hash', lambda f: edit_calendar(f, 'earlier.ics', lambda c: c.walk('VEVENT')[0].__setitem__('LOCATION', 'Elsewhere'), False), 'Source changed'),
            ('changed evidence hash', lambda f: (f / 'owner-notes.md').write_text('Changed evidence\n'), 'Selection evidence changed'),
            ('equal-revision conflict', lambda f: edit_plan(f, lambda p: include(p, 'design-review', ['earlier.ics#5'])), 'equal/newer revision'),
            ('floating time', lambda f: edit_plan(f, lambda p: include(p, 'repair-appointment', ['earlier.ics#4'])), 'Floating time'),
            ('stale active cancellation copy', lambda f: edit_plan(f, lambda p: include(p, 'repair-clinic', ['earlier.ics#6'])), 'equal/newer revision'),
            ('cancelled component emitted', lambda f: edit_plan(f, lambda p: include(p, 'repair-clinic', ['revised.ics#6'])), 'Cancellation is held'),
            ('missing override', lambda f: edit_plan(f, lambda p: include(p, 'office-hour', ['revised.ics#1'])), 'silently omitted'),
            ('wrong UID selected', lambda f: edit_plan(f, lambda p: include(p, 'office-hour', ['earlier.ics#3'])), 'different UID'),
            ('scheduling METHOD', lambda f: edit_calendar(f, 'earlier.ics', lambda c: c.add('METHOD', 'REQUEST')), 'METHOD'),
            ('unsupported calendar scale', lambda f: edit_calendar(f, 'earlier.ics', lambda c: c.__setitem__('CALSCALE', 'UNSUPPORTED')), 'Only Gregorian'),
            ('range override', lambda f: edit_calendar(f, 'revised.ics', lambda c: c.walk('VEVENT')[1]['RECURRENCE-ID'].params.__setitem__('RANGE', 'THISANDFUTURE')), 'RANGE changes'),
            ('unsupported recurrence', lambda f: edit_calendar(f, 'revised.ics', lambda c: [e['RRULE'].__setitem__('BYDAY', ['MO']) for e in c.walk('VEVENT') if 'RRULE' in e]), 'Only FREQ=WEEKLY'),
            ('conflicting VTIMEZONE', lambda f: edit_calendar(f, 'revised.ics', lambda c: c.walk('VTIMEZONE')[0].__setitem__('COMMENT', 'Different definition')), 'Conflicting VTIMEZONE'),
            ('non-positive event span', lambda f: edit_calendar(f, 'earlier.ics', lambda c: c.walk('VEVENT')[2].__setitem__('DTEND', deepcopy(c.walk('VEVENT')[2]['DTSTART']))), 'DTEND must be after'),
            ('alarm side effect', lambda f: edit_calendar(f, 'earlier.ics', add_alarm), 'Nested components'),
        ]
        for name, mutate, expected in cases:
            blocked(mutate, expected)
            tests.append(name)
    print(json.dumps({'status': 'passed', 'checks': tests,
                      'network': 'socket creation prohibited during all reconciliation calls',
                      'scope': 'offline parser, bounded projection and rejection behavior; no calendar UI import'}, indent=2))


def add_alarm(calendar):
    from icalendar import Alarm
    alarm = Alarm()
    alarm.add('ACTION', 'DISPLAY')
    alarm.add('DESCRIPTION', 'Fictional alarm')
    alarm.add('TRIGGER', timedelta(minutes=-5))
    calendar.walk('VEVENT')[2].add_component(alarm)


if __name__ == '__main__':
    main()
