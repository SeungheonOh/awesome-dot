"""Author-owned deterministic fixture builder and independent, non-SQL oracle."""
import collections, datetime as dt, json, pathlib, random, sqlite3
ROOT=pathlib.Path(__file__).resolve().parents[1]
SEED=810327
SCHEMA='''
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, region TEXT NOT NULL);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, family TEXT NOT NULL);
CREATE TABLE invoices(invoice_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, invoice_date TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL, currency TEXT NOT NULL);
CREATE TABLE invoice_lines(line_id INTEGER PRIMARY KEY, invoice_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, unit_price_cents INTEGER NOT NULL);
CREATE TABLE adjustments(adjustment_id INTEGER PRIMARY KEY, line_id INTEGER NOT NULL, amount_cents INTEGER NOT NULL, effective_date TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL);
CREATE TABLE receipts(receipt_id INTEGER PRIMARY KEY, line_id INTEGER NOT NULL, amount_cents INTEGER NOT NULL, effective_date TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL);
CREATE TABLE fulfillments(fulfillment_id INTEGER PRIMARY KEY, line_id INTEGER NOT NULL, quantity INTEGER NOT NULL, effective_date TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL);
'''
PARAMS=[dict(name='quarter_close',report_start='2026-04-01',report_end='2026-07-01',as_of='2026-07-07T23:59:59Z'),dict(name='may_early',report_start='2026-05-01',report_end='2026-06-01',as_of='2026-06-02T12:00:00Z'),dict(name='june_late',report_start='2026-06-01',report_end='2026-07-01',as_of='2026-07-20T23:59:59Z')]
def build():
 r=random.Random(SEED); data={k:[] for k in ['customers','products','invoices','invoice_lines','adjustments','receipts','fulfillments']}
 for i in range(1,13): data['customers'].append([i,['North','South','West'][i%3]])
 for i in range(1,10): data['products'].append([i,['Storage','Compute','Support'][i%3]])
 origin=dt.date(2026,3,28); lineid=0
 for i in range(1,241):
  date=origin+dt.timedelta(days=(i*11)%102); date_s=date.isoformat()
  posted=(date+dt.timedelta(days=r.choice([0,0,1,5,16]))).isoformat()+'T'+r.choice(['09:00:00Z','13:00:00Z'])
  data['invoices'].append([i,1+(i%12),date_s,posted,'void' if i%17==0 else 'draft' if i%23==0 else 'issued',['USD','EUR'][i%2]])
  for j in range(1,1+r.randint(1,5)):
   lineid+=1; qty=r.randint(1,12); price=r.choice([199,500,1250,3499,8000]); data['invoice_lines'].append([lineid,i,1+r.randrange(9),qty,price])
   for table,maxn,ok in [('adjustments',3,'approved'),('receipts',4,'settled'),('fulfillments',3,'posted')]:
    for z in range(r.randint(0,maxn)):
     eff=date+dt.timedelta(days=r.choice([0,1,5,14,30,45])); post=eff+dt.timedelta(days=r.choice([0,0,1,7,21]))
     amount=r.choice([-500,-199,75,200,1000]) if table=='adjustments' else (r.choice([-300,-99,100,500,2500,qty*price]) if table=='receipts' else r.choice([-2,-1,1,2,qty]))
     data[table].append([len(data[table])+1,lineid,amount,eff.isoformat(),post.isoformat()+'T'+r.choice(['09:00:00Z','13:00:00Z']),ok if r.random()<0.8 else 'pending'])
 # Explicit boundary and fanout anchor: all requirements remain general and visible.
 data['invoices'] += [[1001,1,'2026-04-01','2026-04-01T00:00:00Z','issued','USD'],[1002,1,'2026-07-01','2026-07-01T00:00:00Z','issued','USD'],[1003,2,'2026-05-31','2026-06-02T12:00:00Z','issued','EUR'],[1004,2,'2026-05-31','2026-06-02T12:00:01Z','issued','EUR']]
 data['invoice_lines'] += [[10001,1001,1,4,1000],[10002,1001,1,1,500],[10003,1001,2,2,750],[10004,1002,1,9,1000],[10005,1003,3,1,991],[10006,1004,3,1,997]]
 for row in [[10001,-200,'2026-06-01','2026-06-01T10:00:00Z','approved'],[10001,75,'2026-06-02','2026-06-02T11:00:00Z','approved'],[10001,-999,'2026-06-01','2026-06-01T11:00:00Z','pending'],[10002,17,'2026-07-07','2026-07-07T23:59:59Z','approved'],[10002,19,'2026-07-08','2026-07-07T23:59:59Z','approved'],[10002,23,'2026-07-07','2026-07-08T00:00:00Z','approved']]: data['adjustments'].append([len(data['adjustments'])+1]+row)
 for row in [[10001,2000,'2026-06-01','2026-06-01T10:00:00Z','settled'],[10001,1000,'2026-06-02','2026-06-02T11:00:00Z','settled'],[10001,-100,'2026-06-02','2026-06-02T11:30:00Z','settled']]:data['receipts'].append([len(data['receipts'])+1]+row)
 for row in [[10001,3,'2026-06-01','2026-06-01T10:00:00Z','posted'],[10001,2,'2026-06-02','2026-06-02T11:00:00Z','posted'],[10001,-1,'2026-06-03','2026-06-03T11:00:00Z','posted']]:data['fulfillments'].append([len(data['fulfillments'])+1]+row)
 return data
