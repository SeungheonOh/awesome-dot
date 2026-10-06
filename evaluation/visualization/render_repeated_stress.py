#!/usr/bin/env python3
"""Render the frozen repeated-stress study. Run from the repository root:

    python -B evaluation/visualization/render_repeated_stress.py
    python -B evaluation/visualization/render_repeated_stress.py --check

This study-specific renderer checks exact source hashes and reconciles every
attempt and paired count. It renders saved JSON fields, not screenshots. It
executes no candidate code and uses only the Python standard library. A changed
finding or changed artifact requires reviewed selection and binding updates.
"""
import argparse
import hashlib
import json
import textwrap
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY = 'evaluation/studies/repeated-stress-2026-10-06'
BG, INK, MUTED, LINE = '#F5F3EC', '#1B2820', '#566159', '#D3D8CE'
PAPER, SOFT, RUST, RUST_BG = '#FFFEFA', '#E9EDE4', '#98401F', '#F9E9E0'
SAGE, GOLD, GOLD_BG = '#57735F', '#826320', '#F4EBD4'
EXPECTED_CASES = ('R1','R2','R3','R4')
CHECKS = ('pass','fail','not_assessed')
EXPECTED_INPUTS = {
 'results/attempts.json': 'd73aacde955733ef35d461e2519fceb44dbb52d45aed3eea5a50b7607326cc24',
 'results/requirements.json': '8cbf82e7ec847e8307fb89275924e9db414f3d98996e43c2b83aa0e03f583d54',
 'results/summary.json': '8c5dbff6ab099098028b02949e17ca0f71a7a19b60550a2a3c97c497154a2d74',
}

def require(ok, why):
    if not ok: raise ValueError(why)

def sha(raw): return hashlib.sha256(raw).hexdigest()

def read_source(root,path,expected=None):
    p=(root/path).resolve()
    require(p.is_relative_to(root.resolve()),'Source escaped repository')
    raw=p.read_bytes()
    if expected: require(sha(raw)==expected,'Source hash mismatch: '+path)
    return raw

def counts(attempt):
    return Counter(q['status'] for q in attempt['checks'])

def paired(c,s):
    cc,ss=counts(c),counts(s)
    if c['status'] == 'planned' or s['status'] == 'planned':
        return 'not run'
    if cc['not_assessed'] or ss['not_assessed']:
        return 'unresolved'
    d=ss['pass']-cc['pass']
    return 'tie' if d == 0 else 'different count'

def delta_label(c,s):
    if c['status']=='planned' or s['status']=='planned':return 'not run'
    return 'Δ '+str(counts(s)['pass']-counts(c)['pass'])

def outcome(a):
    n=counts(a)
    if a['status'] != 'completed':
        return a['status'].replace('_',' ')
    if n['fail']:
        return 'incomplete'
    if n['not_assessed']:
        return 'unverified'
    return 'all verified'

def text(x,y,value,size=20,fill=INK,weight=400,anchor='start',mono=False):
    font='monospace' if mono else 'Arial, Helvetica, sans-serif'
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>'

def rect(x,y,w,h,fill=PAPER,stroke=LINE,rx=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'

def rule(x,y,w):
    return f'<path d="M{x} {y}h{w}" stroke="{LINE}"/>'

def begin(data,w,h,title,description):
    meta={k:data[k] for k in ['study_id','data_state','canonical_sources']}
    meta['excerpts']=[{k:v for k,v in e.items() if not k.startswith('_')} for e in data.get('excerpts',[])]
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',f'<desc id="desc">{escape(description)}</desc>',
            '<metadata>'+escape(json.dumps(meta,sort_keys=True))+'</metadata>',rect(.5,.5,w-1,h-1,BG,LINE,18)]

def footer(parts,y,mobile,preview=False):
    x=22 if mobile else 40
    if preview:
        lines=['LAYOUT PREVIEW · NO RESULTS','Placeholders are not study outcomes.']
    else:
        lines=['Synthetic workflows · Shared runtime','C is not skill-free. Process integrity unknown.']
    if mobile:
        for i,line in enumerate(lines):parts.append(text(x,y+i*23,line,15,MUTED,700 if preview else 400))
    else:
        parts.append(text(x,y,' · '.join(lines),19,MUTED,700 if preview else 400))

