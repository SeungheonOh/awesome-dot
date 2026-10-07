#!/usr/bin/env python3
"""Read-only integrity and result reconstruction for this completed cohort."""
import collections,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=load(ROOT/'MANIFEST.json');files=manifest['files']
 actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
 assert actual==set(files),{'missing':sorted(set(files)-actual),'extra':sorted(actual-set(files))}
 for name,info in files.items():
  p=ROOT/name
  assert not p.is_symlink() and p.stat().st_size==info['bytes'] and sha(p)==info['sha256'],name
 gold={c['calibration_id']:c for c in load(ROOT/'gold.json')['cases']};schedule=load(ROOT/'schedule.json')['reviews'];analysis=load(ROOT/'results/analysis.json')
 assert len(schedule)==28 and len({x['reviewer_id'] for x in schedule})==28
 votes=[];reviews={}
 for s in schedule:
  raw=ROOT/s['review_file'];review=load(raw);g=gold[s['calibration_id']]
  assert sha(raw)==s['review_sha256'] and review['reviewer_id']==s['reviewer_id'] and review['case_id']==s['case_id']
  hashes={p.name:sha(p) for p in sorted((ROOT/s['output_dir']).iterdir())}
  assert hashes==review['artifact_sha256']==g['artifact_sha256']
  assert review['condition_masked'] is True and review['independent'] is True
  assert review['runtime_disclosure']['exposure_incident'] is None
  assert set(review['checks'])==set(g['checks'])
  reviews[(s['calibration_id'],s['replica'])]=review
  for k,v in review['checks'].items():
   assert v['status'] in ('pass','fail','unknown') and v['rationale'].strip()
   votes.append({'calibration_id':s['calibration_id'],'replica':s['replica'],'reviewer_id':s['reviewer_id'],'criterion':k,'gold':g['checks'][k]['status'],'status':v['status'],'rationale':v['rationale']})
 assert len(votes)==84
 index={(v['reviewer_id'],v['criterion']):v for v in analysis['individual_votes']}
 for v in votes:
  assert all(index[(v['reviewer_id'],v['criterion'])][k]==value for k,value in v.items())
 combined=[]
 for cid,g in gold.items():
  for k,label in g['checks'].items():
   ss=[reviews[(cid,i)]['checks'][k]['status'] for i in (1,2)]
   status=ss[0] if ss[0]==ss[1] and ss[0] in ('pass','fail') else 'unknown'
   combined.append({'calibration_id':cid,'criterion':k,'gold':label['status'],'status':status})
 index={(v['calibration_id'],v['criterion']):v for v in analysis['combined_outcomes']}
 for v in combined:assert all(index[(v['calibration_id'],v['criterion'])][k]==value for k,value in v.items())
 def check_summary(rows,summary):
  assert summary['positions']==len(rows)
  assert summary['exact_matches']==sum(r['status']==r['gold'] for r in rows)
  for g,preds in summary['confusion'].items():
   for p,n in preds.items():assert n==sum(r['gold']==g and r['status']==p for r in rows)
  for g,key in [('fail','failure_detection_sensitivity'),('pass','passed_check_preservation_specificity')]:
   assert summary[key]=={'numerator':sum(r['gold']==g and r['status']==g for r in rows),'denominator':sum(r['gold']==g for r in rows)}
 check_summary(votes,analysis['individual_summary']);check_summary(combined,analysis['combined_summary'])
 for k,summary in analysis['individual_by_criterion'].items():check_summary([x for x in votes if x['criterion']==k],summary)
 for k,summary in analysis['combined_by_criterion'].items():check_summary([x for x in combined if x['criterion']==k],summary)
 for i,summary in analysis['individual_by_replica'].items():check_summary([x for x in votes if x['replica']==int(i)],summary)
 with tempfile.TemporaryDirectory(prefix='semantic-calibration-public-verify-') as temp:
  for cid,g in gold.items():
   rd=Path(temp)/cid;rd.mkdir()
   for i in (1,2):(rd/('review_'+str(i)+'.json')).write_text(json.dumps(reviews[(cid,i)]))
   command=[sys.executable,str(ROOT/'sources'/g['case_id']/'evaluator/grade.py'),'--submission-dir',str(ROOT/'outputs'/cid),'--semantic-review-dir',str(rd)]
   result=json.loads(subprocess.run(command,capture_output=True,text=True,check=True,timeout=10).stdout)
   assert result==load(ROOT/'results/frozen_grader'/(cid+'.json'))
   for k in g['checks']:assert result['checks'][k]['status']==index[(cid,k)]['status']
 print(json.dumps({'verified':True,'files':len(files),'raw_reviews':28,'individual_votes':84,'combined_outcomes':42,'individual_gold_matches':sum(x['gold']==x['status'] for x in votes),'combined_gold_matches':sum(x['gold']==x['status'] for x in combined),'frozen_grader_crosschecks':14,'model_calls':0},indent=2))
if __name__=='__main__':main()