COLS=['report_month','region','family','currency','line_count','invoice_count','billed_units','gross_cents','adjustment_cents','net_cents','received_cents','balance_cents','fulfilled_units']
def oracle(data,p):
 customers=dict(data['customers']);products=dict(data['products']);invoices={x[0]:x for x in data['invoices']};sums={}
 for table,ok in [('adjustments','approved'),('receipts','settled'),('fulfillments','posted')]:
  d=collections.defaultdict(int)
  for eid,lid,amount,effective,posted,status in data[table]:
   if status==ok and effective<=p['as_of'][:10] and posted<=p['as_of']:d[lid]+=amount
  sums[table]=d
 buckets={}
 for lid,iid,pid,qty,price in data['invoice_lines']:
  _,cid,date,posted,status,currency=invoices[iid]
  if status!='issued' or not(p['report_start']<=date<p['report_end']) or posted>p['as_of']:continue
  key=(date[:7],customers[cid],products[pid],currency)
  b=buckets.setdefault(key,dict(line_count=0,ids=set(),billed_units=0,gross_cents=0,adjustment_cents=0,received_cents=0,fulfilled_units=0))
  b['line_count']+=1;b['ids'].add(iid);b['billed_units']+=qty;b['gross_cents']+=qty*price
  b['adjustment_cents']+=sums['adjustments'][lid];b['received_cents']+=sums['receipts'][lid];b['fulfilled_units']+=sums['fulfillments'][lid]
 result=[]
 for key,b in sorted(buckets.items()):
  b['invoice_count']=len(b.pop('ids'));b['net_cents']=b['gross_cents']+b['adjustment_cents'];b['balance_cents']=b['net_cents']-b['received_cents'];result.append(dict(zip(COLS[:4],key),**b))
 return result
if __name__=='__main__':
 data=build(); out=ROOT/'candidate/inputs';db=out/'billing.sqlite'
 if db.exists():db.unlink()
 with sqlite3.connect(db) as c:
  c.executescript(SCHEMA)
  for table,rows in data.items():c.executemany('INSERT INTO '+table+' VALUES ('+','.join('?'*len(rows[0]))+')',rows)
 (out/'schema.sql').write_text(SCHEMA);(out/'ledger.json').write_text(json.dumps(data,indent=2)+'\n');(out/'scenarios.json').write_text(json.dumps(PARAMS,indent=2)+'\n')
 (ROOT/'private/expected.json').write_text(json.dumps({p['name']:oracle(data,p) for p in PARAMS},indent=2)+'\n')
 print(json.dumps({k:len(v) for k,v in data.items()}))
