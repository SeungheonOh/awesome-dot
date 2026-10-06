#!/usr/bin/env python3
"""Render the README's native-cloud comparison using only the Python stdlib.

From the repository root:
    python -B evaluation/visualization/render_native_results.py
    python -B evaluation/visualization/render_native_results.py --check

Reads the published paired-summary.json, status.json and F8 execution-results.json.
Numeric labels and bar segments come from those records; no model calls, candidate
execution, external assets, fonts, dependencies, or network access are needed.
Both SVGs include the source-file SHA-256 hashes. --check verifies committed bytes.
This is a deliberately study-specific layout: changed findings fail validation so
its headline and post-hoc caveat cannot silently become stale.
"""

import argparse
import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY = 'evaluation/results/native-cloud-2026-10-06'
SOURCES = (f'{STUDY}/paired-summary.json', 'evaluation/results/status.json',
           f'{STUDY}/f8/execution-results.json')
BG, INK, MUTED, LINE = '#F5F3EC', '#1B2820', '#566159', '#D3D8CE'
SAGE, ORANGE = '#57735F', '#DB532C'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_data():
    raw = [(ROOT / path).read_bytes() for path in SOURCES]
    paired, status, execution = [json.loads(data) for data in raw]
    study = status['native_cloud_study']
    rows = paired['rows']
    count = len(rows)
    require(count == paired['scheduled_cases'] == study['scheduled_cases'],
            'Case counts disagree')
    require(len({r['case_id'] for r in rows}) == count, 'Duplicate case IDs')
    require(paired['scheduled_attempts'] == paired['first_submissions'] ==
            study['scheduled_attempts'] == study['first_submissions'] == 2 * count,
            'Attempt counts disagree')
    for arm in ('C', 'S'):
        for field in ('passed', 'failed', 'unknown', 'total'):
            require(sum(r[arm][field] for r in rows) == paired[arm][field],
                    f'{arm} {field} does not sum to the reported total')
        require(all(r[arm]['passed'] + r[arm]['failed'] + r[arm]['unknown'] ==
                    r[arm]['total'] for r in rows), 'Invalid criterion counts')
        require(paired[arm]['passed'] == study[arm]['criterion_groups_passed'] and
                paired[arm]['total'] == study[arm]['criterion_groups'],
                f'{arm} status does not match paired results')
        passed_cases = sum(r[arm]['passed'] == r[arm]['total'] for r in rows)
        require(passed_cases == study[arm]['cases_all_primary_artifact_groups_passed']
                and count == study[arm]['cases'], 'Artifact counts disagree')
    delta = 100 * (paired['S']['passed'] / paired['S']['total'] -
                   paired['C']['passed'] / paired['C']['total'])
    require(delta == study['primary_artifact_group_pass_rate_difference_percentage_points'],
            'Pass-rate difference disagrees')
    require(count == paired['paired_outcomes']['tie'] == study['paired_ties'] and
            all(r['paired_outcome'] == 'tie' and r['S_minus_C_passed_groups'] == 0
                for r in rows), 'The tie headline must be reviewed')
    require(delta == 0 and all(paired[a]['passed'] == paired[a]['total']
                              for a in ('C', 'S')), 'The ceiling headline must be reviewed')
    require(count == 8 and all(paired[a]['total'] == 40 for a in ('C', 'S')),
            'This layout is sized for the original eight-case study')
    require(paired['process_integrity'] is None and paired['overall_acceptance'] is None,
            'Review the stated process limitations')
    diagnostic = {r['arm']: r['runs']['posthoc_surrogate']['result']
                  for r in execution['rows']}
    require(all(v['post_hoc'] and not v['changes_primary_score']
                for v in diagnostic.values()), 'Post-hoc scope changed')
    require(diagnostic['C']['saved'] and diagnostic['C']['text_equal_after_reload']
            and diagnostic['S']['saved'] is False
            and diagnostic['S']['error_type'] == 'UnicodeEncodeError',
            'Review the Unicode diagnostic caveat')
    require(study['posthoc_F8_surrogate_diagnostic'] == {
        'C': 'passed', 'S': 'UnicodeEncodeError on save', 'affects_primary_score': False
    }, 'Diagnostic status disagrees')
    require(status['sealed_codex_cli_pilot']['model_attempts'] == 0,
            'Review the sealed-pilot caveat')
    provenance = {path: hashlib.sha256(data).hexdigest()
                  for path, data in zip(SOURCES, raw)}
    return paired, study, delta, provenance


def text(x, y, value, size=24, fill=INK, weight=400, anchor='start', tracking=None):
    extra = f' letter-spacing="{tracking}"' if tracking is not None else ''
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{extra}>'
            f'{escape(str(value))}</text>')


def rule(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{LINE}"/>' if y1 == y2 else (
        f'<path d="M{x1} {y1}V{y2}" stroke="{LINE}"/>')


def bar(x, y, width, passed, total, color, height=22):
    # Each segment is one primary artifact-criterion group, starting at zero.
    gap = 4
    unit = (width - (total - 1) * gap) / total
    return '\n'.join(
        f'<rect x="{x + i * (unit + gap):.2f}" y="{y}" '
        f'width="{unit:.2f}" height="{height}" rx="2" '
        f'fill="{color if i < passed else LINE}"/>' for i in range(total))


