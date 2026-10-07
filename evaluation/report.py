#!/usr/bin/env python3
"""Render current Markdown result tables from saved JSON; optionally check the docs.

Standard library only. No writes, imports of candidate code, grader execution,
model calls, or timing/token estimates. Run the saved-evidence verifier separately
for complete hash and grading-evidence checks.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
STUDY = ROOT / 'studies/repeated-stress-2026-10-06'
INITIAL = ROOT / 'results/native-cloud-2026-10-06'
STATUSES = ('pass', 'fail', 'not_assessed')
EVIDENCE_TYPES = (
    ('objective', 'Mechanical', 'Frozen R1/R2 data checks and R3 SQL checks'),
    ('semantic', 'AI-assisted semantic', 'Two masked reviews per R1/R2 submission'),
    ('behavioral', 'Behavioral', 'Reviewed, approved R4 probe executions'),
)
DOC_PATHS = {'overview': ROOT / 'README.md', 'study': STUDY / 'README.md',
             'index': ROOT / 'results/README.md', 'attempts': STUDY / 'results/README.md'}
DOC_TABLES = {'overview': ('overview',), 'study': ('study', 'evidence'),
              'index': ('index',), 'attempts': ('attempts',)}
GUARDS = {
    'overview': (
        'With skill (S) received the task packet plus its pinned designated package.',
        'Baseline (C) received the same task packet without that package.',
        'baseline does not mean skill-free',
        'isolation and complete process integrity were not verified',
        'Exact model identity, token use, provider cost, and comparable compute time remain unknown',
        'Its scores are not pooled with the latest study.',
    ),
    'study': (
        'With skill (S) received the task packet plus its pinned designated package.',
        'Baseline (C) received the same task packet without that package.',
        'Baseline was not skill-free',
        'Shared-filesystem isolation, complete access histories, and process integrity remain unknown',
        'Exact serving model/build, tokens, provider cost, and comparable compute time were not exposed',
        'Its denominators are not pooled here.',
        'These are AI ratings, not human evaluation;',
        'No population effect, significance, time saving, cost saving, productivity gain, or full-dot efficacy claim follows.',
    ),
    'index': (
        'The completed studies are separate records with different criteria.',
        'Do not pool their denominators.',
        'With skill (S) means the designated pinned package was supplied.',
        'Baseline (C) received no designated package but could have ambient skills.',
        'All scheduled first submissions are retained.',
        'Shared-filesystem isolation and complete process integrity were not verified; primary artifact passes are not full-process acceptance.',
        'This was outside the predeclared primary criteria and does not change those scores.',
        'They are not model trials.',
        'Not-run or unknown process status is not a 0% acceptance rate.',
        'These studies support no time-saving, productivity, statistical-significance, or population claim.',
    ),
    'attempts': (
        'C had no designated package; S received the pinned package.',
        'Pass counts refer to frozen artifact requirements.',
        'Process integrity is unknown for every row.',
        'they are not comparable model compute times.',
    ),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(summary, attempts, schedule, definitions):
    """Check table inputs against every scheduled requirement and condition."""
    planned = {row['attempt_id']: row for row in schedule['attempts']}
    ids = [row['attempt_id'] for row in attempts]
    require(len(planned) == len(schedule['attempts']), 'duplicate scheduled attempt')
    require(len(ids) == len(set(ids)) and set(ids) == set(planned),
            'missing, extra, or duplicate attempt')
    require(len(ids) == summary['scheduled_attempts'], 'stale attempt count')
    require(set(summary['conditions']) == {'C', 'S'}, 'invalid condition labels')
    order = sorted(planned.values(), key=lambda row: row['dispatch_index'])
    require([row['dispatch_index'] for row in order] == list(range(1, len(ids) + 1)),
            'missing or duplicate dispatch index')
    require(ids == [row['attempt_id'] for row in order], 'attempts not in dispatch order')
    require(len(summary['cases']) == len(definitions) and
            [case['case_id'] for case in summary['cases']] == sorted(definitions),
            'missing, duplicate, or unordered summary case')
    for case_id, definition in definitions.items():
        requirements = definition['requirements']
        require(definition['case_id'] == case_id and requirements and
                len({r['requirement_id'] for r in requirements}) == len(requirements),
                'invalid requirement definitions')
        require(all(r['mode'] in {entry[0] for entry in EVIDENCE_TYPES} for r in requirements),
                'unknown evidence mode')
    for row in attempts:
        plan = planned[row['attempt_id']]
        require((row['case_id'], row['repeat'], row['condition']) ==
                (plan['case_id'], plan['repeat'], plan['arm']), 'attempt condition or schedule mismatch')
        require(row['dispatch_index'] == plan['dispatch_index'], 'attempt dispatch index mismatch')
        require(row['attempt_id'] ==
                f"T{plan['dispatch_index']:02d}-{plan['case_id']}-r{plan['repeat']}-{plan['arm']}",
                'attempt ID does not match dispatch/case/repeat/condition')
        require(row['condition'] in {'C', 'S'} and type(row['repeat']) is int and row['repeat'] > 0,
                'invalid attempt condition or repeat')
        outcomes = Counter(r['status'] for r in row['requirements'])
        require(set(outcomes) <= set(STATUSES), 'unknown requirement status')
        expected = {status: outcomes[status] for status in STATUSES}
        require(row['counts'] == expected, 'stale per-attempt counts')
        require(len(row['requirements']) == row['scheduled_requirements'], 'missing requirement')
        require([{key: r[key] for key in ('requirement_id', 'mode')} for r in row['requirements']] ==
                [{key: r[key] for key in ('requirement_id', 'mode')}
                 for r in definitions[row['case_id']]['requirements']],
                'requirement identity or evidence mode mismatch')
        require(row['completed_criteria'] == (expected['pass'] == row['scheduled_requirements']),
                'stale completion status')
        paths = [artifact['path'] for artifact in row['artifacts']]
        require(len(paths) == len(set(paths)) and paths == sorted(paths) and
                all(Path(path).parts[:2] == ('artifacts', row['attempt_id']) and
                    len(Path(path).parts) == 3 and '..' not in Path(path).parts for path in paths),
                'invalid or duplicate artifact links')
        require(row['process_integrity'] == 'unknown', 'unsupported process-integrity claim')
    case_ids = {row['case_id'] for row in attempts}
    require(len(case_ids) == summary['authored_cases'] and
            case_ids == {case['case_id'] for case in summary['cases']}, 'case coverage mismatch')
    require(sum(r['scheduled_requirements'] for r in attempts) ==
            summary['scheduled_requirement_instances'], 'stale scheduled total')
    require(sum(len(c['requirements']) for c in definitions.values()) == summary['distinct_requirements'],
            'stale distinct requirement count')
    require(sum(len(row['artifacts']) for row in attempts) == summary['artifact_files'],
            'stale artifact file count')
    coverage = {mode: {s: sum(r['status'] == s for row in attempts for r in row['requirements']
                              if r['mode'] == mode) for s in STATUSES}
                for mode, _, _ in EVIDENCE_TYPES}
    require(coverage == summary['evidence_coverage'], 'stale evidence-mode counts')
    require({mode: {case_id for case_id, case in definitions.items()
                    if any(r['mode'] == mode for r in case['requirements'])}
             for mode, _, _ in EVIDENCE_TYPES} ==
            {'objective': {'R1', 'R2', 'R3'}, 'semantic': {'R1', 'R2'}, 'behavioral': {'R4'}},
            'evidence basis does not match scheduled case modes')
    pairs = {}
    for row in attempts:
        pair = pairs.setdefault((row['case_id'], row['repeat']), {})
        require(row['condition'] not in pair, 'duplicate case/repeat/condition')
        pair[row['condition']] = row
    require(all(set(pair) == {'C', 'S'} for pair in pairs.values()), 'incomplete case/repeat pair')
    expected_pairs = [
        {'case_id': case_id, 'repeat': repeat,
         **{arm: {'attempt_id': pair[arm]['attempt_id'], **pair[arm]['counts']} for arm in ('C', 'S')},
         'scheduled_requirements_per_condition': pair['C']['scheduled_requirements'],
         'verified_pass_difference_S_minus_C': pair['S']['counts']['pass'] - pair['C']['counts']['pass']}
        for (case_id, repeat), pair in sorted(pairs.items())]
    require(summary['pairs'] == expected_pairs and summary['case_repeat_pairs'] == len(pairs),
            'stale paired outcomes')
    for arm in ('C', 'S'):
        rows = [r for r in attempts if r['condition'] == arm]
        total = summary['conditions'][arm]
        require(total['attempts'] == len(rows), 'stale condition attempt count')
        require(total['complete_attempts'] == sum(r['completed_criteria'] for r in rows),
                'stale condition completion count')
        require(total['scheduled_requirements'] == sum(r['scheduled_requirements'] for r in rows),
                'stale condition denominator')
        require(total['counts'] == {s: sum(r['counts'][s] for r in rows) for s in STATUSES},
                'stale condition counts')
        fractions = []
        for case in summary['cases']:
            selected = [r for r in rows if r['case_id'] == case['case_id']]
            entry = case['conditions'][arm]
            denominator = sum(r['scheduled_requirements'] for r in selected)
            counts = {s: sum(r['counts'][s] for r in selected) for s in STATUSES}
            definition = definitions[case['case_id']]
            require(case['label'] == definition['label'] and
                    case['requirements_per_attempt'] == len(definition['requirements']),
                    'stale case label or denominator')
            require(entry['counts'] == counts and entry['scheduled_requirements'] == denominator,
                    'stale case counts')
            fractions.append(counts['pass'] / denominator)
        require(total['equal_case_mean_verified_fraction'] == sum(fractions) / len(fractions),
                'stale equal-case fraction')


def validate_initial(summary, attempts, schedule):
    """Bind the index's older-study counts to saved criterion groups, not new grades."""
    rows = attempts['rows']
    require(len({row['attempt_id'] for row in rows}) == len(rows), 'duplicate initial attempt')
    planned = {row['attempt_id']: row for row in schedule['rows']}
    require(len(planned) == len(schedule['rows']) and
            set(planned) == {row['attempt_id'] for row in rows},
            'missing or duplicate initial scheduled attempt')
    ordinals = [row['ordinal'] for row in planned.values()]
    require(all(type(value) is int for value in ordinals) and
            sorted(ordinals) == list(range(1, len(rows) + 1)), 'invalid initial schedule ordinals')
    for row in rows:
        plan = planned[row['attempt_id']]
        require(row['attempt_id'] == f"N{plan['ordinal']:02d}-{plan['case_id']}-{plan['arm']}" and
                all(type(row[actual]) is type(plan[expected]) and row[actual] == plan[expected]
                    for actual, expected in (('case_id', 'case_id'), ('arm', 'arm'),
                                             ('schedule_ordinal', 'ordinal'))),
                'initial attempt identity or schedule mismatch')
    cases = {row['case_id'] for row in rows}
    require(len(rows) == attempts['scheduled_attempts'] == summary['scheduled_attempts'] ==
            summary['first_submissions'] and len(cases) == summary['scheduled_cases'],
            'stale initial case or attempt count')
    require([pair['case_id'] for pair in summary['rows']] == sorted(cases),
            'missing, duplicate, or unordered initial case')
    outcomes = Counter()
    for pair in summary['rows']:
        selected = [row for row in rows if row['case_id'] == pair['case_id']]
        require(len(selected) == 2 and {row['arm'] for row in selected} == {'C', 'S'},
                'missing or duplicate initial condition')
        for row in selected:
            groups = row['criterion_groups']
            require(groups and len({group['id'] for group in groups}) == len(groups),
                    'missing or duplicate initial criterion')
            states = [group['passed'] for group in groups]
            require(all(state is None or type(state) is bool for state in states),
                    'invalid initial criterion state')
            counts = {'passed': states.count(True), 'failed': states.count(False),
                      'unknown': states.count(None), 'total': len(states)}
            require(pair[row['arm']] == counts, 'stale initial case counts')
        c, s = pair['C'], pair['S']
        comparable = c['unknown'] == s['unknown'] == 0 and c['total'] == s['total']
        delta = s['passed'] - c['passed'] if comparable else None
        outcome = ('tie' if delta == 0 else 'S_win' if delta > 0 else 'S_loss') if comparable else 'unresolved'
        require(pair['S_minus_C_passed_groups'] == delta and pair['paired_outcome'] == outcome,
                'stale initial paired outcome')
        outcomes[outcome] += 1
    require(summary['paired_outcomes'] ==
            {key: outcomes[key] for key in ('S_win', 'tie', 'S_loss', 'unresolved')},
            'stale initial paired outcomes')
    for arm in ('C', 'S'):
        require(summary[arm] == {key: sum(pair[arm][key] for pair in summary['rows'])
                                for key in ('passed', 'failed', 'unknown', 'total')},
                'stale initial condition counts')


