"""Author-owned mutation checks; no model submissions are run here."""
import json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from grade import grade,safe_read
HERE=pathlib.Path(__file__).resolve().parent
ref=safe_read(HERE/'reference.sql',65536).decode()
controls={
 'starter_fanout':(safe_read(HERE.parent/'candidate/output/report.sql',65536).decode(),'gross_cents'),
 'count_lines_as_invoices':(ref.replace('COUNT(DISTINCT e.invoice_id)','COUNT(e.invoice_id)'),'invoice_count'),
 'drop_unpaid_lines':(ref.replace('LEFT JOIN r ON','JOIN r ON'),'grouping_cohort'),
 'ignore_event_posting_cutoff':(ref.replace(' AND posted_at<=:as_of',''),'adjustment_cents'),
 'erase_signed_adjustments':(ref.replace('SUM(amount_cents) AS amount FROM adjustments','SUM(abs(amount_cents)) AS amount FROM adjustments'),'adjustment_cents'),
 'omit_invoice_status':(ref.replace("i.status='issued' AND ",''),'line_count'),
 'write_attempt':('DELETE FROM invoice_lines;','execution')}
results=[]
(HERE/'tmp').mkdir(exist_ok=True)
for name,(sql,check) in controls.items():
 path=HERE/'tmp'/('control_'+name+'.sql');path.write_text(sql);result=grade(path);path.unlink()
 status=next(c['status'] for c in result['checks'] if c['id']==check)
 # Missing coverage can retain every group while still changing line counts.
 if name=='drop_unpaid_lines' and status!='fail':check='line_count';status=next(c['status'] for c in result['checks'] if c['id']==check)
 assert status=='fail',(name,check,result)
 results.append({'control':name,'expected_detected_check':check,'source_sha256':result['source_sha256'],'totals':result['totals'],'validated':True})
print(json.dumps(results,indent=2))
