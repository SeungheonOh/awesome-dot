#!/usr/bin/env python3
"""F2 source-backed exact checks plus explicit blinded semantic criteria."""
import argparse,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
FIELDS={'action_id','deliverable','owner','deadline','status','reported_complete','verified_complete','source_refs','clarifications'}
CATEGORIES={'commitment','owner','deadline','completion'}
def check(ok,detail):return {'passed':bool(ok),'detail':detail,'kind':'objective'}
def reject_duplicates(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('Duplicate JSON member: '+k)
  d[k]=v
 return d

def grade(packet,submission,semantic=None):
 key=json.loads((HERE/'oracle.json').read_text());snapshot=json.loads((HERE/'packet-hashes.json').read_text());checks=[]
 for name,want in snapshot['files'].items():
  f=packet/name;got=hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else None
  checks.append(check(got==want,'Protected SHA-256: '+name))
 groups={g:[] for g in ('g1','g2','g3','g4','g5')}
 def add(g,ok,detail):groups[g].append(check(ok,detail))
 data={};err=None
 try:
  data=json.loads((submission/'actions.json').read_text(encoding='utf-8'),object_pairs_hook=reject_duplicates)
  if not isinstance(data,dict):raise ValueError('Top level must be object')
 except Exception as ex:err=str(ex);data={}
 try:handoff=(submission/'handoff.txt').read_text(encoding='utf-8');herr=None
 except Exception as ex:handoff='';herr=str(ex)
 raw=data.get('actions',[]);raw=raw if isinstance(raw,list) else []
 valid_actions=[a for a in raw if isinstance(a,dict) and isinstance(a.get('action_id'),str)]
 actions={a['action_id']:a for a in valid_actions};ids=[a['action_id'] for a in valid_actions]
 exp={a['action_id']:a for a in key['actions']};valid_refs=set(key['valid_locators'])
 add('g1',len(raw)==6 and len(valid_actions)==6 and set(ids)==set(exp),'Exactly the six agreed EX-11 through EX-16 actions are represented')
 add('g1',all(isinstance(a.get('deliverable'),str) and a['deliverable'].strip() for a in valid_actions) and len(valid_actions)==6,'Every agreed action has a nonempty deliverable description; meaning is reviewed')
 add('g2',len(ids)==len(set(ids))==6,'Each canonical deliverable occurs once; no repeated commitment creates an extra action')
 add('g3',data.get('as_of')==key['as_of'],'Snapshot as-of matches the closed evidence cutoff')
 for aid,want in exp.items():
  got=actions.get(aid,{})
  add('g3',got.get('owner')==want['owner'],aid+' current owner or explicit null matches accepted authority')
  add('g3',got.get('deadline')==want['deadline'],aid+' exact local date/time, unknown time, zone and authoritative offset')
  add('g4',got.get('status')==want['status'],aid+' status matches completion evidence')
  for name in ('reported_complete','verified_complete'):
   add('g4',type(got.get(name)) is bool and got[name] is want[name],aid+' '+name+' distinguishes a claim from verified completion')
 add('g5',err is None and set(data)=={'as_of','actions'} and isinstance(data.get('actions'),list),'Readable non-duplicate JSON with exact top-level schema'+(' ('+str(err)+')' if err else ''))
 add('g5',herr is None and bool(handoff.strip()) and len(handoff.split())<=450,'handoff.txt is readable, nonempty, at most 450 whitespace-delimited words'+(' ('+str(herr)+')' if herr else ''))
 for aid,got in actions.items():
  add('g5',set(got)==FIELDS,aid+' exact action schema')
  sr=got.get('source_refs');sr=sr if isinstance(sr,dict) else {}
  add('g5',set(sr)==CATEGORIES,aid+' all four source-reference categories exist')
  for category in CATEGORIES:
   refs=sr.get(category)
   add('g5',isinstance(refs,list) and all(isinstance(r,str) and r in valid_refs for r in refs),aid+' '+category+' references resolve')
  qs=got.get('clarifications')
  qvalid=isinstance(qs,list) and all(isinstance(q,dict) and set(q)=={'question','source_refs'} and isinstance(q['question'],str) and bool(q['question'].strip()) and isinstance(q['source_refs'],list) and bool(q['source_refs']) and all(isinstance(r,str) and r in valid_refs for r in q['source_refs']) for q in qs)
  add('g5',qvalid,aid+' clarification schema and references')
  if aid in ('EX-14','EX-15'):add('g5',isinstance(qs,list) and len(qs)>=1,aid+' has a specific-question slot; specificity is manually reviewed')
 required_outputs=('actions.json','handoff.txt')
 submission_hashes={name:hashlib.sha256((submission/name).read_bytes()).hexdigest() for name in required_outputs if (submission/name).is_file()}
 review=semantic.get('groups',{}) if isinstance(semantic,dict) and semantic.get('case_id')=='F2' and semantic.get('submission_hashes')==submission_hashes and len(submission_hashes)==2 else {}
 for gid in groups:
  r=review.get(gid,{}) if isinstance(review,dict) else {};r=r if isinstance(r,dict) else {}
  valid=type(r.get('passed')) is bool and isinstance(r.get('evidence'),list) and bool(r['evidence']) and all(isinstance(s,str) and s.strip() for s in r['evidence'])
  groups[gid].append({'kind':'semantic','passed':r['passed'] if valid else None,'detail':'Blinded source-grounded semantic review: '+' | '.join(r['evidence']) if valid else 'Blinded semantic review pending; no keyword matching supplies a score'})
 result=[]
 for gid,items in groups.items():
  status=False if any(c['passed'] is False for c in items) else None if any(c['passed'] is None for c in items) else True
  result.append({'id':gid,'passed':status,'assertions':items})
 states=[g['passed'] for g in result];ip=all(c['passed'] for c in checks)
 return {'case_id':'F2','integrity':{'passed':ip,'assertions':checks},'groups':result,'accepted':False if not ip or False in states else None if None in states else True,'quality':{'passed_groups':sum(x is True for x in states),'scored_groups':sum(x is not None for x in states),'total_groups':5}}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',required=True,type=Path);ap.add_argument('--submission',required=True,type=Path);ap.add_argument('--semantic',type=Path);ap.add_argument('--out',type=Path);n=ap.parse_args()
 r=grade(n.packet,n.submission,json.loads(n.semantic.read_text()) if n.semantic else None);s=json.dumps(r,indent=2)+'\n'
 if n.out:n.out.write_text(s,encoding='utf-8')
 else:print(s,end='')
if __name__=='__main__':main()