def fraction(value):
    return f"{value['counts']['pass']}/{value['scheduled_requirements']}"


def tables(summary, attempts, initial):
    skill, baseline = (summary['conditions'][arm] for arm in ('S', 'C'))
    overview = [
        '| Metric | With skill | Baseline | Delta (S − C) |',
        '| --- | ---: | ---: | ---: |',
        f"| Requirements passed / scheduled | {fraction(skill)} | {fraction(baseline)} | {skill['counts']['pass'] - baseline['counts']['pass']} |",
        f"| Submissions meeting all requirements | {skill['complete_attempts']}/{skill['attempts']} | {baseline['complete_attempts']}/{baseline['attempts']} | {skill['complete_attempts'] - baseline['complete_attempts']} |",
        f"| Equal-case mean verified fraction | {100 * skill['equal_case_mean_verified_fraction']:g}% | {100 * baseline['equal_case_mean_verified_fraction']:g}% | {100 * (skill['equal_case_mean_verified_fraction'] - baseline['equal_case_mean_verified_fraction']):g} pp |",
    ]
    study = ['| Case | With skill | Baseline | Delta (S − C) |', '| --- | ---: | ---: | ---: |']
    for case in summary['cases']:
        s, c = (case['conditions'][arm] for arm in ('S', 'C'))
        study.append(f"| [{case['case_id']} · {case['label']}](cases/{case['case_id']}/candidate/TASK.md) | {fraction(s)} | {fraction(c)} | {s['counts']['pass'] - c['counts']['pass']} |")
    study.append(f"| Total scheduled requirement instances | {fraction(skill)} | {fraction(baseline)} | {skill['counts']['pass'] - baseline['counts']['pass']} |")
    evidence = ['| Evidence type | Passed / scheduled, both conditions | Basis |', '| --- | ---: | --- |']
    for mode, label, basis in EVIDENCE_TYPES:
        counts = summary['evidence_coverage'][mode]
        evidence.append(f"| {label} | {counts['pass']}/{sum(counts.values())} | {basis} |")
    tied = sum(pair['verified_pass_difference_S_minus_C'] == 0 and
               pair['C']['not_assessed'] == pair['S']['not_assessed'] == 0
               for pair in summary['pairs'])
    index = [
        '| Study | Cases / submissions | With skill | Baseline | Primary result |',
        '| --- | ---: | ---: | ---: | --- |',
        f"| [Repeated stress study](../studies/repeated-stress-2026-10-06/README.md), 2026-10-06 | {summary['authored_cases']} / {summary['scheduled_attempts']} | {fraction(skill)} requirements | {fraction(baseline)} requirements | {tied} tied case/repeat pairs |",
        f"| [Initial native-cloud study](native-cloud-2026-10-06/README.md), 2026-10-06 | {initial['scheduled_cases']} / {initial['scheduled_attempts']} | {initial['S']['passed']}/{initial['S']['total']} criterion groups | {initial['C']['passed']}/{initial['C']['total']} criterion groups | {initial['paired_outcomes']['tie']} tied case pairs |",
    ]
    submissions = [
        '| Attempt | Workflow | Repeat | Condition | Pass / scheduled | Fail | Not assessed | Saved files |',
        '|---|---|---:|:---:|---:|---:|---:|---|',
    ]
    for row in attempts:
        links = ' · '.join(f"[{Path(artifact['path']).name}](../{artifact['path']})"
                           for artifact in row['artifacts'])
        counts = row['counts']
        submissions.append(f"| {row['attempt_id']} | {row['case_id']} | {row['repeat']} | {row['condition']} | {counts['pass']} / {row['scheduled_requirements']} | {counts['fail']} | {counts['not_assessed']} | {links} |")
    return {name: '\n'.join(rows) for name, rows in
            (('overview', overview), ('study', study), ('evidence', evidence),
             ('index', index), ('attempts', submissions))}


