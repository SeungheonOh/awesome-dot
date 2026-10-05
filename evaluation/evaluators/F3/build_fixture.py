#!/usr/bin/env python3
"""Original fictional fixture authoring only; not part of the runner packet."""
import csv, hashlib, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
P = ROOT.parents[1]/'cases/F3'
E = ROOT
START='2026-10-30T00:00:00Z'; END='2026-11-03T00:00:00Z'
def save_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
people=[]
for pid,name,zone,offset,hours in [('P1','Ari Vale','America/New_York','-04:00',('08:30','12:30')),('P2','Bea Moss','Europe/London','+00:00',('12:30','17:30')),('P3','Cleo Neri','Africa/Nairobi','+03:00',('15:30','20:30'))]:
    periods=([{'start_utc':START,'end_utc':'2026-11-01T06:00:00Z','offset':'-04:00'}, {'start_utc':'2026-11-01T06:00:00Z','end_utc':END,'offset':'-05:00'}] if pid=='P1' else [{'start_utc':START,'end_utc':END,'offset':offset}])
    windows=[]
    for day in ['2026-10-30','2026-10-31','2026-11-01','2026-11-02']:
        off='-05:00' if pid=='P1' and day >= '2026-11-01' else offset
        windows.append({'local_date':day,'start_local':f'{day}T{hours[0]}:00{off}','end_local':f'{day}T{hours[1]}:00{off}'})
    people.append({'id':pid,'name':name,'display_zone':zone,'offset_periods':periods,'working_windows':windows})
save_json(P/'inputs/participants.json', {'fictional':True,'participants':people})
busy=[
 ['B01','P1','2026-10-30T08:30:00-04:00','2026-10-30T09:00:00-04:00'],
 ['B02','P1','2026-10-30T09:00:00-04:00','2026-10-30T09:45:00-04:00'],
 ['B03','P2','2026-10-30T15:00:00+00:00','2026-10-30T15:15:00+00:00'],
 ['B04','P3','2026-10-31T15:30:00+03:00','2026-10-31T17:00:00+03:00'],
 ['B05','P2','2026-11-01T12:30:00+00:00','2026-11-01T14:30:00+00:00'],
 ['B06','P3','2026-11-01T18:45:00+03:00','2026-11-01T19:00:00+03:00'],
 ['B07','P1','2026-11-02T10:00:00-05:00','2026-11-02T10:30:00-05:00'],
]
with (P/'inputs/busy.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['busy_id','participant_id','start_local','end_local']);w.writerows(busy)
with (P/'inputs/coverage.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['coverage_id','participant_id','start_utc','end_utc']);w.writerows([
        ['C01','P1',START,END],['C02','P2',START,'2026-10-31T14:30:00Z'],
        ['C03','P2','2026-10-31T17:30:00Z',END],['C04','P3',START,END]])
# Hand-derived frozen independent interval key. Do not replace it with runner output.
key={
 'case_id':'F3','time_cap_seconds':900,
 'horizon':{'start_utc':START,'end_utc':END},
 'expected_starts':['2026-10-30T14:00:00Z','2026-10-30T15:30:00Z','2026-11-01T14:45:00Z','2026-11-01T16:15:00Z','2026-11-01T16:30:00Z'],
 'all_verified_starts':['2026-10-30T14:00:00Z','2026-10-30T15:30:00Z','2026-11-01T14:45:00Z','2026-11-01T16:15:00Z','2026-11-01T16:30:00Z','2026-11-02T13:45:00Z','2026-11-02T14:00:00Z','2026-11-02T15:45:00Z','2026-11-02T16:00:00Z','2026-11-02T16:15:00Z','2026-11-02T16:30:00Z'],
 'coverage_gaps':[{'participant_id':'P2','start_utc':'2026-10-31T14:30:00Z','end_utc':'2026-10-31T17:30:00Z'}],
 'proof_by_date':{
   '2026-10-30':{'guarded_work_intersection':['12:30Z','16:30Z'],'raw_busy_union_in_intersection':[['12:30Z','13:45Z'],['15:00Z','15:15Z']],'start_ranges_closed':[['14:00Z','14:00Z'],['15:30Z','15:30Z']]},
   '2026-10-31':{'guarded_work_intersection':['12:30Z','16:30Z'],'raw_busy_union_in_intersection':[['12:30Z','14:00Z']],'earliest_busy_clear_start':'14:15Z','latest_start_with_full_P2_coverage':'13:30Z','start_ranges_closed':[],'conclusion':'No verified options; later time remains unknown, not proven unavailable'},
   '2026-11-01':{'guarded_work_intersection':['13:30Z','17:30Z'],'raw_busy_union_in_intersection':[['13:30Z','14:30Z'],['15:45Z','16:00Z']],'start_ranges_closed':[['14:45Z','14:45Z'],['16:15Z','16:30Z']]},
   '2026-11-02':{'guarded_work_intersection':['13:30Z','17:30Z'],'raw_busy_union_in_intersection':[['15:00Z','15:30Z']],'start_ranges_closed':[['13:45Z','14:00Z'],['15:45Z','16:30Z']]}
 }
}
save_json(E/'oracle.json', key)
