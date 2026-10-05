import unittest,json,tempfile,shutil
from pathlib import Path
from grade import grade,HERE
P=HERE.parents[1]/'cases/F2'
class GraderTests(unittest.TestCase):
 def setUp(self):self.review=json.loads((HERE/'reference-review.json').read_text())
 def test_reference_accepted(self):self.assertTrue(grade(P,HERE/'reference',self.review)['accepted'])
 def test_paraphrase_and_reordering_accepted(self):self.assertTrue(grade(P,HERE/'controls/accepted-paraphrase',json.loads((HERE/'controls/accepted-paraphrase-review.json').read_text()))['accepted'])
 def test_no_semantic_scores_means_pending(self):
  r=grade(P,HERE/'reference');self.assertIsNone(r['accepted']);self.assertEqual(r['quality']['scored_groups'],0)
 def test_each_group_adverse_control(self):
  names=['missing-agreement','collapsed-labels','rejected-authority','draft-is-sent','vague-question']
  for i,name in enumerate(names,1):
   base='bad-g%d-%s'%(i,name);review=json.loads((HERE/('controls/'+base+'-review.json')).read_text())
   r=grade(P,HERE/('controls/'+base),review);self.assertFalse(r['groups'][i-1]['passed'],base);self.assertFalse(r['accepted'])
 def test_wordcount_and_dangling_ref_are_objective(self):
  for name in ['bad-g5-word-limit','bad-g5-dangling-reference']:
   r=grade(P,HERE/('controls/'+name),self.review);self.assertFalse(r['groups'][4]['passed'])
 def test_source_mutation_fails(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'p';shutil.copytree(P,p);f=p/'inputs/meeting.txt';f.write_bytes(f.read_bytes()+b'\n');self.assertFalse(grade(p,HERE/'reference',self.review)['integrity']['passed'])
 def test_missing_submission_does_not_crash(self):
  with tempfile.TemporaryDirectory() as t:self.assertFalse(grade(P,Path(t),self.review)['accepted'])
 def test_duplicate_json_keys_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   s=Path(t);shutil.copytree(HERE/'reference',s,dirs_exist_ok=True);f=s/'actions.json';f.write_text('{"actions":[],"actions":[]}');self.assertFalse(grade(P,s,self.review)['groups'][4]['passed'])
 def test_review_hash_mismatch_stays_pending(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);shutil.copytree(HERE/'reference',p,dirs_exist_ok=True);f=p/'handoff.txt';f.write_text(f.read_text()+'\n')
   r=grade(P,p,self.review);self.assertIsNone(r['accepted']);self.assertTrue(all(g['passed'] is None for g in r['groups']))
if __name__=='__main__':unittest.main(verbosity=2)