def legend(parts,y,mobile):
    x=22 if mobile else 40
    if mobile:
        for i,line in enumerate(['C · No designated package','S · Designated package supplied','✓ verified pass   × fail   ? not assessed']):
            parts.append(text(x,y+i*25,line,15,MUTED))
    else:
        parts.append(text(x,y,'C · No designated package   |   S · Designated package supplied',20,MUTED))
        parts.append(text(x,y+30,'✓ verified pass     × fail     ? not assessed',18,MUTED))

def ledger(data,mobile=False):
    preview=data['data_state']=='placeholder'
    extras=sum(any(a['status'] not in {'completed','planned'} for a in data['attempts'] if a['case_id']==c and a['repeat']==r) for c in EXPECTED_CASES for r in [1,2,3])
    w,h=(375,1310+extras*19) if mobile else (1280,947)
    desc=('Layout preview only. No study outcomes. ' if preview else '')
    desc+='Every scheduled first submission, shown by synthetic workflow and repeat. C means no designated package; S means designated package supplied. Ratios show verified passes over scheduled requirements; not-assessed checks are neither passes nor defects. Four task families, not twelve independent task samples. Shared runtime and instruction-only separation; process integrity unknown. '
    by={(a['case_id'],a['repeat'],a['arm']):a for a in data['attempts']}
    for c in data['cases']:
        for r in [1,2,3]:
            for arm in 'CS':
                a=by[c['case_id'],r,arm]; n=counts(a)
                desc+=f"{a['attempt_id']}, {c['label']}, repeat {r}, {arm}: "+('planned; no result. ' if preview else f"{n['pass']} passed, {n['fail']} failed, {n['not_assessed']} not assessed; {a['status']}. ")
    title='Every run, side by side.'
    p=begin(data,w,h,title,desc)
    x=22 if mobile else 40
    p.append(text(x,34 if mobile else 40,'DOT-SKILLS / REPEATED RUNS',13 if mobile else 17,MUTED,700))
    if mobile:
        p.append(text(x,75,'Every run,',32,weight=700));p.append(text(x,113,'side by side.',32,weight=700))
        p.append(text(x,145,f"{len(data['cases'])} synthetic workflows · {len(data['repeats'])} repeats",16,MUTED))
        legend(p,180,True)
        p.append(text(22,254,'Ratios: passed / scheduled · Δ = S − C',15,MUTED))
        offset=25
        for i,c in enumerate(data['cases']):
            extra=sum(any(by[c['case_id'],r,arm]['status'] not in {'completed','planned'} for arm in 'CS') for r in [1,2,3])
            y=258+i*236+offset
            p.append(rect(16,y,343,222+extra*19))
            p.append(text(30,y+31,c['case_id']+' / '+c['label'],17,weight=700))
            rowoffset=0
            for j,r in enumerate([1,2,3]):
                yy=y+65+j*54+rowoffset
                aa=[by[c['case_id'],r,arm] for arm in 'CS']
                p.append(text(30,yy,'#'+str(r),14,MUTED,700))
                p.append(text(30,yy+21,delta_label(*aa),12,MUTED))
                rowextra=any(a['status'] not in {'completed','planned'} for a in aa)
                for a,xx in zip(aa,[99,237]):
                    n=counts(a); total=len(a['checks'])
                    p.append(text(xx,yy,a['arm'],17,weight=700))
                    p.append(text(xx+25,yy,'—' if preview else f"{n['pass']}/{total}",21,weight=700))
                    if preview:p.append(text(xx,yy+23,'not run',15,MUTED))
                    else:
                        p.append(text(xx,yy+23,f"× {n['fail']}",15,RUST if n['fail'] else MUTED))
                        p.append(text(xx+55,yy+23,f"? {n['not_assessed']}",15,MUTED))
                    if rowextra and a['status']!='completed':p.append(text(xx,yy+41,a['status'].replace('_',' '),13,RUST))
                if j<2:p.append(rule(30,yy+32+19*rowextra,314))
                rowoffset+=19*rowextra
            offset+=extra*19
        footer(p,1259+extras*19,True,preview)
    else:
        p.append(text(x,101,title,44,weight=700))
        p.append(text(x,140,f"{len(data['attempts'])} native-agent attempts · {len(data['cases'])} synthetic workflows · {len(data['repeats'])} repeats per condition",23,MUTED))
        legend(p,180,False)
        p.append(text(1240,210,'Ratios: passed / scheduled · Δ = S − C',18,MUTED,anchor='end'))
        for j,r in enumerate([1,2,3]):p.append(text(481+j*305,257,'REPEAT '+str(r),17,MUTED,700,'middle'))
        for i,c in enumerate(data['cases']):
            y=281+i*132
            p.append(rect(28,y,1224,116))
            p.append(text(49,y+33,c['case_id'],15,MUTED,700))
            lines=textwrap.wrap(c['label'],23)
            for n,line in enumerate(lines):p.append(text(49,y+63+n*28,line,23,weight=700))
            for j,r in enumerate([1,2,3]):
                xx=348+j*305; aa=[by[c['case_id'],r,arm] for arm in 'CS']
                for a,xxx in zip(aa,[xx,xx+146]):
                    n=counts(a);total=len(a['checks'])
                    p.append(text(xxx,y+40,a['arm'],20,weight=700))
                    p.append(text(xxx+28,y+40,'—' if preview else f"{n['pass']}/{total}",27,weight=700))
                    if preview:p.append(text(xxx,y+72,'not run',18,MUTED))
                    else:
                        p.append(text(xxx,y+72,f"× {n['fail']}",18,RUST if n['fail'] else MUTED))
                        p.append(text(xxx+58,y+72,f"? {n['not_assessed']}",18,MUTED))
                    if a['status'] not in {'completed','planned'}:p.append(text(xxx,y+92,a['status'].replace('_',' '),13,RUST))
                label=delta_label(*aa)+(' · '+paired(*aa) if not preview else '')
                p.append(text(xx+129,y+109,label,14,MUTED,anchor='middle'))
        p.append(rule(40,832,1200))
        footer(p,870,False,preview)
    return '\n'.join(p+['</svg>'])+'\n'

