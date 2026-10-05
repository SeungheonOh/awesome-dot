import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('f5_grader',HERE/'grader.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class GraderTests(unittest.TestCase):
 def test_reference(self):self.assertTrue(g.grade(HERE/'reference',HERE.parents[1]/'cases/F5')['accepted'])
 def test_controls(self):
  for c in json.loads((HERE/'controls/index.json').read_text()):
   with self.subTest(control=c['name']),tempfile.TemporaryDirectory() as td:
    runner=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F5',runner)
    if 'runner_mutation' in c:
     m=c['runner_mutation'];p=runner/m['path'];p.write_text(p.read_text()+m['append'])
    result=g.grade(HERE/c['submission'],runner)
    self.assertEqual(result['accepted'],c['accepted'])
    statuses={x['id']:x['passed'] for x in result['groups']};statuses['integrity']=result['integrity']['passed']
    for id in c['must_fail']:self.assertFalse(statuses[id],json.dumps(result))
    if 'expected_matrix' in c:self.assertEqual(statuses,c['expected_matrix'])
if __name__=='__main__':unittest.main()


class SafeIngestionTests(unittest.TestCase):
 def test_symlink_artifact_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   p=d/'candidate.txt';p.unlink();p.symlink_to((HERE/'reference/candidate.txt').resolve())
   self.assertFalse(g.grade(d,HERE.parents[1]/'cases/F5')['accepted'])
 def test_symlink_input_integrity_failure(self):
  with tempfile.TemporaryDirectory() as td:
   r=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F5',r)
   p=r/'inputs/baseline.txt';p.unlink();p.symlink_to((HERE.parents[1]/'cases/F5/inputs/baseline.txt').resolve())
   self.assertFalse(g.grade(HERE/'reference',r)['integrity']['passed'])
 def test_directory_input_integrity_failure(self):
  with tempfile.TemporaryDirectory() as td:
   r=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F5',r)
   p=r/'inputs/baseline.txt';p.unlink();p.mkdir()
   self.assertFalse(g.grade(HERE/'reference',r)['integrity']['passed'])
 def test_oversized_artifact_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   (d/'candidate.txt').write_bytes(b' '*1048577)
   self.assertFalse(g.grade(d,HERE.parents[1]/'cases/F5')['accepted'])
 def test_unicode_separator_cannot_replace_lf(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   p=d/'candidate.txt';s=p.read_text();p.write_text(s[:-1].replace('\n','\u2028')+'\n')
   self.assertFalse(g.grade(d,HERE.parents[1]/'cases/F5')['accepted'])


class FullPacketIntegrityTests(unittest.TestCase):
 def test_task_and_manifest_are_evaluator_bound(self):
  for rel in ['task.txt','input-manifest.json']:
   with self.subTest(path=rel),tempfile.TemporaryDirectory() as td:
    r=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F5',r)
    p=r/rel;p.write_bytes(p.read_bytes()+b'\n')
    self.assertFalse(g.grade(HERE/'reference',r)['integrity']['passed'])


class LayoutEquivalenceTests(unittest.TestCase):
 def test_unicode_blank_line_whitespace_is_nonsubstantive(self):
  import hashlib
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   p=d/'candidate.txt';p.write_text(p.read_text().replace('\n\n','\n\u00a0\n'))
   ledger=d/'decisions.json';j=json.loads(ledger.read_text());j['candidate_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();ledger.write_text(json.dumps(j))
   self.assertTrue(g.grade(d,HERE.parents[1]/'cases/F5')['accepted'])
