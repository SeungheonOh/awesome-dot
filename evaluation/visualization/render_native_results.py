#!/usr/bin/env python3
"""Render the README's evidence-led native-cloud panels using the Python stdlib.

From the repository root:
    python -B evaluation/visualization/render_native_results.py
    python -B evaluation/visualization/render_native_results.py --check

Reads the published summary, status, F6 CSVs and F8 execution-result records.
The display selects CSV columns and JSON fields; it is an excerpt, not a screenshot.
Values are loaded from saved files, not invented console output. No model calls,
candidate execution, external assets, fonts, dependencies or network are needed.
Both SVGs include source-file SHA-256 hashes and field-selection provenance.
--check verifies committed bytes.
This is a deliberately study-specific layout: changed findings fail validation so
its headline and post-hoc caveat cannot silently become stale.
"""

import argparse
import csv
import io
import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY = 'evaluation/results/native-cloud-2026-10-06'
SOURCES = (f'{STUDY}/paired-summary.json', 'evaluation/results/status.json',
           f'{STUDY}/f8/execution-results.json',
           f'{STUDY}/artifacts/N09-F6-C/result.csv',
           f'{STUDY}/artifacts/N10-F6-S/result.csv')
BG, INK, MUTED, LINE = '#F5F3EC', '#1B2820', '#566159', '#D3D8CE'
PAPER, SOFT, ERROR, ERROR_BG = '#FFFEFA', '#E9EDE4', '#98401F', '#F9E9E0'
SAGE, ORANGE = '#57735F', '#DB532C'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_data():
    raw = [(ROOT / path).read_bytes() for path in SOURCES]
    paired, status, execution = [json.loads(data) for data in raw[:3]]
    csv_rows = [list(csv.DictReader(io.StringIO(data.decode('utf-8')))) for data in raw[3:]]
    require(raw[3] == raw[4], 'Review the identical-CSV statement')
    require([r['channel'] for r in csv_rows[0]] ==
            ['__unallocated__', 'desk', 'phone', 'web'], 'Review the CSV layout')
    phone = next(r for r in csv_rows[0] if r['channel'] == 'phone')
    require(phone['gross_minor'] == phone['net_minor'] == 'NULL',
            'Review the unknown-total headline')
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
    require(diagnostic['S']['error'].endswith('surrogates not allowed'),
            'Review the quoted error-message suffix')
    provenance = {path: hashlib.sha256(data).hexdigest()
                  for path, data in zip(SOURCES, raw)}
    return paired, study, delta, provenance, csv_rows[0], diagnostic


def text(x, y, value, size=24, fill=INK, weight=400, anchor='start', mono=False, tracking=None):
    extra = f' letter-spacing="{tracking}"' if tracking is not None else ''
    if mono:
        extra += ' font-family="monospace"'
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{extra}>'
            f'{escape(str(value))}</text>')


def rect(x, y, w, h, fill=PAPER, radius=12, stroke=LINE):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}"/>')


def rule(x1, y, x2):
    return f'<path d="M{x1} {y}H{x2}" stroke="{LINE}"/>'


def field(value):
    return str(value).lower() if isinstance(value, bool) else str(value)


