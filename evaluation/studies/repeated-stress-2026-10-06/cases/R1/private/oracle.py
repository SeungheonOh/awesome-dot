"""Author-only source-derived integer/Decimal oracle; never imports candidate code."""
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
import csv,json
ROOT=Path(__file__).resolve().parents[1]
def cents(s): return int((Decimal(s)*100).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
def build():
 p=ROOT/'candidate'/'inputs'
 def rows(name):
  with (p/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
 claims=rows('claims.csv'); receipts={x['receipt_id']:x for x in rows('receipts.csv')}; bank=rows('statement.csv')
 out=[]
 for c in claims:
  cid=c['claim_id']; cat=c['category']; rid=c['receipt_id'];rec=receipts.get(rid)
  settled=[s for s in bank if s['claim_link']==cid and s['state']=='settled']
  charges=[s for s in settled if s['direction']=='charge'];credits=sum(cents(s['amount']) for s in settled if s['direction']=='credit')
  evid=[rid] if rid else []
  evid += [s['statement_id'] for s in settled]
  late=c['service_date']>='2026-09-15'; policy='P2' if late else 'P1'; evid.append(policy)
  gross=cents(charges[0]['amount']) if charges else (cents(c['claimed_amount']) if c['currency']=='USD' else None)
  row={'claim_id':cid,'disposition':'reimbursable','approved_usd_cents':gross,'reimbursement_usd_cents':gross,'excluded_usd_cents':0,'held_usd_cents':0,'credit_usd_cents':credits,'duplicate_of':None,'evidence_ids':evid,'note':'Supported business expense'}
  if cid=='C007':
   row.update(disposition='duplicate',approved_usd_cents=0,reimbursement_usd_cents=0,duplicate_of='C001',note='R001 already reimbursed only through canonical C001');evid.append('E05')
  elif cid in ('C017','C018','C026','C028'):
   known=cents(c['claimed_amount']) if c['currency']=='USD' else None
   row.update(disposition='hold',approved_usd_cents=0 if known is not None else None,reimbursement_usd_cents=0,excluded_usd_cents=0 if known is not None else None,held_usd_cents=known,note={'C017':'Required itemized receipt missing','C018':'Attendees/count missing; do not guess a per-person allowance','C026':'Approved cash FX rate missing; EUR 24.00 unvalued','C028':'Receipt 79.00 versus settled charge 89.00 unexplained'}[cid]);evid.append('E05')
  elif cid=='C025':row.update(disposition='ineligible',approved_usd_cents=0,reimbursement_usd_cents=0,excluded_usd_cents=gross,note='Explicitly personal')
  else:
   eligible=gross
   if cat in ('breakfast','lunch','dinner'):
    caps=({'breakfast':2000,'lunch':3000,'dinner':8000} if late else {'breakfast':1500,'lunch':2500,'dinner':6500})
    if rec and c['currency']=='USD':
     food=Decimal(rec['food_pre_tax']);alcohol=Decimal(rec['alcohol_pre_tax']);tax=Decimal(rec['tax'])
     eligible=cents(str(food+tax*food/(food+alcohol)))
    eligible=min(eligible,caps[cat])
   elif cat=='taxi':
    cap=9500 if cid=='C013' else (7500 if late else 6000)
    eligible=min(gross,cap)
    if cid=='C013':evid.append('E02')
   elif cat=='hotel':
    cap=23000 if cid=='C010' else 18000
    eligible=min(cents(rec['room_per_night']),cap)*int(rec['nights'])+cents(rec['tax'])
    if cid=='C010':eligible-=cents(rec['deposit_applied']);evid+=['R021','E01']
   elif cid=='C021':evid+=['R010','E01']
   if cid in ('C019','C020'):evid.append('E03')
   if cid=='C024':evid.append('E04')
   claimed=gross if c['currency']!='USD' else cents(c['claimed_amount'])
   excluded=max(0,claimed-eligible)
   net=max(0,eligible-credits)
   row.update(approved_usd_cents=net,reimbursement_usd_cents=net,excluded_usd_cents=excluded)
   if c['paid_by']=='company':row.update(disposition='corporate_paid',reimbursement_usd_cents=0,note='Company settled directly; no employee payment')
   elif credits and net==0:row.update(disposition='refunded',note='Settled credit fully offsets original charge')
   elif excluded or credits:row.update(disposition='partial',note='Cap, supported final adjustment, or settled partial credit reduces payable amount')
  out.append(row)
 totals={field:sum(x[field] or 0 for x in out) for field in ('reimbursement_usd_cents','approved_usd_cents','excluded_usd_cents','held_usd_cents','credit_usd_cents')}
 totals['corporate_paid_usd_cents']=sum(x['approved_usd_cents'] for x in out if x['disposition']=='corporate_paid')
 totals['unvalued_holds']=[{'claim_id':'C026','currency':'EUR','original_amount':'24.00'}]
 return {'claims':out,'totals':totals}
if __name__=='__main__':print(json.dumps(build(),indent=2))
