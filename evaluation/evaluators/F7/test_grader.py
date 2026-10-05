import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('f7_grader',HERE/'grader.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class GraderTests(unittest.TestCase):
 def test_reference(self):self.assertTrue(g.grade(HERE/'reference',HERE.parents[1]/'cases/F7')['accepted'])
 def test_controls(self):
  for c in json.loads((HERE/'controls/index.json').read_text()):
   with self.subTest(control=c['name']),tempfile.TemporaryDirectory() as td:
    runner=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F7',runner)
    if 'runner_mutation' in c:
     m=c['runner_mutation'];p=runner/m['path'];p.write_text(p.read_text()+m['append'])
    result=g.grade(HERE/c['submission'],runner)
    self.assertEqual(result['accepted'],c['accepted'])
    statuses={x['id']:x['passed'] for x in result['groups']};statuses['integrity']=result['integrity']['passed']
    for id in c['must_fail']:self.assertFalse(statuses[id],json.dumps(result))
    if 'expected_matrix' in c:self.assertEqual(statuses,c['expected_matrix'])
if __name__=='__main__':unittest.main()

class InterpreterTests(unittest.TestCase):
 def test_empty_slash_tilde(self):
  self.assertEqual(g.apply({'a/b':{'~':{'':1}}},[{'op':'replace','path':'/a~1b/~0/','value':2}]),{'a/b':{'~':{'':2}}})
 def test_array_insert_and_append(self):
  self.assertEqual(g.apply({'x':[1,3]},[{'op':'add','path':'/x/1','value':2},{'op':'add','path':'/x/-','value':4}]),{'x':[1,2,3,4]})
 def test_object_order_irrelevant(self):self.assertTrue(g.exact({'x':1,'y':2},{'y':2,'x':1}))
 def test_bool_not_integer(self):self.assertFalse(g.exact(True,1))
 def test_large_integer(self):self.assertEqual(g.strict_loads('9007199254740993'),9007199254740993)
 def test_reject_fraction_exponent_constant_duplicate(self):
  for text in ['1.0','1e0','NaN','Infinity','{"x":1,"x":2}']:
   with self.subTest(text=text),self.assertRaises(g.Invalid):g.strict_loads(text)
 def test_bad_pointer_and_index(self):
  for path in ['/x/01','/x/-','/x/3','/x/~2']:
   with self.subTest(path=path),self.assertRaises(g.Invalid):g.apply({'x':[1]},[{'op':'remove','path':path}])
 def test_long_integer_without_precision_limit(self):self.assertEqual(g.strict_loads('9'*5000),10**5000-1)
 def test_duplicate_diagnostic_path(self):
  with self.assertRaises(g.Invalid) as cm:g.strict_loads('{"a/b":[{"~":1,"~":2}]}')
  self.assertEqual((cm.exception.code,cm.exception.pointer),('duplicate_key','/a~1b/0/~0'))


class SafeIngestionTests(unittest.TestCase):
 def test_symlink_artifact_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   p=d/'patch.json';p.unlink();p.symlink_to((HERE/'reference/patch.json').resolve())
   self.assertFalse(g.grade(d,HERE.parents[1]/'cases/F7')['accepted'])
 def test_symlink_input_integrity_failure(self):
  with tempfile.TemporaryDirectory() as td:
   r=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F7',r)
   p=r/'inputs/before.json';p.unlink();p.symlink_to((HERE.parents[1]/'cases/F7/inputs/before.json').resolve())
   self.assertFalse(g.grade(HERE/'reference',r)['integrity']['passed'])
 def test_directory_input_integrity_failure(self):
  with tempfile.TemporaryDirectory() as td:
   r=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F7',r)
   p=r/'inputs/before.json';p.unlink();p.mkdir()
   self.assertFalse(g.grade(HERE/'reference',r)['integrity']['passed'])
 def test_oversized_artifact_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   (d/'patch.json').write_bytes(b' '*16385)
   self.assertFalse(g.grade(d,HERE.parents[1]/'cases/F7')['accepted'])
 def test_unicode_separator_cannot_replace_lf(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   p=d/'change-summary.txt';s=p.read_text();p.write_text(s[:-1].replace('\n','\u2028')+'\n')
   self.assertFalse(g.grade(d,HERE.parents[1]/'cases/F7')['accepted'])
 def test_nondict_status_is_recorded_failure(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   p=d/'validation-status.json';j=json.loads(p.read_text());j['valid_pair']=[];p.write_text(json.dumps(j))
   self.assertFalse(g.grade(d,HERE.parents[1]/'cases/F7')['accepted'])


class FullPacketIntegrityTests(unittest.TestCase):
 def test_task_and_manifest_are_evaluator_bound(self):
  for rel in ['task.txt','input-manifest.json']:
   with self.subTest(path=rel),tempfile.TemporaryDirectory() as td:
    r=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F7',r)
    p=r/rel;p.write_bytes(p.read_bytes()+b'\n')
    self.assertFalse(g.grade(HERE/'reference',r)['integrity']['passed'])
