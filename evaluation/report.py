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
import sys

ROOT = Path(__file__).resolve().parent
STUDY = ROOT / 'studies/repeated-stress-2026-10-06'
STATUSES = ('pass', 'fail', 'not_assessed')
GUARDS = {
    'overview': (
        'With skill (S) received the task packet plus its pinned designated package.',
        'Baseline (C) received the same task packet without that package.',
        'baseline does not mean skill-free',
        'isolation and complete process integrity were not verified',
        'Exact model identity, token use, provider cost, and comparable compute time remain unknown',
    ),
    'study': (
        'With skill (S) received the task packet plus its pinned designated package.',
        'Baseline (C) received the same task packet without that package.',
        'Baseline was not skill-free',
        'Shared-filesystem isolation, complete access histories, and process integrity remain unknown',
        'Exact serving model/build, tokens, provider cost, and comparable compute time were not exposed',
    ),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(summary, attempts, schedule):
    """Check table inputs against every scheduled requirement and condition."""
    planned = {row['attempt_id']: row for row in schedule['attempts']}
    ids = [row['attempt_id'] for row in attempts]
    require(len(planned) == len(schedule['attempts']), 'duplicate scheduled attempt')
    require(len(ids) == len(set(ids)) and set(ids) == set(planned),
            'missing, extra, or duplicate attempt')
    require(len(ids) == summary['scheduled_attempts'], 'stale attempt count')
    require(set(summary['conditions']) == {'C', 'S'}, 'invalid condition labels')
    for row in attempts:
        plan = planned[row['attempt_id']]
        require((row['case_id'], row['repeat'], row['condition']) ==
                (plan['case_id'], plan['repeat'], plan['arm']), 'attempt condition or schedule mismatch')
        outcomes = Counter(r['status'] for r in row['requirements'])
        require(set(outcomes) <= set(STATUSES), 'unknown requirement status')
        expected = {status: outcomes[status] for status in STATUSES}
        require(row['counts'] == expected, 'stale per-attempt counts')
        require(len(row['requirements']) == row['scheduled_requirements'], 'missing requirement')
        require(row['completed_criteria'] == (expected['pass'] == row['scheduled_requirements']),
                'stale completion status')
    case_ids = {row['case_id'] for row in attempts}
    require(len(case_ids) == summary['authored_cases'] and
            case_ids == {case['case_id'] for case in summary['cases']}, 'case coverage mismatch')
    require(sum(r['scheduled_requirements'] for r in attempts) ==
            summary['scheduled_requirement_instances'], 'stale scheduled total')
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
            require(entry['counts'] == counts and entry['scheduled_requirements'] == denominator,
                    'stale case counts')
            fractions.append(counts['pass'] / denominator)
        require(total['equal_case_mean_verified_fraction'] == sum(fractions) / len(fractions),
                'stale equal-case fraction')


def fraction(value):
    return f"{value['counts']['pass']}/{value['scheduled_requirements']}"


def tables(summary):
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
    return {'overview': '\n'.join(overview), 'study': '\n'.join(study)}


def check_docs(rendered, docs):
    for name, table in rendered.items():
        require(docs[name].count(table) == 1, f'{name}: stale or missing result table')
        for text in GUARDS[name]:
            require(text in docs[name], f'{name}: missing condition definition or limitation: {text}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='check current report tables and required caveats')
    args = parser.parse_args()
    summary = json.loads((STUDY / 'results/summary.json').read_text())
    attempts = json.loads((STUDY / 'results/attempts.json').read_text())
    schedule = json.loads((STUDY / 'methods/schedule.json').read_text())
    validate(summary, attempts, schedule)
    rendered = tables(summary)
    if args.check:
        check_docs(rendered, {'overview': (ROOT / 'README.md').read_text(),
                              'study': (STUDY / 'README.md').read_text()})
        print('Report checks passed: scheduled attempts, condition labels, saved counts, two Markdown tables, and required caveats.')
    else:
        print(rendered['overview'] + '\n\n' + rendered['study'])


if __name__ == '__main__':
    try:
        main()
    except (KeyError, OSError, ValueError, ZeroDivisionError) as error:
        print(f'Report check failed: {error}', file=sys.stderr)
        raise SystemExit(1)