def visible_markdown(text):
    """Exclude fenced examples; fail closed on HTML, including comments.

    These reports use a small plain-Markdown subset. Rejecting HTML avoids
    synthesizing a table or fence by deleting comment text from a physical line.
    """
    lines, fence = [], None
    for line in text.splitlines():
        if fence is not None:
            marker, width = fence
            closing = re.fullmatch(r' {0,3}' + re.escape(marker) + '{' + str(width) + r',}\s*', line)
            if closing:
                fence = None
            lines.append('')
            continue
        opener = re.match(r' {0,3}(`{3,}|~{3,})(.*)', line)
        if opener and not (opener[1][0] == '`' and '`' in opener[2]):
            fence = (opener[1][0], len(opener[1]))
            lines.append('')
        else:
            require(not re.search(r'<(?:/?[A-Za-z]|[!?])', line),
                    'unsupported raw HTML, comment, or angle-bracket construct in report')
            lines.append(line)
    return '\n'.join(lines)


def table_cells(line):
    """Recognize unescaped separators, including optional outer pipes."""
    # Quoted tables are outside the reports' style but must not escape detection.
    line = re.sub(r'^(?:\s*>\s*)+', '', line).strip()
    cells, value, escaped = [], [], False
    for character in line:
        if character == '|' and not escaped:
            cells.append(''.join(value).strip())
            value = []
        else:
            value.append(character)
        escaped = character == '\\' and not escaped
    cells.append(''.join(value).strip())
    if len(cells) > 1 and not cells[0]:
        cells.pop(0)
    if len(cells) > 1 and not cells[-1]:
        cells.pop()
    return cells


