import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('f6_grader',HERE/'grader.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class GraderTests(unittest.TestCase):
 def test_reference(self):self.assertTrue(g.grade(HERE/'reference',HERE.parents[1]/'cases/F6')['accepted'])
 def test_controls(self):
  for c in json.loads((HERE/'controls/index.json').read_text()):
   with self.subTest(control=c['name']),tempfile.TemporaryDirectory() as td:
    runner=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F6',runner)
    if 'runner_mutation' in c:
     m=c['runner_mutation'];p=runner/m['path'];p.write_text(p.read_text()+m['append'])
    result=g.grade(HERE/c['submission'],runner)
    self.assertEqual(result['accepted'],c['accepted'])
    statuses={x['id']:x['passed'] for x in result['groups']};statuses['integrity']=result['integrity']['passed']
    for id in c['must_fail']:self.assertFalse(statuses[id],json.dumps(result))
    if 'expected_matrix' in c:self.assertEqual(statuses,c['expected_matrix'])
if __name__=='__main__':unittest.main()

class OracleIndependenceTests(unittest.TestCase):
 def test_direct_main_calculation(self):
  # Independently hand-tallied records: web 1250+1000; desk 0+800+800;
  # phone partial 0+180 with unknown gross; refunds 450,320,70 and orphan77.
  expected=[['__unallocated__',0,0,0,0,0,0,77,None,1],['desk',3,3,1600,0,1,1600,320,1280,0],['phone',2,1,180,2,0,None,70,None,0],['web',2,4,2250,0,0,2250,450,1800,0]]
  self.assertEqual(g.oracle.expected(g.oracle.DATA['scenarios'][0]),expected)
 def test_exports_match_sqlite_rows(self):
  import csv,sqlite3
  uri=(HERE.parents[1]/'cases/F6/inputs/orders.sqlite3').resolve().as_uri()+'?mode=ro'
  conn=sqlite3.connect(uri,uri=True)
  try:
   for table in ['orders','line_items','refunds']:
    with (HERE.parents[1]/f'cases/F6/inputs/{table}.csv').open(newline='') as f:export=list(csv.reader(f))
    stored=conn.execute('SELECT * FROM '+table).fetchall()
    self.assertEqual([[str(x) for x in row] for row in stored],export[1:])
  finally:conn.close()
 def test_readonly_security(self):
  db=HERE.parents[1]/'cases/F6/inputs/orders.sqlite3';p=g.oracle.DATA['scenarios'][0]
  for sql in ['DROP TABLE orders','PRAGMA query_only=OFF',"ATTACH DATABASE ':memory:' AS x",'SELECT load_extension(\'bad\')','SELECT writefile(\'/tmp/nope\',\'bad\')']:
   with self.subTest(sql=sql):self.assertFalse(g.run_query(sql,db,p)['ok'])


class SafeIngestionTests(unittest.TestCase):
 def test_symlink_artifact_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   p=d/'report.sql';p.unlink();p.symlink_to((HERE/'reference/report.sql').resolve())
   self.assertFalse(g.grade(d,HERE.parents[1]/'cases/F6')['accepted'])
 def test_symlink_input_integrity_failure(self):
  with tempfile.TemporaryDirectory() as td:
   r=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F6',r)
   p=r/'inputs/schema.sql';p.unlink();p.symlink_to((HERE.parents[1]/'cases/F6/inputs/schema.sql').resolve())
   self.assertFalse(g.grade(HERE/'reference',r)['integrity']['passed'])
 def test_directory_input_integrity_failure(self):
  with tempfile.TemporaryDirectory() as td:
   r=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F6',r)
   p=r/'inputs/schema.sql';p.unlink();p.mkdir()
   self.assertFalse(g.grade(HERE/'reference',r)['integrity']['passed'])
 def test_oversized_artifact_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   (d/'report.sql').write_bytes(b' '*100001)
   self.assertFalse(g.grade(d,HERE.parents[1]/'cases/F6')['accepted'])
 def test_aggregate_worker_output_is_bounded(self):
  sql='SELECT '+','.join("printf('%200000s','x') AS c"+str(i) for i in range(6))
  result=g.run_query(sql,HERE.parents[1]/'cases/F6/inputs/orders.sqlite3',g.oracle.DATA['scenarios'][0])
  self.assertFalse(result['ok']);self.assertLess(len(json.dumps(result)),1000)


class FullPacketIntegrityTests(unittest.TestCase):
 def test_task_and_manifest_are_evaluator_bound(self):
  for rel in ['task.txt','input-manifest.json']:
   with self.subTest(path=rel),tempfile.TemporaryDirectory() as td:
    r=Path(td)/'runner';shutil.copytree(HERE.parents[1]/'cases/F6',r)
    p=r/rel;p.write_bytes(p.read_bytes()+b'\n')
    self.assertFalse(g.grade(HERE/'reference',r)['integrity']['passed'])

 def test_infrastructure_error_is_ungraded(self):
  from unittest.mock import patch
  with patch.object(g.subprocess,'run',side_effect=OSError('trusted worker unavailable')):
   result=g.grade(HERE/'reference',HERE.parents[1]/'cases/F6')
  self.assertIsNone(result['accepted']);self.assertIsNone(result['quality'])
  self.assertTrue(all(x['passed'] is None for x in result['groups']))
  self.assertEqual(result['blocked_reason'],'trusted_sql_worker_infrastructure_failure')


class NotesEquivalenceTests(unittest.TestCase):
 def test_crlf_notes_are_accepted(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td)/'output';shutil.copytree(HERE/'reference',d)
   p=d/'report-notes.txt';p.write_bytes(p.read_bytes().replace(b'\n',b'\r\n'))
   self.assertTrue(g.grade(d,HERE.parents[1]/'cases/F6')['accepted'])
