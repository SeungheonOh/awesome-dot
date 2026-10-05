#!/usr/bin/env python3
"""Construct frozen author-owned controls from explicit, manually calculated endpoints."""
import copy, json, pathlib
import grade
HERE=pathlib.Path(__file__).resolve().parent
P=HERE.parents[1]/'cases/F3'
def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def option(rank,start,end,ny,london,nairobi):
    return {'rank':rank,'start_utc':start,'end_utc':end,'local_times':{p:{'start':a,'end':b} for p,(a,b) in zip(['P1','P2','P3'],[ny,london,nairobi])}}
options=[
 option(1,'2026-10-30T14:00:00Z','2026-10-30T14:45:00Z',('2026-10-30T10:00:00-04:00','2026-10-30T10:45:00-04:00'),('2026-10-30T14:00:00+00:00','2026-10-30T14:45:00+00:00'),('2026-10-30T17:00:00+03:00','2026-10-30T17:45:00+03:00')),
 option(2,'2026-10-30T15:30:00Z','2026-10-30T16:15:00Z',('2026-10-30T11:30:00-04:00','2026-10-30T12:15:00-04:00'),('2026-10-30T15:30:00+00:00','2026-10-30T16:15:00+00:00'),('2026-10-30T18:30:00+03:00','2026-10-30T19:15:00+03:00')),
 option(3,'2026-11-01T14:45:00Z','2026-11-01T15:30:00Z',('2026-11-01T09:45:00-05:00','2026-11-01T10:30:00-05:00'),('2026-11-01T14:45:00+00:00','2026-11-01T15:30:00+00:00'),('2026-11-01T17:45:00+03:00','2026-11-01T18:30:00+03:00')),
 option(4,'2026-11-01T16:15:00Z','2026-11-01T17:00:00Z',('2026-11-01T11:15:00-05:00','2026-11-01T12:00:00-05:00'),('2026-11-01T16:15:00+00:00','2026-11-01T17:00:00+00:00'),('2026-11-01T19:15:00+03:00','2026-11-01T20:00:00+03:00')),
 option(5,'2026-11-01T16:30:00Z','2026-11-01T17:15:00Z',('2026-11-01T11:30:00-05:00','2026-11-01T12:15:00-05:00'),('2026-11-01T16:30:00+00:00','2026-11-01T17:15:00+00:00'),('2026-11-01T19:30:00+03:00','2026-11-01T20:15:00+03:00')),
]
ref={'case_id':'F3','status':'options_only','meeting_duration_minutes':45,'pre_buffer_minutes':15,'post_buffer_minutes':15,'grid_minutes':15,'all_participants_required':True,'buffers_within_working_hours':True,'coverage_policy':'verified_only','uncovered_time_means':'unknown','constraints_relaxed':False,'coverage_gaps':[{'participant_id':'P2','start_utc':'2026-10-31T14:30:00Z','end_utc':'2026-10-31T17:30:00Z'}],'options':options}
def deliver(folder,d):
    save(folder/'options.json',d)
    (folder/'explanation.txt').write_text(grade.receipt(d),encoding='utf-8')
deliver(HERE/'reference',ref)
key=grade.read_json(HERE/'oracle.json');key['expected_options']=options;save(HERE/'oracle.json',key)
controls={}
d=copy.deepcopy(ref);d['options'][2]['local_times']['P1']={'start':'2026-11-01T10:45:00-04:00','end':'2026-11-01T11:30:00-04:00'}
controls['g1_stale_offset']=d
d=copy.deepcopy(ref);d['options'][0]['end_utc']='2026-10-30T14:30:00Z'
d['options'][0]['local_times']['P1']['end']='2026-10-30T10:30:00-04:00';d['options'][0]['local_times']['P2']['end']='2026-10-30T14:30:00+00:00';d['options'][0]['local_times']['P3']['end']='2026-10-30T17:30:00+03:00'
controls['g2_short_meeting']=d
d=copy.deepcopy(ref);d['options'][4]=option(5,'2026-11-02T13:45:00Z','2026-11-02T14:30:00Z',('2026-11-02T08:45:00-05:00','2026-11-02T09:30:00-05:00'),('2026-11-02T13:45:00+00:00','2026-11-02T14:30:00+00:00'),('2026-11-02T16:45:00+03:00','2026-11-02T17:30:00+03:00'))
controls['g3_later_valid_option']=d
d=copy.deepcopy(ref);d['coverage_gaps']=[];controls['g4_omitted_unknown_gap']=d
d=copy.deepcopy(ref);d['status']='booked';controls['g5_claimed_booking']=d
for name,d in controls.items():
    deliver(HERE/'controls'/name,d)
save(HERE/'controls/expected-results.json',{'reference':{'integrity':True,'groups':{f'g{i}':True for i in range(1,6)},'accepted':True},**{name:{'integrity':True,'groups':{f'g{i}':not name.startswith(f'g{i}_') for i in range(1,6)},'accepted':False} for name in controls}})
save(HERE/'case-metadata.json',{'case_id':'F3','fixture_version':1,'time_cap_seconds':900,'time_cap_start':'runner process launch','time_cap_includes':['task execution','skill reading','self-checks'],'time_cap_excludes':['setup','grading'],'runtime':'Python 3.10+ standard library','network':False,'model_execution':False,'external_mutation':False,'semantic_review_required':False,'protected_packet':'../../cases/F3','required_artifacts':['options.json','explanation.txt'],'groups':['g1','g2','g3','g4','g5'],'integrity_gate':'SHA-256 of all supplied packet files including task and manifest'})