def markdown_tables(text):
    """Recognize plain pipe tables, retaining complete rows for exact comparison."""
    lines = visible_markdown(text).splitlines()
    blocks, index = [], 0
    while index + 1 < len(lines):
        header, separator = table_cells(lines[index]), table_cells(lines[index + 1])
        if (lines[index].strip() and '|' in lines[index] + lines[index + 1] and
                len(header) == len(separator) and
                all(re.fullmatch(r':?-+:?', cell) for cell in separator)):
            end = index + 2
            # These reports separate tables with blank lines. Keep every
            # nonblank body line rather than guessing GFM block interruptions;
            # a row may omit outer pipes or contain a single/list-like cell.
            while end < len(lines) and lines[end].strip():
                end += 1
            blocks.append('\n'.join(lines[index:end]))
            index = end
        else:
            index += 1
    return blocks


def check_docs(rendered, docs):
    for name, names in DOC_TABLES.items():
        require(markdown_tables(docs[name]) == [rendered[table] for table in names],
                f'{name}: stale or missing result table, extra rows, or duplicate table')
        visible = visible_markdown(docs[name])
        for text in GUARDS[name]:
            require(visible.count(text) == 1,
                    f'{name}: missing condition definition or limitation: {text}')


def check_claims(summary, attempts, initial, docs):
    """Check bounded numeric statements; this is not a general prose fact checker."""
    cases, runs = summary['authored_cases'], summary['scheduled_attempts']
    repeats = {row['repeat'] for row in attempts}
    require(repeats == set(range(1, len(repeats) + 1)) and
            all({row['repeat'] for row in attempts if row['case_id'] == case['case_id']
                 and row['condition'] == arm} == repeats
                for case in summary['cases'] for arm in ('C', 'S')),
            'unbalanced repeat coverage')
    require(all(pair['verified_pass_difference_S_minus_C'] == 0 for pair in summary['pairs']) and
            all(row['counts']['fail'] == row['counts']['not_assessed'] == 0 for row in attempts),
            'ceiling and all-pairs-tied prose is unsupported')
    require(all(initial[arm]['failed'] == initial[arm]['unknown'] == 0 for arm in ('C', 'S')),
            'initial ceiling prose is unsupported')
    common = [f'- Cases: {cases} authored synthetic workflows',
              f'- Runs: {runs} first submissions, with {len(repeats)} repeats per case and condition']
    claims = {
        'overview': [*common,
                     f"All {summary['case_repeat_pairs']} case/repeat pairs tied.",
                     f"The {summary['distinct_requirements']} distinct requirements produced {summary['scheduled_requirement_instances']} scheduled instances across both conditions, with no failed or unassessed instances.",
                     f"contains {initial['scheduled_attempts']} submissions and {initial['S']['passed']}/{initial['S']['total']} primary criterion groups per condition."],
        'study': [*common,
                  f"All {summary['case_repeat_pairs']} case/repeat pairs tied;",
                  f"There were {summary['distinct_requirements']} distinct requirements and {summary['scheduled_requirement_instances']} scheduled instances overall, with zero failed or not assessed.",
                  f"[All {summary['artifact_files']} original artifact files](artifacts/)"],
        'index': [f'[all {runs} submissions]', f"[all {initial['scheduled_attempts']} attempts]"],
        'attempts': [f'All {runs} rows are retained in dispatch order.'],
    }
    per_case = {case['case_id']: case['requirements_per_attempt'] for case in summary['cases']}
    require(per_case['R1'] == per_case['R2'], 'shared R1/R2 denominator prose is unsupported')
    claims['study'].append(
        f"Each R1/R2 submission passed {per_case['R1']}/{per_case['R1']} requirements, "
        f"R3 passed {per_case['R3']}/{per_case['R3']}, and R4 passed {per_case['R4']}/{per_case['R4']}.")
    skill, baseline = (summary['conditions'][arm] for arm in ('S', 'C'))
    require(skill == baseline, 'shared per-condition prose is unsupported')
    claims['study'].append(
        f"Each condition had {skill['complete_attempts']}/{skill['attempts']} submissions meeting all criteria "
        f"and a predeclared equal-case mean verified fraction of {100 * skill['equal_case_mean_verified_fraction']:g}%.")
    for name, sentences in claims.items():
        visible = visible_markdown(docs[name])
        for text in sentences:
            require(visible.count(text) == 1, f'{name}: stale numeric statement: {text}')


