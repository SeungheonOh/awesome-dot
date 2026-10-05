"""Trusted evaluator subprocess. Only executes bounded, authorizer-limited SELECT SQL."""
import json,resource,sqlite3,sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024))
resource.setrlimit(resource.RLIMIT_CPU,(3,3))
resource.setrlimit(resource.RLIMIT_FSIZE,(0,0))
resource.setrlimit(resource.RLIMIT_NOFILE,(32,32))
request=json.load(sys.stdin)
c=sqlite3.connect(Path(request['database']).resolve().as_uri()+'?mode=ro',uri=True)
c.enable_load_extension(False)
c.execute('PRAGMA query_only=ON');c.execute('PRAGMA temp_store=MEMORY')
for limit,value in [(sqlite3.SQLITE_LIMIT_LENGTH,1000000),(sqlite3.SQLITE_LIMIT_SQL_LENGTH,100000),(sqlite3.SQLITE_LIMIT_COLUMN,100),(sqlite3.SQLITE_LIMIT_EXPR_DEPTH,200),(sqlite3.SQLITE_LIMIT_COMPOUND_SELECT,50),(sqlite3.SQLITE_LIMIT_VARIABLE_NUMBER,100)]:c.setlimit(limit,value)
allowed={sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ,sqlite3.SQLITE_FUNCTION,sqlite3.SQLITE_RECURSIVE}
def authorizer(action,arg1,arg2,db,source):
 if action not in allowed:return sqlite3.SQLITE_DENY
 if action==sqlite3.SQLITE_READ and db!='main':return sqlite3.SQLITE_DENY
 if action==sqlite3.SQLITE_FUNCTION and (arg2 or arg1 or '').lower() in {'load_extension','readfile','writefile','eval'}:return sqlite3.SQLITE_DENY
 return sqlite3.SQLITE_OK
c.set_authorizer(authorizer)
steps=[0]
def progress():
 steps[0]+=1
 return int(steps[0]>10000)
c.set_progress_handler(progress,100)
try:
 cur=c.execute(request['sql'],request['params'])
 columns=[x[0] for x in cur.description];rows=[]
 used=128+len(json.dumps(columns).encode('utf-8'))
 for _ in range(1001):
  row=cur.fetchone()
  if row is None:break
  used+=len(json.dumps(row).encode('utf-8'))+2
  if used>1048576:raise ValueError('Aggregate serialized result exceeds 1048576 bytes')
  rows.append(row)
 if len(rows)>1000:raise ValueError('Result row limit exceeded')
 result={'ok':True,'columns':columns,'rows':rows}
except Exception as exc:result={'ok':False,'error':f'{type(exc).__name__}: {exc}'}
finally:c.close()
encoded=json.dumps(result)
if len(encoded.encode('utf-8'))>1048576:encoded=json.dumps({'ok':False,'error':'Aggregate serialized result byte bound exceeded'})
print(encoded)
