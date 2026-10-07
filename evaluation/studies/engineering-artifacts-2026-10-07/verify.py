"""Read-only verification of the staged engineering evidence package."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_text())
def main():
 m=load(ROOT/'manifest.json')
 files={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='manifest.json'}
 assert files==set(m['sha256']),'package inventory differs'
 for rel,h in m['sha256'].items():
  p=ROOT/rel;assert not p.is_symlink() and sha(p.read_bytes())==h,rel
 d=load(ROOT/'results/all-results.json');assert d['planned_slots']==len(d['rows'])==8
 assert d['captured_first_finals']==6 and d['infrastructure_missing']==2
 assert len({r['slot_id'] for r in d['rows']})==8
 count=0
 for r in d['rows']:
  stdout=(ROOT/r['stdout_path']).read_bytes();stderr=(ROOT/r['stderr_path']).read_bytes()
  assert sha(stdout)==r['stdout_sha256'] and sha(stderr)==r['stderr_sha256']
  assert json.loads(stdout)==r['raw_grader_output']
  if r['artifact_path']:
   raw=(ROOT/r['artifact_path']).read_bytes();assert sha(raw)==r['artifact_sha256'] and len(raw)==r['artifact_bytes'];count+=1
  else:assert r['operational_status']=='infrastructure_error' and r['raw_grader_output']['discovery'] is False
 assert count==6
 proj=load(ROOT/'prompts/projection-manifest.json')
 for e in proj['entries']:
  raw=(ROOT/e['public_projection_path']).read_bytes();assert sha(raw)==e['public_projection_sha256'] and len(raw)==e['public_projection_bytes']
  assert raw.startswith(b'BEGIN SUPPLIED FILE: PROMPT.md\n')
  assert e['original_bytes']-e['public_projection_bytes']==e['removed_prefix_bytes']
 for case in ['exporter','triage']:
  guide='write-behavior-tests.md' if case=='exporter' else 'bug-reproduction-triage.md'
  for repeat in [1,2]:
   b=(ROOT/f'prompts/{case}-r{repeat}-baseline.public-projection.txt').read_bytes()
   g=(ROOT/f'prompts/{case}-r{repeat}-guide.public-projection.txt').read_bytes()
   assert g==b+b'BEGIN DESIGNATED GUIDE\n'+(ROOT/'fixture/sources'/guide).read_bytes()+b'END DESIGNATED GUIDE\n'
 print(json.dumps({'verified':True,'package_files':len(files),'planned_slots':8,'captured_artifacts':6,'infrastructure_unknown':2,'candidate_grading_rerun':False},sort_keys=True))
if __name__=='__main__':
 try:main()
 except (AssertionError,OSError,ValueError,KeyError) as e:print(str(e),file=sys.stderr);sys.exit(1)