def load_inputs():
    def read(path):
        return json.loads(path.read_text(encoding='utf-8'))
    return (read(STUDY / 'results/summary.json'), read(STUDY / 'results/attempts.json'),
            read(STUDY / 'methods/schedule.json'), read(STUDY / 'results/requirements.json'),
            read(INITIAL / 'paired-summary.json'), read(INITIAL / 'attempts.json'),
            read(INITIAL / 'schedule.json'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='check current report tables and required caveats')
    args = parser.parse_args()
    summary, attempts, schedule, definitions, initial, initial_attempts, initial_schedule = load_inputs()
    validate(summary, attempts, schedule, definitions)
    validate_initial(initial, initial_attempts, initial_schedule)
    rendered = tables(summary, attempts, initial)
    if args.check:
        docs = {name: path.read_text(encoding='utf-8') for name, path in DOC_PATHS.items()}
        check_docs(rendered, docs)
        check_claims(summary, attempts, initial, docs)
        print('Report checks passed: both studies\' saved counts; five complete Markdown tables '
              'across four reports; dispatch order, artifact links, evidence modes, numeric statements, and required caveats.')
    else:
        print('\n\n'.join(rendered.values()))


if __name__ == '__main__':
    try:
        main()
    except (KeyError, OSError, TypeError, ValueError, ZeroDivisionError) as error:
        print(f'Report check failed: {error}', file=sys.stderr)
        raise SystemExit(1)
