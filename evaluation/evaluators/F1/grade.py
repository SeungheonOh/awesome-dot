#!/usr/bin/env python3
"""F1 exact-data grader plus an explicit pending blinded-prose review."""
import argparse,csv,hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent

def assertion(ok,detail): return {'passed':bool(ok),'detail':detail,'kind':'objective'}
def allpass(xs): return all(x['passed'] for x in xs)
def read_csv(path,headers):
 try:
  with path.open(newline='',encoding='utf-8-sig') as f:
   reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
  valid=(len(fields or [])==len(headers) and set(fields or [])==set(headers) and all(None not in r and all(v is not None for v in r.values()) for r in rows))
  return rows,valid,None
 except Exception as ex:return [],False,str(ex)
def integer(v):
 if not isinstance(v,str) or not re.fullmatch(r'[+-]?\d+',v):return None
 return int(v)
def refs(v):return set(x.strip() for x in (v or '').split(';') if x.strip())
def grade(packet,submission,semantic=None):
 key=json.loads((HERE/'oracle.json').read_text()); frozen=json.loads((HERE/'packet-hashes.json').read_text())
 integrity=[]
 for name,expected in frozen['files'].items():
  f=packet/name
  actual=hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else None
  integrity.append(assertion(actual==expected,'Protected source SHA-256: '+name))
 cr,cv,ce=read_csv(submission/'claim-lines.csv',key['claim_headers']);mr,mv,me=read_csv(submission/'source-map.csv',key['map_headers'])
 c={r.get('transaction_id'):r for r in cr};m={r.get('source_id'):r for r in mr};expected_c={r['transaction_id']:r for r in key['claim_rows']};expected_m={r['source_id']:r for r in key['map_rows']}
 try:note=(submission/'exceptions.txt').read_text(encoding='utf-8');ne=None
 except Exception as ex:note='';ne=str(ex)
 labels={};headerlines=note.splitlines()[:4]
 for line in headerlines:
  if ':' in line:
   name,value=line.split(':',1);labels[name.strip()]=integer(value.strip())
 groups={x:[] for x in ('g1','g2','g3','g4','g5')}
 a=lambda g,ok,msg:groups[g].append(assertion(ok,msg))
 a('g1',len(cr)==6 and set(c)==set(expected_c),'Exactly one claim row for each of six canonical transactions')
 a('g1',len(mr)==15 and set(m)==set(expected_m),'Exactly one mapping for every S01–S15 source')
 for sid,r in expected_m.items():a('g1',all(m.get(sid,{}).get(k)==r[k] for k in ('transaction_id','disposition')),sid+' maps to the canonical transaction with correct evidence disposition')
 for tid,r in expected_c.items():
  got=c.get(tid,{})
  for k in ('source_minor','business_minor','cap_adjustment_minor','claim_minor'):
   ok=got.get(k)=='' if r[k]=='' else integer(got.get(k))==int(r[k])
   a('g2',ok,tid+' exact signed '+k)
  if tid!='T06':
   a('g3',all(got.get(k)==r[k] for k in ('date','kind','currency','status')),tid+' correct date, currency, line kind and readiness')
   a('g3',all(integer(got.get(k))==int(r[k]) for k in ('business_minor','cap_adjustment_minor','claim_minor')),tid+' policy business amount, credit, split and cap allocation')
 a('g2',labels.get('ready_subtotal_minor')==7774,'Ready subtotal is exact signed 7774 pence')
 a('g2',labels.get('source_total_minor')==10667,'Canonical source signed total is 10667 pence')
 u=c.get('T06',{})
 a('g4',u.get('status')=='unresolved' and all(u.get(k)=='' for k in ('business_minor','cap_adjustment_minor','claim_minor')),'T06 unresolved amount is unknown rather than zero or included')
 a('g4',integer(u.get('source_minor'))==1488 and u.get('date')=='2026-09-17' and u.get('kind')=='expense' and u.get('currency')=='GBP','T06 keeps its 1488-pence source and identity')
 ready=[integer(r.get('claim_minor')) for r in cr if r.get('status')=='ready']
 a('g4',len(ready)==5 and None not in ready and sum(v for v in ready if v is not None)==7774,'Only five ready signed lines form the subtotal')
 a('g4',labels.get('unresolved_source_minor')==1488,'Unresolved source amount is 1488')
 a('g5',cv and mv,'Both CSV files have complete exactly named columns and valid rows'+(' ('+str(ce or me)+')' if ce or me else ''))
 a('g5',ne is None,'exceptions.txt exists and is readable'+(' ('+str(ne)+')' if ne else ''))
 a('g5',len(labels)==4 and labels==key['totals'],'Four leading numeric labels agree with canonical accounting')
 valid_policy={'inputs/policy.txt#P'+str(n) for n in range(1,7)}
 for tid,r in expected_c.items():
  got=c.get(tid,{})
  a('g5',refs(got.get('source_refs'))==refs(r['source_refs']),tid+' source references include all and only canonical evidence')
  pref=refs(got.get('policy_refs'))
  a('g5',bool(pref) and pref<=valid_policy,tid+' nonempty policy locators resolve; substantive adequacy is reviewed')
 for sid,r in expected_m.items():a('g5',m.get(sid,{}).get('locator')==r['locator'],sid+' source locator resolves')
 semantic_result=None;semantic_detail='Blinded explanation review is pending; keyword matching is not used'
 required_outputs=('claim-lines.csv','source-map.csv','exceptions.txt')
 submission_hashes={name:hashlib.sha256((submission/name).read_bytes()).hexdigest() for name in required_outputs if (submission/name).is_file()}
 if isinstance(semantic,dict):
  rg=semantic.get('groups',{})
  bound=semantic.get('case_id')=='F1' and semantic.get('submission_hashes')==submission_hashes and len(submission_hashes)==3
  review=rg.get('g5',{}) if bound and isinstance(rg,dict) else {}
  review=review if isinstance(review,dict) else {}
  if type(review.get('passed')) is bool and isinstance(review.get('evidence'),list) and review['evidence'] and all(isinstance(x,str) and x.strip() for x in review['evidence']):
   semantic_result=review['passed'];semantic_detail='Blinded explanation review: '+' | '.join(review['evidence'])
 groups['g5'].append({'passed':semantic_result,'detail':semantic_detail,'kind':'semantic'})
 output=[]
 for gid,xs in groups.items():
  passed=False if any(x['passed'] is False for x in xs) else None if any(x['passed'] is None for x in xs) else True
  output.append({'id':gid,'passed':passed,'assertions':xs})
 ip=allpass(integrity);states=[g['passed'] for g in output]
 accepted=False if not ip or False in states else None if None in states else True
 return {'case_id':'F1','integrity':{'passed':ip,'assertions':integrity},'groups':output,'accepted':accepted,'quality':{'passed_groups':sum(s is True for s in states),'scored_groups':sum(s is not None for s in states),'total_groups':5}}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',required=True,type=Path);ap.add_argument('--submission',required=True,type=Path);ap.add_argument('--semantic',type=Path);ap.add_argument('--out',type=Path);ns=ap.parse_args()
 sem=json.loads(ns.semantic.read_text()) if ns.semantic else None
 report=grade(ns.packet,ns.submission,sem);raw=json.dumps(report,indent=2)+'\n'
 if ns.out:ns.out.write_text(raw,encoding='utf-8')
 else:print(raw,end='')
if __name__=='__main__':main()