def load_data(root):
    """Adapt the canonical public projection without changing a single score."""
    docs={};bindings=[]
    for path,expected in EXPECTED_INPUTS.items():
        full=f'{STUDY}/{path}';raw=read_source(root,full,expected)
        docs[path]=json.loads(raw);bindings.append({'path':full,'sha256':sha(raw)})
    rows=docs['results/attempts.json'];cases=docs['results/requirements.json'];summary=docs['results/summary.json']
    require(summary['status']=='final saved-evidence accounting','Final result seal required')
    require(summary['study_id']=='native-cloud-repeated-stress-2026-10-06','Wrong study')
    require(set(cases)==set(EXPECTED_CASES),'Expected exactly four authored cases')
    require(len(rows)==summary['scheduled_attempts']==24,'All 24 attempts must remain visible')
    require(len({a['attempt_id'] for a in rows})==24,'Duplicate attempt ID')
    slots={(a['case_id'],a['repeat'],a['condition']) for a in rows}
    require(slots=={(c,r,a) for c in EXPECTED_CASES for r in [1,2,3] for a in 'CS'},'Missing or duplicate attempt slot')
    by={a['attempt_id']:a for a in rows};normalized=[]
    modes={k:Counter() for k in ['objective','semantic','behavioral']}
    for a in rows:
        reqs=a['requirements'];expected=cases[a['case_id']]['requirements']
        require(len(reqs)==len(expected)==a['scheduled_requirements'],'Scheduled denominator mismatch')
        require({q['requirement_id'] for q in reqs}=={q['requirement_id'] for q in expected},'Requirement IDs mismatch')
        definitions={q['requirement_id']:q for q in expected}
        for q in reqs:
            require(q['status'] in CHECKS and q['mode']==definitions[q['requirement_id']]['mode'],'Status/mode mismatch')
            require(q['evidence_path'],'Verified score lacks an evidence path')
            modes[q['mode']][q['status']]+=1
        counts_=Counter(q['status'] for q in reqs)
        require(a['counts']=={s:counts_[s] for s in CHECKS},'Attempt counts disagree')
        require(a['completed_criteria']==(counts_['pass']==len(reqs)),'Completion flag disagrees')
        require(a['submission_status']=='completed','Review operational-failure layout')
        require(a['process_integrity']=='unknown','Review process-integrity caveat')
        normalized.append({'attempt_id':a['attempt_id'],'case_id':a['case_id'],'repeat':a['repeat'],'arm':a['condition'],'status':a['submission_status'],'checks':reqs})
    require(len(cases)==summary['authored_cases'],'Case count mismatch')
    require(sum(len(c['requirements']) for c in cases.values())==summary['distinct_requirements'],'Distinct count mismatch')
    require(sum(len(a['requirements']) for a in rows)==summary['scheduled_requirement_instances'],'Instance count mismatch')
    for mode,totals in modes.items():require(summary['evidence_coverage'][mode]=={s:totals[s] for s in CHECKS},'Coverage disagrees')
    for arm in 'CS':
        group=[a for a in rows if a['condition']==arm];t=Counter(q['status'] for a in group for q in a['requirements'])
        require(summary['conditions'][arm]['counts']=={s:t[s] for s in CHECKS},'Condition counts disagree')
        require(summary['conditions'][arm]['scheduled_requirements']==sum(len(a['requirements']) for a in group),'Condition denominator disagrees')
    require(len(summary['pairs'])==summary['case_repeat_pairs']==12,'Paired count mismatch')
    for pair in summary['pairs']:
        for arm in 'CS':
            a=by[pair[arm]['attempt_id']]
            require((a['case_id'],a['repeat'],a['condition'])==(pair['case_id'],pair['repeat'],arm),'Paired ID mismatch')
            require({s:pair[arm][s] for s in CHECKS}==a['counts'],'Paired score mismatch')
        require(pair['verified_pass_difference_S_minus_C']==pair['S']['pass']-pair['C']['pass'],'Paired delta mismatch')
    require(all(a['counts']['fail']==a['counts']['not_assessed']==0 for a in rows),'Observed misses require reviewed failure-first selection; do not use no-failure fallback')
    require(all(p['verified_pass_difference_S_minus_C']==0 for p in summary['pairs']),'Review tie wording')
    excerpts=[]
    configs=[('R1','reconciliation.json','claims','claim_id',['C007','C026'],['disposition','duplicate_of','reimbursement_usd_cents','approved_usd_cents','held_usd_cents']),
             ('R2','action_register.json','actions','action_id',['A21','A30'],['owner','status','due_date','overdue'])]
    for cid,filename,collection,idkey,ids,fields in configs:
        group=sorted((a for a in rows if a['case_id']==cid),key=lambda a:a['dispatch_index'])
        first=group[0];all_values=[];all_totals=[];record_counts=[];source_records=[]
        for a in group:
            rel=f"artifacts/{a['attempt_id']}/{filename}"
            binding=next(v for v in a['artifacts'] if v['path']==rel)
            full=f'{STUDY}/{rel}';raw=read_source(root,full,binding['sha256'])
            require(len(raw)==binding['bytes'],'Artifact byte count mismatch')
            bindings.append({'path':full,'sha256':sha(raw)})
            artifact=json.loads(raw);records=artifact[collection]
            if cid=='R2':
                require(dict(Counter(r['status'] for r in records))==artifact['totals']['by_status'],'Action status totals disagree')
                active=[r for r in records if r['status'] in {'open','blocked','unresolved'}]
                require(len(active)==artifact['totals']['active_count'],'Active action total disagrees')
                require(sum(r['overdue'] for r in records)==sum(r['overdue'] for r in active)==artifact['totals']['overdue_count'],'Overdue subset summary disagrees')
            all_totals.append(artifact['totals']);record_counts.append(len(records))
            selected=[]
            for rid in ids:
                matches=[r for r in records if r[idkey]==rid];require(len(matches)==1,'Selected record missing or duplicated')
                selected.append({idkey:rid,**{f:matches[0][f] for f in fields}})
            all_values.append(selected)
            source_records.append({'attempt_id':a['attempt_id'],'condition':a['condition'],'path':full,'sha256':sha(raw)})
        require(all(v==all_values[0] for v in all_values),'Review selected-field equivalence statement')
        require(all(v==all_totals[0] for v in all_totals),'Review summary-total equivalence statement')
        require(all(v==record_counts[0] for v in record_counts),'Review source record-count statement')
        chosen=source_records[0];raw=read_source(root,chosen['path'],chosen['sha256']);lines=raw.decode().splitlines()
        ranges=[]
        for rid in ids:
            lo=next(i for i,line in enumerate(lines,1) if f'"{idkey}": "{rid}"' in line)
            hi=next(i for i in range(lo,len(lines)) if lines[i].startswith('    }'))+1
            ranges.append({'record_id':rid,'line_start':lo,'line_end':hi})
        totals_lo=next(i for i,line in enumerate(lines,1) if line.startswith('  "totals":'))
        totals_hi=next(i for i in range(totals_lo,len(lines)) if lines[i].startswith('  }'))+1
        paired_=next(a for a in group if a['repeat']==first['repeat'] and a['condition']!=first['condition'])
        excerpts.append({'case_id':cid,'attempt_id':first['attempt_id'],'condition':first['condition'],'repeat':first['repeat'],
                         'path':chosen['path'],'sha256':chosen['sha256'],'paired_path':f"{STUDY}/artifacts/{paired_['attempt_id']}/{filename}",
                         'collection':collection,'id_field':idkey,'fields':fields,'records':all_values[0],'source_lines':ranges,
                         'totals':all_totals[0],'record_count':record_counts[0],'totals_source_lines':{'line_start':totals_lo,'line_end':totals_hi},
                         'verified_matches':source_records,'selection_reason':'No-failure fallback; lowest dispatch-index successful attempt in R1/R2. Selected business fields illustrate duplicate/unvalued claims and unresolved/missing-date actions; no condition-based selection.'})
    return {'study_id':summary['study_id'],'data_state':'frozen','cases':[cases[c] for c in EXPECTED_CASES],'attempts':normalized,
            'repeats':[1,2,3],'canonical_sources':bindings,'excerpts':excerpts,'summary':summary}

