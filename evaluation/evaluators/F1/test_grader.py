import unittest,tempfile,shutil,json
from pathlib import Path
from grade import grade,HERE
P=HERE.parents[1]/'cases/F1'
class GraderTests(unittest.TestCase):
 def setUp(self):self.review=json.loads((HERE/'reference-review.json').read_text())
 def test_reference_passes(self):self.assertTrue(grade(P,HERE/'reference',self.review)['accepted'])
 def test_alternate_order_passes(self):self.assertTrue(grade(P,HERE/'controls/accepted-reordered',json.loads((HERE/'controls/accepted-reordered-review.json').read_text()))['accepted'])
 def test_concise_relevant_policy_refs_accepted(self):
  review=json.loads((HERE/'controls/accepted-concise-policy-refs-review.json').read_text())
  self.assertTrue(grade(P,HERE/'controls/accepted-concise-policy-refs',review)['accepted'])
 def test_missing_semantic_is_pending(self):
  r=grade(P,HERE/'reference');self.assertIsNone(r['accepted']);self.assertIsNone(r['groups'][4]['passed'])
 def test_each_group_control_fails(self):
  for i,name in enumerate(['duplicate-count','source-amount','cap-before-credit','unknown-as-zero','dangling-locator'],1):
   r=grade(P,HERE/('controls/bad-g%d-%s'%(i,name)),self.review)
   self.assertFalse(r['groups'][i-1]['passed'],name);self.assertFalse(r['accepted'])
 def test_semantic_contradiction(self):
  r=grade(P,HERE/'controls/bad-g5-prose-contradiction',json.loads((HERE/'reject-prose-review.json').read_text()))
  self.assertFalse(r['groups'][4]['passed'])
 def test_mutated_source_fails_integrity(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'packet';shutil.copytree(P,p);f=p/'inputs/evidence.csv';f.write_bytes(f.read_bytes()+b'\n')
   self.assertFalse(grade(p,HERE/'reference',self.review)['integrity']['passed'])
 def test_missing_files_fail_without_crash(self):
  with tempfile.TemporaryDirectory() as t:self.assertFalse(grade(P,Path(t),self.review)['accepted'])
 def test_review_hash_mismatch_stays_pending(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);shutil.copytree(HERE/'reference',p,dirs_exist_ok=True);f=p/'exceptions.txt';f.write_text(f.read_text()+'\n')
   self.assertIsNone(grade(P,p,self.review)['groups'][4]['passed'])
 def test_independent_integer_fixture_arithmetic(self):
  import csv
  with (P/'inputs/evidence.csv').open(newline='') as f: sources=list(csv.DictReader(f))
  primary={r['transaction_id']:int(r['amount_minor']) for r in sources if r['evidence_type'] in ('receipt','credit')}
  self.assertEqual(sum(primary.values()),10667)
  net_meals=sum(primary[t] for t in ('T01','T02','T03'));overage=max(0,net_meals-4500)
  self.assertEqual((net_meals,overage),(4705,205))
  ready=primary['T01']+primary['T02']-overage+primary['T03']+(primary['T04']-1200)+primary['T05']
  self.assertEqual(ready,7774)
if __name__=='__main__':unittest.main(verbosity=2)