def render(paired, study, delta, provenance, csv_rows, diagnostic, mobile=False):
    w, h = (400, 1178) if mobile else (1280, 786)
    title = 'The score ties. Inspect the files.'
    desc = (f"{paired['first_submissions']} actual native-agent runs on "
            f"{paired['scheduled_cases']} paired fictional tasks, 6 October 2026. "
            'Saved-file excerpts, not screenshots. C: no designated package. '
            'S: designated package supplied. Both F6 result.csv files are identical; '
            'selected columns are channel, gross_minor, refund_minor, and net_minor, '
            'with shortened display headings. Phone gross and net are NULL. '
            'A separate post-hoc F8 diagnostic with U+D800 followed by LF saved and '
            'reloaded text in C, but S failed to save with UnicodeEncodeError. '
            'Selected JSON fields are transcribed from execution-results.json. '
            f"Both arms passed {paired['C']['passed']}/{paired['C']['total']} primary "
            f"artifact-criterion groups and {study['C']['cases_all_primary_artifact_groups_passed']}/"
            f"{study['C']['cases']} artifacts. {delta:g} percentage-point pass-rate difference, "
            'no measured uplift. Post-hoc findings do not change primary scores. '
            'Shared runtime; C was not skill-free. Process integrity unverified.')
    metadata = {'renderer': 'evaluation/visualization/render_native_results.py',
                'source_sha256': provenance,
                'excerpts': [
                    {'paths': list(SOURCES[3:]), 'rows': 'all four data rows',
                     'columns': ['channel', 'gross_minor', 'refund_minor', 'net_minor'],
                     'display_headings': ['CHANNEL', 'GROSS', 'REFUNDS', 'NET'],
                     'display': 'CSV values reformatted as a table; integer minor units'},
                    {'path': SOURCES[2], 'selector': 'rows[*].runs.posthoc_surrogate.result',
                     'fields': ['input', 'saved', 'text_equal_after_reload', 'error_type'],
                     'error_excerpt': 'surrogates not allowed',
                     'display': 'selected saved JSON fields; error message suffix quoted'}]}
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
             f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
             f'<title id="title">{escape(title)}</title>',
             f'<desc id="desc">{escape(desc)}</desc>',
             '<metadata>' + escape(json.dumps(metadata, sort_keys=True)) + '</metadata>',
             rect(.5, .5, w-1, h-1, BG, 18),
             '<g font-family="Arial, Helvetica, sans-serif">']
    p = parts.append
    # The panels have a fixed, study-specific layout. Validation above fails if
    # changed evidence would invalidate any prose or the intended visual order.
    if mobile:
        p(text(22, 35, 'DOT-SKILLS / RUN EVIDENCE', 13, MUTED, 700, tracking=1))
        p(text(22, 82, 'The score ties.', 33, weight=700, tracking=-1))
        p(text(22, 122, 'Inspect the files.', 33, weight=700, tracking=-1))
        p(text(22, 158, f"{paired['first_submissions']} actual runs · {paired['scheduled_cases']} paired fictional tasks", 16, MUTED))
        p(text(22, 184, '06 Oct 2026 · Excerpts, not screenshots', 15, MUTED))
        # F6: full row coverage, four selected columns. No fake terminal chrome.
        p(rect(16, 210, 368, 347))
        p(text(34, 241, 'F6 / SQLITE REPORT', 13, MUTED, 700, tracking=.7))
        p(text(34, 278, 'Missing totals stay unknown', 23, weight=700, tracking=-.5))
        p(text(34, 307, 'C + S saved identical CSVs', 17, MUTED))
        p(text(34, 333, 'Selected columns · integer minor units', 14, MUTED))
        heads=[('CHANNEL',34,'start'),('GROSS',225,'end'),('REFUNDS',299,'end'),('NET',365,'end')]
        for label,x,anchor in heads:p(text(x,365,label,11,MUTED,700,anchor,tracking=.2))
        p(rule(34,378,366))
        for idx,row in enumerate(csv_rows):
            y=397+idx*38
            # phone is the third row; highlight only that saved record.
            if row['channel']=='phone':
                p(rect(27,y-23,346,36,SOFT,0,SOFT))
            p(text(34,y,row['channel'],13,weight=700 if row['channel']=='phone' else 400,mono=True))
            for key,x in [('gross_minor',225),('refund_minor',299),('net_minor',365)]:
                p(text(x,y,row[key],15,weight=700 if row[key]=='NULL' else 400,anchor='end',mono=True))
        p(text(34,537,'Phone gross + net are NULL in both outputs',14,MUTED))
        # F8: directly transcribed fields, with the same C/S ordering.
        p(rect(16,575,368,387))
        p(text(34,606,'F8 / TEXT-MERGE CALLER',13,MUTED,700,tracking=.7))
        p(text(34,643,'A save fails after primary checks',22,weight=700,tracking=-.7))
        p(text(34,672,'Post-hoc result excerpt · U+D800 + LF',15,MUTED))
        p(rule(34,690,366))
        p(text(34,718,'C · NO DESIGNATED PACKAGE',12,MUTED,700,tracking=.5))
        p(text(34,746,'saved: '+field(diagnostic['C']['saved']),16,mono=True))
        p(text(34,774,'text_equal_after_reload: '+field(diagnostic['C']['text_equal_after_reload']),15,mono=True))
        p(rule(34,792,366))
        p(text(34,819,'S · DESIGNATED PACKAGE SUPPLIED',12,MUTED,700,tracking=.4))
        p(text(34,847,'saved: '+field(diagnostic['S']['saved']),16,mono=True))
        p(text(34,875,'error_type: '+diagnostic['S']['error_type'],14,ERROR,700,mono=True))
        p(rect(30,895,340,46,ERROR_BG,6,ERROR_BG))
        p(text(43,924,'“surrogates not allowed”',17,ERROR,mono=True))
        p(text(22,1000,'PRIMARY ARTIFACT CRITERION GROUPS',12,MUTED,700,tracking=.5))
        p(text(22,1035,f"C {paired['C']['passed']}/{paired['C']['total']}  ·  S {paired['S']['passed']}/{paired['S']['total']}",25,weight=700))
        p(text(22,1064,f"{paired['scheduled_cases']} tied pairs · {delta:g} pp pass-rate difference",16,MUTED))
        p(text(22,1092,f"{study['C']['cases_all_primary_artifact_groups_passed']}/{study['C']['cases']} artifacts met primary checks in each arm",15,MUTED))
        p(rule(22,1112,378))
        p(text(22,1139,'Post-hoc result does not change primary scores',14,MUTED))
        p(text(22,1161,'Exploratory study · Process integrity unverified',14,MUTED))
    else:
        p(text(40,42,'DOT-SKILLS / RUN EVIDENCE',18,MUTED,700,tracking=1.2))
        p(text(1240,42,'06 OCT 2026',18,MUTED,700,'end',tracking=1))
        p(text(40,107,title,48,weight=700,tracking=-1.5))
        p(text(40,150,f"{paired['first_submissions']} actual native-agent runs · {paired['scheduled_cases']} paired fictional tasks · Excerpts, not screenshots",23,MUTED))
        p(rect(40,184,586,408))
        p(text(64,221,'F6 / SQLITE REPORT',16,MUTED,700,tracking=.8))
        p(text(64,262,'Missing totals stay unknown',30,weight=700,tracking=-.5))
        p(text(64,297,'C + S saved identical CSVs',22,MUTED))
        p(text(64,326,'Selected columns · integer minor units',18,MUTED))
        for label,x,anchor in [('CHANNEL',64,'start'),('GROSS',368,'end'),('REFUNDS',476,'end'),('NET',600,'end')]:
            p(text(x,363,label,14,MUTED,700,anchor,tracking=.5))
        p(rule(64,378,602))
        for idx,row in enumerate(csv_rows):
            y=407+idx*43
            if row['channel']=='phone':p(rect(52,y-29,562,42,SOFT,0,SOFT))
            p(text(64,y,row['channel'],20,weight=700 if row['channel']=='phone' else 400,mono=True))
            for key,x in [('gross_minor',368),('refund_minor',476),('net_minor',600)]:
                p(text(x,y,row[key],22,weight=700 if row[key]=='NULL' else 400,anchor='end',mono=True))
        p(text(64,574,'Phone gross + net are NULL in both outputs',19,MUTED))
        p(rect(646,184,594,408))
        p(text(670,221,'F8 / TEXT-MERGE CALLER',16,MUTED,700,tracking=.8))
        p(text(670,262,'A save fails after primary checks',30,weight=700,tracking=-.5))
        p(text(670,297,'Post-hoc result excerpt · U+D800 + LF',22,MUTED))
        p(rule(670,316,1216))
        p(text(670,345,'C · NO DESIGNATED PACKAGE',15,MUTED,700,tracking=.5))
        p(text(670,378,'saved: '+field(diagnostic['C']['saved']),20,mono=True))
        p(text(670,409,'text_equal_after_reload: '+field(diagnostic['C']['text_equal_after_reload']),20,mono=True))
        p(rule(670,429,1216))
        p(text(670,458,'S · DESIGNATED PACKAGE SUPPLIED',15,MUTED,700,tracking=.5))
        p(text(670,491,'saved: '+field(diagnostic['S']['saved']),20,mono=True))
        p(text(670,522,'error_type: '+diagnostic['S']['error_type'],20,ERROR,700,mono=True))
        p(rect(666,540,554,38,ERROR_BG,6,ERROR_BG))
        p(text(680,566,'“surrogates not allowed”',20,ERROR,mono=True))
        p(text(40,632,'PRIMARY ARTIFACT CRITERION GROUPS',16,MUTED,700,tracking=.6))
        p(text(40,675,f"C {paired['C']['passed']}/{paired['C']['total']}  ·  S {paired['S']['passed']}/{paired['S']['total']}",32,weight=700))
        p(text(414,672,f"{paired['scheduled_cases']} tied pairs · {delta:g} pp pass-rate difference",23,MUTED))
        p(text(1240,675,f"{study['C']['cases_all_primary_artifact_groups_passed']}/{study['C']['cases']} passed artifacts per arm",23,MUTED,anchor='end'))
        p(rule(40,707,1240))
        p(text(40,751,'Post-hoc result does not change primary scores',20,MUTED))
        p(text(1240,751,'Exploratory study · Process integrity unverified',20,MUTED,anchor='end'))
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
