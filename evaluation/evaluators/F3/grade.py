#!/usr/bin/env python3
"""F3 deterministic evaluator. Reads artifacts only; executes no submitted code."""
import argparse
import csv
import datetime as dt
import hashlib
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
UTC_RE = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
LOCAL_RE = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$')
TOP_KEYS = {'case_id','status','meeting_duration_minutes','pre_buffer_minutes','post_buffer_minutes','grid_minutes','all_participants_required','buffers_within_working_hours','coverage_policy','uncovered_time_means','constraints_relaxed','coverage_gaps','options'}
OPTION_KEYS = {'rank','start_utc','end_utc','local_times'}
PID = {'P1','P2','P3'}


def unique_object(pairs):
    result = {}
    for k,v in pairs:
        if k in result:
            raise ValueError('Duplicate JSON key: '+k)
        result[k]=v
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Non-finite JSON number: '+x)))


def stamp(s):
    if not isinstance(s,str):
        raise ValueError('Timestamp is not a string')
    d=dt.datetime.fromisoformat(s.replace('Z','+00:00'))
    if d.tzinfo is None:
        raise ValueError('Timestamp has no offset')
    return int(d.timestamp())


def utc(t):
    return dt.datetime.fromtimestamp(t,dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def utc_stamp(s):
    if not isinstance(s,str) or not UTC_RE.fullmatch(s):
        raise ValueError('Noncanonical UTC timestamp')
    t=stamp(s)
    if utc(t)!=s:
        raise ValueError('Noncanonical UTC value')
    return t


def merge(intervals):
    out=[]
    for a,b in sorted(intervals):
        if out and a<=out[-1][1]:
            out[-1]=(out[-1][0],max(b,out[-1][1]))
        else:
            out.append((a,b))
    return out


def subtract(window, covered):
    a,b=window; cursor=a; out=[]
    for x,y in merge(covered):
        if y<=cursor or x>=b:
            continue
        if cursor<x:
            out.append((cursor,min(x,b)))
        cursor=max(cursor,min(y,b))
        if cursor>=b:
            break
    if cursor<b:
        out.append((cursor,b))
    return out


def load_inputs(packet):
    people={p['id']:p for p in read_json(packet/'inputs/participants.json')['participants']}
    windows={p:[(stamp(w['start_local']),stamp(w['end_local'])) for w in v['working_windows']] for p,v in people.items()}
    busy={p:[] for p in PID}; coverage={p:[] for p in PID}
    with (packet/'inputs/busy.csv').open(newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            busy[r['participant_id']].append((stamp(r['start_local']),stamp(r['end_local'])))
    with (packet/'inputs/coverage.csv').open(newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            coverage[r['participant_id']].append((stamp(r['start_utc']),stamp(r['end_utc'])))
    return people,windows,busy,coverage


def local_at(t, person):
    for p in person['offset_periods']:
        if stamp(p['start_utc'])<=t<stamp(p['end_utc']):
            off=p['offset']; sign=1 if off[0]=='+' else -1
            seconds=sign*(int(off[1:3])*3600+int(off[4:6])*60)
            return dt.datetime.fromtimestamp(t+seconds,dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')+off
    raise ValueError('No supplied authoritative offset for this endpoint')


def contained(a,b,intervals):
    return any(x<=a and b<=y for x,y in merge(intervals))


def overlaps(a,b,intervals):
    return any(a<y and x<b for x,y in intervals)


def arithmetic_starts(packet):
    """Independent exhaustive 15-minute integer-instant calculation for fixture QA."""
    _,windows,busy,coverage=load_inputs(pathlib.Path(packet))
    starts=[]
    for s in range(stamp('2026-10-30T00:00:00Z'),stamp('2026-11-03T00:00:00Z'),900):
        a,b=s-900,s+3600
        if all(contained(a,b,windows[p]) and contained(a,b,coverage[p]) and not overlaps(a,b,busy[p]) for p in PID):
            starts.append(utc(s))
    return starts


def calculated_gaps(windows,coverage):
    result=[]
    for p in sorted(PID):
        pieces=[]
        for w in windows[p]:
            pieces.extend(subtract(w,coverage[p]))
        for a,b in merge(pieces):
            result.append({'participant_id':p,'start_utc':utc(a),'end_utc':utc(b)})
    return result


def receipt(d):
    def boolean(v):
        return 'true' if v is True else 'false' if v is False else str(v)
    lines=[
      'Status: options only; no calendar changes made',
      'Returned options: '+str(len(d['options'])),
      f"Meeting: {d['meeting_duration_minutes']} minutes; pre-buffer: {d['pre_buffer_minutes']} minutes; post-buffer: {d['post_buffer_minutes']} minutes",
      f"Requirements: all attendees={boolean(d['all_participants_required'])}; buffers inside working hours={boolean(d['buffers_within_working_hours'])}; grid={d['grid_minutes']} minutes UTC",
      f"Coverage: {d['coverage_policy']}; uncovered time={d['uncovered_time_means']}; constraints relaxed={boolean(d['constraints_relaxed'])}",
    ]
    if d['coverage_gaps']:
        lines += [f"Coverage gap: {g['participant_id']} | {g['start_utc']} | {g['end_utc']}" for g in d['coverage_gaps']]
    else:
        lines += ['Coverage gaps: none']
    lines += ['Offset change: P1 | 2026-11-01T06:00:00Z | -04:00 to -05:00','Touching endpoints are allowed; buffers are applied once.']
    lines += [f"Option {o['rank']}: {o['start_utc']} to {o['end_utc']}" for o in d['options']]
    return '\n'.join(lines)+'\n'


def assertion(name,passed,reason='',**values):
    return dict(id=name,passed=bool(passed),reason=reason,**values)


def grade(packet,submission):
    packet=pathlib.Path(packet); submission=pathlib.Path(submission)
    key=read_json(HERE/'oracle.json'); protected=read_json(HERE/'protected-hashes.json')
    ia=[]
    for rel,want in protected.items():
        try:
            got=hashlib.sha256((packet/rel).read_bytes()).hexdigest()
            ia.append(assertion('protected:'+rel,got==want,'Protected packet bytes must match the frozen originals',expected=want,actual=got))
        except (OSError,ValueError) as e:
            ia.append(assertion('protected:'+rel,False,str(e)))
    integrity={'passed':all(a['passed'] for a in ia),'assertions':ia}
    groups={f'g{i}':[] for i in range(1,6)}
    def add(g,name,passed,reason='',**values):
        groups[g].append(assertion(name,passed,reason,**values))
    try:
        d=read_json(submission/'options.json')
        prose=(submission/'explanation.txt').read_text(encoding='utf-8')
        if not isinstance(d,dict) or not isinstance(d.get('options'),list):
            raise ValueError('JSON must be an object containing an options array')
        people,windows,busy,coverage=load_inputs(packet)
    except (OSError,ValueError,KeyError,TypeError) as e:
        for g in groups:
            add(g,'readable-required-artifacts',False,str(e))
        return finish(integrity,groups)

    opts=d['options']; parsed=[]
    add('g1','nonempty-evaluable-options',len(opts)>0,'This fixture has verified options, so an empty result cannot establish correct displays')
    add('g2','nonempty-evaluable-options',len(opts)>0,'This fixture has verified options, so an empty result cannot establish a valid offered meeting')
    for i,o in enumerate(opts,1):
        try:
            s=utc_stamp(o['start_utc']); e=utc_stamp(o['end_utc'])
            parsed.append((o,s,e))
            displays=o['local_times']
            valid=isinstance(displays,dict) and set(displays)==PID
            expected={p:{'start':local_at(s,people[p]),'end':local_at(e,people[p])} for p in sorted(PID)}
            valid=valid and displays==expected
            add('g1',f'option-{i}-endpoint-displays',valid,'Both local endpoints must use supplied authoritative dates and numeric offsets',expected=expected,actual=displays)
        except (ValueError,KeyError,TypeError,OverflowError,AttributeError) as exc:
            add('g1',f'option-{i}-timestamps',False,str(exc))
            add('g2',f'option-{i}-evaluable',False,str(exc))
            add('g4',f'option-{i}-evaluable-coverage',False,str(exc))
    for name,want in [('meeting_duration_minutes',45),('pre_buffer_minutes',15),('post_buffer_minutes',15),('grid_minutes',15)]:
        add('g2','declared-'+name,type(d.get(name)) is int and d.get(name)==want,'Declared constraint must match the task',expected=want,actual=d.get(name))
    for name in ['all_participants_required','buffers_within_working_hours']:
        add('g2','declared-'+name,d.get(name) is True,'Hard constraint cannot be relaxed')
    h0=stamp(key['horizon']['start_utc']); h1=stamp(key['horizon']['end_utc'])
    for i,(o,s,e) in enumerate(parsed,1):
        a,b=s-900,e+900
        add('g2',f'option-{i}-duration',e-s==2700,'Meeting duration is exactly 45 elapsed minutes',actual_seconds=e-s)
        add('g2',f'option-{i}-utc-grid',s%900==0,'Starts lie on the 15-minute UTC grid')
        add('g2',f'option-{i}-horizon',h0<=a<b<=h1,'The whole once-buffered meeting lies inside the bounded horizon')
        for p in sorted(PID):
            add('g2',f'option-{i}-{p}-working',any(x<=a and b<=y for x,y in windows[p]),'The guarded interval fits one listed working window')
            add('g2',f'option-{i}-{p}-busy',not overlaps(a,b,busy[p]),'The guarded interval does not overlap any raw busy interval; touching is allowed')
            add('g4',f'option-{i}-{p}-coverage',contained(a,b,coverage[p]),'The whole guarded interval must have known coverage')
    starts=[o.get('start_utc') if isinstance(o,dict) else None for o in opts]
    add('g3','exact-earliest-start-sequence',starts==key['expected_starts'],'Return precisely the earliest five verified distinct starts',expected=key['expected_starts'],actual=starts)
    ranks=[o.get('rank') if isinstance(o,dict) else None for o in opts]
    add('g3','ranks',ranks==list(range(1,len(opts)+1)) and all(type(r) is int for r in ranks),'Ranks are consecutive JSON integers in saved order',actual=ranks)
    for name,want in [('coverage_policy','verified_only'),('uncovered_time_means','unknown'),('constraints_relaxed',False)]:
        value=d.get(name)
        add('g4','declared-'+name,type(value) is type(want) and value==want,'Unknown time stays unknown; no hard constraint is relaxed',expected=want,actual=value)
    gaps=d.get('coverage_gaps')
    add('g4','complete-maximal-coverage-gaps',gaps==key['coverage_gaps'],'List all and only maximal uncovered portions of listed work windows, including unused days',expected=key['coverage_gaps'],actual=gaps)
    add('g5','exact-top-level-schema',set(d)==TOP_KEYS,'Use exactly the declared top-level keys')
    add('g5','case-and-options-only-status',d.get('case_id')=='F3' and d.get('status')=='options_only','Outputs are options only, with no claim of booking')
    try:
        schema=all(isinstance(o,dict) and set(o)==OPTION_KEYS and isinstance(o['local_times'],dict) and set(o['local_times'])==PID and all(isinstance(v,dict) and set(v)=={'start','end'} for v in o['local_times'].values()) for o in opts)
        schema=schema and isinstance(gaps,list) and all(isinstance(g,dict) and set(g)=={'participant_id','start_utc','end_utc'} for g in gaps)
        add('g5','exact-nested-schema',schema,'Option, local endpoint, and coverage-gap objects use only their requested keys')
        expected_receipt=receipt(d)
        # Only the final newline is optional; no synonym or free-form prose heuristics.
        add('g5','receipt-agrees-with-saved-json',prose==expected_receipt or prose==expected_receipt[:-1],'Receipt lines must use the explicitly requested format and agree with saved values')
    except (KeyError,TypeError,ValueError,AttributeError) as e:
        add('g5','renderable-receipt',False,str(e))
    return finish(integrity,groups)


def finish(integrity,groups):
    rows=[{'id':g,'passed':all(a['passed'] for a in assertions),'assertions':assertions} for g,assertions in groups.items()]
    n=sum(r['passed'] for r in rows)
    return {'case_id':'F3','integrity':integrity,'groups':rows,'accepted':integrity['passed'] and n==5,'quality':{'passed_groups':n,'scored_groups':5,'total_groups':5}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',required=True,type=pathlib.Path)
    parser.add_argument('--submission',required=True,type=pathlib.Path)
    parser.add_argument('--semantic',type=pathlib.Path,help='Reserved common interface; F3 has no semantic-scored requirements')
    parser.add_argument('--out',required=True,type=pathlib.Path)
    a=parser.parse_args()
    report=grade(a.packet,a.submission)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'case_id':report['case_id'],'accepted':report['accepted'],'quality':report['quality']}))

if __name__=='__main__':
    main()
