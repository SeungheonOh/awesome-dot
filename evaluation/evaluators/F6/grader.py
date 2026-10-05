import argparse,csv,hashlib,importlib.util,io,json,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
import importlib.util as _io_import
_io_spec=_io_import.spec_from_file_location('f6_safe_io',HERE/'safe_io.py');safe_io=_io_import.module_from_spec(_io_spec);_io_spec.loader.exec_module(safe_io)
_spec=importlib.util.spec_from_file_location('f6_oracle',HERE/'oracle.py');oracle=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(oracle)
def run_query(sql,database,params):
    try:
        database=Path(database)
        verified_bytes=safe_io.regular_bytes(database.parent,database.name,1048576)
        with tempfile.TemporaryDirectory() as td:
            staged=Path(td)/'fixture.sqlite3';staged.write_bytes(verified_bytes)
            request={'sql':sql,'database':str(staged),'params':params}
            p=subprocess.run([sys.executable,'-I',str(HERE/'sql_worker.py')],input=json.dumps(request),text=True,capture_output=True,cwd=td,timeout=6,env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8'})
        if p.returncode!=0:return {'ok':False,'classification':'infrastructure_failure' if p.returncode>0 else 'execution_resource_limit','error':f'Isolated SQLite worker exited {p.returncode}'}
        if len(p.stdout.encode('utf-8'))>1048576:return {'ok':False,'error':'SQL worker response exceeds public byte bound'}
        return json.loads(p.stdout)
    except subprocess.TimeoutExpired as exc:return {'ok':False,'classification':'execution_resource_limit','error':'SQL worker exceeded the public wall-clock limit'}
    except safe_io.FileIssue as exc:return {'ok':False,'classification':'protected_input_failure','error':str(exc)}
    except Exception as exc:return {'ok':False,'classification':'infrastructure_failure','error':f'{type(exc).__name__}: {exc}'}
def grade(submission_dir,runner_dir):
    submission,runner=Path(submission_dir),Path(runner_dir)
    assertions={f'g{i}':[] for i in range(1,6)}
    def ck(g,ok,why):assertions[g].append({'passed':bool(ok),'reason':why})
    trusted=json.loads((HERE/'trusted-input-manifest.json').read_text())
    integrity=[]
    for source in [{'path':k,'sha256':v} for k,v in trusted['runner_files'].items()]:
        ok,why=safe_io.hash_check(runner,source['path'],source['sha256'])
        integrity.append({'passed':ok,'reason':'Protected source bytes: '+source['path']+'; '+why})
    try:sql=safe_io.regular_text(submission,'report.sql',100000)
    except Exception as exc:sql='';ck('g4',False,'Readable report.sql: '+type(exc).__name__)
    results=[]
    for i,params in enumerate(oracle.DATA['scenarios']):
        result=run_query(sql,runner/'inputs/orders.sqlite3',params) if all(x['passed'] for x in integrity) else {'ok':False,'error':'Protected input integrity failed; SQL not executed'};results.append(result)
        expected=oracle.expected(params)
        shape=result.get('ok') and result.get('columns')==oracle.COLUMNS and isinstance(result.get('rows'),list)
        rows=result.get('rows',[]) if shape else []
        valid_rows=all(isinstance(row,list) and len(row)==len(oracle.COLUMNS) for row in rows)
        if not valid_rows:rows=[];shape=False
        typed=all(isinstance(row[0],str) and all(type(x) is int or (x is None and j in {6,8}) for j,x in enumerate(row) if j>0) for row in rows)
        ck('g1',shape and typed and [(r[0],r[1]) for r in rows]==[(r[0],r[1]) for r in expected],f'Scenario {i}: cohort channels/counts, half-open period, statuses and integer output')
        ck('g2',shape and [[r[j] for j in [0,1,2,3,7,9]] for r in rows]==[[r[j] for j in [0,1,2,3,7,9]] for r in expected],f'Scenario {i}: entity IDs counted once; equal amounts retained; refund cutoff exact')
        ck('g3',shape and [[r[j] for j in [0,4,5,6,8,9]] for r in rows]==[[r[j] for j in [0,4,5,6,8,9]] for r in expected],f'Scenario {i}: complete-zero, partial/unknown and mandatory unallocated treatment')
        ck('g4',shape and typed and rows==expected,f'Scenario {i}: safe saved SQL output equals independent source calculation'+('' if result.get('ok') else '; '+result.get('error','execution failed')))
    try:
        raw=safe_io.regular_text(submission,'result.csv',1048576);parsed=list(csv.reader(io.StringIO(raw)))
        ck('g5',bool(parsed) and parsed[0]==oracle.COLUMNS,'Saved CSV exact header order')
        data=[]
        for row in parsed[1:]:
            if len(row)!=10:raise ValueError('CSV row width')
            converted=[row[0]]
            for col,s in enumerate(row[1:],1):
                if s=='NULL' and col in {6,8}:converted.append(None)
                elif s==str(int(s)):converted.append(int(s))
                else:raise ValueError('Noncanonical integer')
            data.append(converted)
        ck('g5',data==oracle.expected(oracle.DATA['scenarios'][0]),'Saved main CSV matches independent amounts/counts')
        ck('g5',results[0].get('ok') and results[0].get('rows')==data,'Saved CSV agrees with the saved query actually executed')
    except Exception as exc:ck('g5',False,'Readable compliant CSV: '+str(exc))
    try:notes=safe_io.regular_text(submission,'report-notes.txt',1048576).splitlines()
    except Exception:notes=[]
    for line in oracle.DATA['notes']:ck('g5',notes.count(line)==1,'Required notes declaration: '+line)
    labels=[x.split(':',1)[0]+':' for x in oracle.DATA['notes']]
    ck('g5',all(sum(s.startswith(label) for s in notes)==1 for label in labels),'Notes do not contain conflicting duplicate declarations')
    groups=[{'id':id,'passed':all(a['passed'] for a in aa),'reasons':[a['reason'] for a in aa if not a['passed']],'assertions':aa} for id,aa in assertions.items()]
    # Check again after executing submitted SELECT statements, including the database bytes.
    for source in [{'path':k,'sha256':v} for k,v in trusted['runner_files'].items()]:
        ok,why=safe_io.hash_check(runner,source['path'],source['sha256']);integrity.append({'passed':ok,'reason':'Post-query protected bytes: '+source['path']+'; '+why})
    ip=all(x['passed'] for x in integrity)
    result={'case_id':'F6','integrity':{'passed':ip,'reasons':[x['reason'] for x in integrity if not x['passed']],'assertions':integrity},'groups':groups,'accepted':ip and all(g['passed'] for g in groups),'quality':sum(g['passed'] for g in groups)/5}
    infrastructure=[x.get('error','Trusted worker unavailable') for x in results if x.get('classification')=='infrastructure_failure']
    if infrastructure:
        for group in result['groups']:
            group['passed']=None;group['reasons']=['Ungraded: trusted SQL execution infrastructure failed']+infrastructure
        result['accepted']=None if ip else False;result['quality']=None;result['blocked_reason']='trusted_sql_worker_infrastructure_failure'
    return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--submission',required=True);p.add_argument('--runner',required=True);a=p.parse_args();print(json.dumps(grade(a.submission,a.runner),indent=2))