def coverage(data,mobile=False):
    w,h=(375,914) if mobile else (1280,710)
    counts_by_case={c['case_id']:Counter(q['mode'] for q in c['requirements']) for c in data['cases']}
    desc='Distinct predeclared requirements by synthetic workflow. Each requirement is checked on three repetitions in each condition, six instances. These are four authored cases, not twelve independent task samples. Mechanical and behavioral checks are separate from AI semantic ratings. '
    for c in data['cases']:
        n=counts_by_case[c['case_id']];desc+=f"{c['label']}: {n['objective']} mechanical, {n['behavioral']} behavioral, {n['semantic']} AI semantic requirements. "
    desc+='Semantic requirements received two source-grounded AI ratings; this is not human evaluation. Process integrity remains unknown.'
    p=begin(data,w,h,'What the checks cover.',desc);x=22 if mobile else 40
    p.append(text(x,35 if mobile else 40,'DOT-SKILLS / EVIDENCE COVERAGE',13 if mobile else 17,MUTED,700))
    p.append(text(x,81 if mobile else 98,'What the checks cover.',27 if mobile else 43,weight=700))
    p.append(text(x,114 if mobile else 139,'Distinct requirements, by workflow',16 if mobile else 23,MUTED))
    styles=[('objective','Mechanical',SAGE,SAGE),('behavioral','Behavioral',INK,INK),('semantic','AI semantic',GOLD_BG,GOLD)]
    for j,(_,label,fill,stroke) in enumerate(styles):
        xx=22 if mobile else 40+j*235;yy=147+j*27 if mobile else 184
        p.append(rect(xx,yy-13,13,13,fill,stroke,3));p.append(text(xx+23,yy,label,15 if mobile else 19,MUTED))
    for i,c in enumerate(data['cases']):
        yy=234+i*139 if mobile else 236+i*86
        p.append(rect(16 if mobile else 28,yy,343 if mobile else 1224,123 if mobile else 72))
        xx=30 if mobile else 48;n=counts_by_case[c['case_id']]
        p.append(text(xx,yy+29,c['case_id']+' / '+c['label'],17 if mobile else 22,weight=700))
        bx=xx if mobile else 503;by=yy+48 if mobile else yy+21;idx=0
        for mode,label,fill,stroke in styles:
            for _ in range(n[mode]):
                p.append(rect(bx+idx*(20 if mobile else 29),by,15 if mobile else 21,15 if mobile else 21,fill,stroke,3));idx+=1
        counttext=' · '.join(f"{n[mode]} {label if mode=='semantic' else label.lower()}" for mode,label,_,_ in styles if n[mode])
        p.append(text(xx if mobile else 503,yy+(99 if mobile else 60),counttext,15 if mobile else 18,MUTED))
    if mobile:
        p.append(text(22,822,'Each requirement checked in 6 runs:',15,MUTED))
        p.append(text(22,847,'3 repeats × 2 conditions',16,weight=700))
        p.append(text(22,879,'Four authored cases · AI-rated semantics',14,MUTED))
    else:
        p.append(text(40,628,'One block = one distinct requirement; each checked on 3 repeats × 2 conditions',21,MUTED))
        p.append(text(40,671,'Four authored cases · Semantic judgments are AI ratings · Process integrity unknown',19,MUTED))
    return '\n'.join(p+['</svg>'])+'\n'