def render(paired, study, delta, provenance, mobile=False):
    w, h = (600, 832) if mobile else (1280, 580)
    title = 'Native-cloud study: no measured primary-criterion uplift'
    desc = (f"{paired['first_submissions']} actual native-agent first submissions on "
            f"{paired['scheduled_cases']} paired fictional cases. C received no designated "
            'package; S received the designated package. Both passed '
            f"{paired['C']['passed']}/{paired['C']['total']} primary artifact-criterion "
            f"groups and {study['C']['cases_all_primary_artifact_groups_passed']}/"
            f"{study['C']['cases']} artifacts. {delta:g} percentage-point pass-rate "
            'difference. Ceiling tie; no demonstrated uplift. Shared ambient runtime; '
            'C was not skill-free. Process integrity unverified. A separate post-hoc '
            'F8 Unicode save/reload check passed in C and failed with UnicodeEncodeError '
            'in S; it does not alter primary scores. No productivity claim.')
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
             f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
             f'<title id="title">{escape(title)}</title>',
             f'<desc id="desc">{escape(desc)}</desc>',
             '<metadata>' + escape(json.dumps({'renderer':
                'evaluation/visualization/render_native_results.py',
                'source_sha256': provenance}, sort_keys=True)) + '</metadata>',
             f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" '
             f'fill="{BG}" stroke="{LINE}"/>',
             '<g font-family="Arial, Helvetica, sans-serif">']
    p = parts.append
    if mobile:
        p(f'<circle cx="37" cy="40" r="5" fill="{ORANGE}"/>')
        p(text(53, 47, 'DOT-SKILLS / EVALUATION', 20, MUTED, 700, tracking=1))
        p(text(32, 116, 'Same tasks.', 48, weight=700, tracking=-1.5))
        p(text(32, 172, 'Same primary score.', 48, weight=700, tracking=-1.5))
        p(text(32, 220, f"{paired['first_submissions']} actual native-agent attempts", 26, MUTED))
        p(text(32, 256, f"{paired['scheduled_cases']} paired fictional tasks · 06 Oct 2026", 26, MUTED))
        p(rule(32, 287, 568, 287))
        p(text(32, 328, 'PRIMARY ARTIFACT CRITERION GROUPS', 20, MUTED, 700, tracking=.4))
        for arm, y, label, color in [('C', 376, 'C · No designated package', INK),
                                     ('S', 474, 'S · Designated package supplied', SAGE)]:
            p(text(32, y, label, 25, color, 700))
            p(text(568, y, f"{paired[arm]['passed']}/{paired[arm]['total']}", 30,
                   color, 700, 'end'))
            p(bar(32, y + 22, 536, paired[arm]['passed'], paired[arm]['total'], color))
        p(rule(32, 552, 568, 552))
        p(text(32, 654, f'{delta:g}', 100, weight=700, tracking=-5))
        p(text(96, 650, 'pp', 38, MUTED, 700))
        p(text(202, 611, 'Primary pass-rate', 28, weight=700))
        p(text(202, 648, 'difference', 28, weight=700))
        p(text(32, 704, f"{study['C']['cases_all_primary_artifact_groups_passed']}/{study['C']['cases']} met primary checks in each arm", 27, MUTED))
        p(rule(32, 742, 568, 742))
        p(text(32, 778, 'Exploratory study · Process unverified', 24, MUTED))
        p(text(32, 810, 'Read the limits + post-hoc finding below', 23, MUTED))
    else:
        p(f'<circle cx="53" cy="47" r="5" fill="{ORANGE}"/>')
        p(text(70, 54, 'DOT-SKILLS / EVALUATION', 20, MUTED, 700, tracking=1.2))
        p(text(1232, 54, '06 OCT 2026', 20, MUTED, 700, 'end', 1.2))
        p(text(48, 127, 'Same tasks. Same primary score.', 55, weight=700, tracking=-1.7))
        p(text(48, 173, f"{paired['first_submissions']} actual native-agent attempts · {paired['scheduled_cases']} paired fictional tasks", 28, MUTED))
        p(rule(48, 210, 1232, 210))
        p(text(48, 251, 'PRIMARY ARTIFACT CRITERION GROUPS', 20, MUTED, 700, tracking=.8))
        for arm, y, label, color in [('C', 303, 'C · No designated package', INK),
                                     ('S', 413, 'S · Designated package supplied', SAGE)]:
            p(text(48, y, label, 28, color, 700))
            p(text(810, y, f"{paired[arm]['passed']}/{paired[arm]['total']}", 36,
                   color, 700, 'end'))
            p(bar(48, y + 24, 762, paired[arm]['passed'], paired[arm]['total'], color, 26))
        p(rule(866, 245, 866, 468))
        p(text(920, 354, f'{delta:g}', 120, weight=700, tracking=-5))
        p(text(1000, 352, 'pp', 42, MUTED, 700))
        p(text(920, 400, 'Primary pass-rate', 28, weight=700))
        p(text(920, 438, 'difference', 28, weight=700))
        p(rule(48, 500, 1232, 500))
        p(text(48, 546, f"{study['C']['cases_all_primary_artifact_groups_passed']}/{study['C']['cases']} met primary checks in each arm", 25, weight=700))
        p(text(1232, 546, 'Exploratory study · Process integrity unverified', 23, MUTED, anchor='end'))
    p('</g>\n</svg>\n')
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='verify SVGs without changing files')
    args = parser.parse_args()
    data = load_data()
    for mobile in (False, True):
        name = 'native-results-mobile.svg' if mobile else 'native-results.svg'
        path = ROOT / '.github' / 'assets' / name
        expected = render(*data, mobile=mobile)
        if args.check:
            require(path.exists() and path.read_text(encoding='utf-8') == expected,
                    f'{path.relative_to(ROOT)} is stale; rerun this renderer')
            print(f'Checked {path.relative_to(ROOT)}')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding='utf-8')
            print(f'Wrote {path.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
