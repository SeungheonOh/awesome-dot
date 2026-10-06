"""Read-only bounded SQL grading. Does not import or execute candidate Python."""
import argparse, hashlib, json, os, pathlib, sqlite3, stat, tempfile, time
HERE=pathlib.Path(__file__).resolve().parent
TABLES={'customers','products','invoices','invoice_lines','adjustments','receipts','fulfillments'}
FUNCS={'sum','total','count','coalesce','substr','substring','strftime','date','datetime','julianday','unixepoch','min','max','abs','round','nullif','ifnull','printf','format','lower','upper','length','trim','ltrim','rtrim','replace','iif','typeof','instr','like','glob','row_number','rank','dense_rank','lag','lead','first_value','last_value','nth_value','ntile','cume_dist','percent_rank','group_concat','hex','quote','unicode','char'}
KEYS=['report_month','region','family','currency']
MEASURES=['line_count','invoice_count','billed_units','gross_cents','adjustment_cents','net_cents','received_cents','balance_cents','fulfilled_units']
CHECKS=['execution','schema_types','grouping_cohort']+MEASURES

def safe_read(path,limit):
 p=pathlib.Path(os.path.abspath(path)); fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
 try:
  for part in p.parts[1:-1]:
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  f=os.open(p.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
  try:
   s=os.fstat(f)
   if not stat.S_ISREG(s.st_mode) or s.st_size>limit:raise ValueError('not a regular bounded file')
   chunks=[];remaining=limit+1
   while remaining:
    b=os.read(f,min(65536,remaining))
    if not b:break
    chunks.append(b);remaining-=len(b)
   result=b''.join(chunks)
   if len(result)>limit:raise ValueError('file grew beyond limit')
   return result
  finally:os.close(f)
 finally:os.close(fd)

def run_sql(sql,db,params):
 con=sqlite3.connect('file:'+str(db)+'?mode=ro&immutable=1',uri=True,timeout=1)
 def authorize(action,a,b,database,source):
  if action==sqlite3.SQLITE_SELECT:return sqlite3.SQLITE_OK
  if action==sqlite3.SQLITE_READ and a in TABLES and (database=='main' or (b=='' and database is None)):return sqlite3.SQLITE_OK
  if action==sqlite3.SQLITE_FUNCTION and (b or '').lower() in FUNCS:return sqlite3.SQLITE_OK
  return sqlite3.SQLITE_DENY
 con.set_authorizer(authorize);started=time.monotonic();ticks=0
 def progress():
  nonlocal ticks
  ticks+=1000
  return int(ticks>50_000_000 or time.monotonic()-started>5)
 con.set_progress_handler(progress,1000)
 for category,value in [(sqlite3.SQLITE_LIMIT_LENGTH,1_000_000),(sqlite3.SQLITE_LIMIT_SQL_LENGTH,65536),(sqlite3.SQLITE_LIMIT_COLUMN,64),(sqlite3.SQLITE_LIMIT_EXPR_DEPTH,100),(sqlite3.SQLITE_LIMIT_COMPOUND_SELECT,20),(sqlite3.SQLITE_LIMIT_ATTACHED,0),(sqlite3.SQLITE_LIMIT_LIKE_PATTERN_LENGTH,1000),(sqlite3.SQLITE_LIMIT_VDBE_OP,100000)]:con.setlimit(category,value)
 try:
  cur=con.execute(sql,{k:v for k,v in params.items() if k!='name'});names=[x[0] for x in cur.description];rows=cur.fetchmany(10001)
  if len(rows)>10000:raise ValueError('result exceeds 10,000 rows')
  return names,rows
 finally:con.close()

def grade(sql_path):
 sql_bytes=safe_read(sql_path,65536);sql=sql_bytes.decode('utf8');fixture=HERE.parent/'candidate/inputs';params=json.loads(safe_read(fixture/'scenarios.json',100000));expected=json.loads(safe_read(HERE/'expected.json',2_000_000))
 statuses={c:{'id':c,'status':'pass','evidence':[]} for c in CHECKS};scenarios=[]
 def note(c,status,evidence):
  old=statuses[c]['status']
  if status=='fail' or (status=='unknown' and old=='pass'):statuses[c]['status']=status
  if len(statuses[c]['evidence'])<6:statuses[c]['evidence'].append(evidence)
 (HERE/'tmp').mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='r3-',dir=HERE/'tmp') as t:
  db=pathlib.Path(t)/'billing.sqlite';db.write_bytes(safe_read(fixture/'billing.sqlite',8_000_000))
  for p in params:
   n=p['name']
   try:names,rows=run_sql(sql,db,p)
   except Exception as e:
    note('execution','fail',{'scenario':n,'error':str(e)});scenarios.append({'name':n,'execution':'fail'})
    for c in CHECKS[1:]:note(c,'unknown',{'scenario':n,'reason':'query did not produce a result'})
    continue
   scenarios.append({'name':n,'execution':'pass','rows':len(rows)})
   if len(names)!=len(KEYS+MEASURES) or set(names)!=set(KEYS+MEASURES):
    note('schema_types','fail',{'scenario':n,'columns':names})
    for c in CHECKS[2:]:note(c,'unknown',{'scenario':n,'reason':'missing or duplicate required columns'})
    continue
   actual=[dict(zip(names,row)) for row in rows]
   good_types=all(all(type(row[k]) is str for k in KEYS) and all(type(row[k]) is int for k in MEASURES) for row in actual)
   if not good_types:note('schema_types','fail',{'scenario':n,'reason':'key must be text; measures must be non-null integers'})
   keys=[tuple(row[k] for k in KEYS) for row in actual];want={tuple(row[k] for k in KEYS):row for row in expected[n]}
   if len(keys)!=len(set(keys)) or set(keys)!=set(want):note('grouping_cohort','fail',{'scenario':n,'actual_rows':len(keys),'expected_rows':len(want),'missing_keys':[list(k) for k in sorted(set(want)-set(keys),key=repr)][:3],'extra_keys':[list(k) for k in sorted(set(keys)-set(want),key=repr)][:3]})
   for c in MEASURES:
    diffs=[{'key':list(k),'actual':row[c],'expected':want[k][c]} for k,row in zip(keys,actual) if k in want and (type(row[c]) is not int or row[c]!=want[k][c])]
    if diffs:note(c,'fail',{'scenario':n,'differences':diffs[:3]})
    elif set(keys)!=set(want) or len(keys)!=len(set(keys)):note(c,'unknown',{'scenario':n,'reason':'measure matched available unique rows, but cohort incomplete/duplicated'})
 return {'case':'R3','source_sha256':hashlib.sha256(sql_bytes).hexdigest(),'checks':list(statuses.values()),'scenarios':scenarios,'totals':{s:sum(c['status']==s for c in statuses.values()) for s in ['pass','fail','unknown']}}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--sql',required=True);args=a.parse_args()
 try:print(json.dumps(grade(args.sql),indent=2,default=repr))
 except Exception as e:print(json.dumps({'case':'R3','status':'ungraded','error':str(e)}));raise SystemExit(2)