def literal(value):
    if value is None:return 'null'
    if isinstance(value,bool):return str(value).lower()
    return str(value)

def usd(cents):
    require(type(cents) is int,'USD summary requires saved integer cents')
    sign='-' if cents<0 else '';whole,fraction=divmod(abs(cents),100)
    return f'USD {sign}{whole:,}.{fraction:02d}'

def evidence(data,mobile=False):
    w,h=(375,1597) if mobile else (1280,943)
    e1,e2=data['excerpts']
    desc='Selected saved JSON fields, reformatted for readability; not screenshots. Both excerpts are from condition C, meaning no designated package. '
    for e in data['excerpts']:
        desc+=f"{e['attempt_id']}, {e['path']}. Selected values: "+json.dumps(e['records'],ensure_ascii=False)+'. Saved totals: '+json.dumps(e['totals'],ensure_ascii=False)+'. '
    desc+='These selected fields match all three C and all three S artifacts within each case; this does not assert byte-identical files or quality beyond the displayed fields. No failed or unassessed requirements were observed in the frozen study. Synthetic workflows; shared runtime; process integrity unknown.'
    p=begin(data,w,h,'Decisions in the saved files.',desc);x=22 if mobile else 40
    p.append(text(x,35 if mobile else 40,'DOT-SKILLS / SAVED EVIDENCE',13 if mobile else 17,MUTED,700))
    if mobile:
        p.append(text(x,78,'Decisions in',29,weight=700));p.append(text(x,115,'the saved files.',29,weight=700))
        p.append(text(x,149,'Synthetic workflows · Selected JSON fields',15,MUTED))
        p.append(text(x,174,'Reformatted excerpts, not screenshots',15,MUTED))
    else:
        p.append(text(x,103,'Decisions in the saved files.',43,weight=700))
        p.append(text(x,146,'Synthetic workflows · Selected JSON fields · Reformatted excerpts, not screenshots',23,MUTED))
    for i,e in enumerate(data['excerpts']):
        xx=16 if mobile else 40+i*610;yy=202+i*646 if mobile else 184;cw=343 if mobile else 590;ch=625 if mobile else 607
        p.append(rect(xx,yy,cw,ch));tx=xx+18 if mobile else xx+24
        p.append(text(tx,yy+32,e['case_id']+' / '+e['attempt_id'],14 if mobile else 17,MUTED,700))
        title='Expense reconciliation' if i==0 else 'Dated action handoff'
        p.append(text(tx,yy+67,title,22 if mobile else 30,weight=700))
        p.append(text(tx,yy+95,'C · No designated package',15 if mobile else 19,MUTED))
        totals=e['totals']
        if i==0:
            require(len(totals['unvalued_holds'])==1,'Review unvalued-hold summary')
            unvalued=totals['unvalued_holds'][0]
            summaries=[('Payable',usd(totals['reimbursement_usd_cents'])),('Held, USD-valued',usd(totals['held_usd_cents'])),('Unvalued hold',unvalued['currency']+' '+unvalued['original_amount'])]
        else:
            summaries=[('Active actions',totals['active_count']),('Of these, overdue',totals['overdue_count']),('Done / cancelled',str(totals['by_status']['done'])+' / '+str(totals['by_status']['cancelled']))]
        for j,(label,value) in enumerate(summaries):
            p.append(text(tx,yy+129+j*26,label,14 if mobile else 18,MUTED))
            p.append(text(xx+cw-24,yy+129+j*26,value,16 if mobile else 22,weight=700,anchor='end'))
        p.append(rule(tx,yy+198,cw-(36 if mobile else 48)))
        rows=e['records']
        for j,row in enumerate(rows):
            ry=yy+223+j*(164 if mobile else 159)
            rid=row[e['id_field']];status=row['disposition' if i==0 else 'status']
            p.append(rect(tx-4,ry,cw-(28 if mobile else 40),148 if mobile else 144,SOFT,SOFT,8))
            p.append(text(tx+9,ry+30,rid+' / '+status,19 if mobile else 24,weight=700))
            if i==0:
                fields=[('duplicate_of','Duplicate of'),('reimbursement_usd_cents','Reimbursement (USD cents)')] if j==0 else [('approved_usd_cents','Approved USD cents'),('held_usd_cents','Held USD cents'),('reimbursement_usd_cents','Reimbursement (USD cents)')]
            else:fields=[('owner','Owner'),('due_date','Due date'),('overdue','Overdue')]
            for k,(key,label) in enumerate(fields):
                yy2=ry+63+k*28
                p.append(text(tx+9,yy2,label,14 if mobile else 18,MUTED))
                p.append(text(xx+cw-25,yy2,literal(row[key]),16 if mobile else 20,weight=700,anchor='end',mono=True))
        source_note=Path(e['path']).name
        p.append(text(tx,yy+(586 if mobile else 566),source_note,14 if mobile else 18,MUTED))
        note='Summary cents converted to USD' if i==0 else 'Values transcribed from saved fields'
        p.append(text(tx,yy+(607 if mobile else 591),note,14 if mobile else 17,MUTED))
    if mobile:
        p.append(text(22,1513,'Shown fields match all 3 C + 3 S repeats',15,weight=700))
        p.append(text(22,1538,'within each case; source links below',15,MUTED))
        p.append(text(22,1572,'Shared runtime · Process integrity unknown',14,MUTED))
    else:
        p.append(text(40,837,'Shown fields match all 3 C + 3 S repeats within each case',23,weight=700))
        p.append(text(40,874,'Selected source records are linked below; this is not a claim that whole files are identical',20,MUTED))
        p.append(text(40,913,'Shared runtime · C is not skill-free · Process integrity unknown',18,MUTED))
    return '\n'.join(p+['</svg>'])+'\n'

def render_all(root):
    data=load_data(root);outputs={}
    for name,fn in [('runs',ledger),('coverage',coverage),('evidence',evidence)]:
        for mobile in [False,True]:
            outputs[f'.github/assets/repeated-stress-{name}'+('-mobile' if mobile else '')+'.svg']=fn(data,mobile)
    provenance={'study_id':data['study_id'],'state':'final saved-evidence accounting','renderer':'evaluation/visualization/render_repeated_stress.py',
                'canonical_sources':data['canonical_sources'],'evidence_selection':data['excerpts'],
                'asset_sha256':{k:sha(v.encode()) for k,v in outputs.items()},
                'selection_rule':'First substantive failure by case/requirement order plus representative successful artifact from another case; with no failures, lowest dispatch-index successful R1 and R2 artifacts. This frozen study uses the no-failure fallback.',
                'display_transformations':['JSON fields are arranged as labeled values; field names shortened in the evidence panel. Summary USD cents are formatted as dollars by exact integer division, while record-detail cents stay integers. All other literal values are unchanged.',
                                           'Mechanical is the display name for objective requirements. Behavioral and AI semantic requirements remain separate.',
                                           'Run ratios use verified passes over scheduled requirements; not-assessed remains in the denominator.'],
                'limits':data['summary']['limits']}
    outputs[f'{STUDY}/results/visual-provenance.json']=json.dumps(provenance,indent=2,ensure_ascii=False)+'\n'
    return outputs

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--check',action='store_true');a=p.parse_args()
    outputs=render_all(a.root)
    for rel,content in outputs.items():
        target=a.root/rel
        if a.check:require(target.read_text()==content,'Stale rendered file: '+rel)
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content)
    print(json.dumps({'checked':a.check,'files':list(outputs),'source_binding':'exact SHA-256','data_state':'final'}))

if __name__=='__main__':main()
