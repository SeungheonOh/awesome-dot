"""Independent count/date/identity audit of the author-only adjudicated state."""
import json,csv
from pathlib import Path
from datetime import date
P=Path(__file__).resolve().parent
x=json.loads((P/'expected.json').read_text())
with (P.parent/'candidate/inputs/baseline.csv').open(newline='') as f: ids={r['action_id'] for r in csv.DictReader(f)}
assert {r['action_id'] for r in x['actions']}==ids and len(x['actions'])==34
active=[r for r in x['actions'] if r['status'] not in ('done','cancelled')]
overdue=[r['action_id'] for r in active if r['due_date'] and date.fromisoformat(r['due_date'])<date(2026,9,30)]
assert set(overdue)=={'A03','A11','A12','A21'}
assert len(active)==18
assert x['totals']['by_status']=={'open':9,'blocked':7,'done':12,'cancelled':4,'unresolved':2}
assert x['totals']['active_count']==len(active) and x['totals']['overdue_count']==len(overdue)
assert {r['action_id']:r['dependencies'] for r in x['actions'] if r['dependencies']}=={'A25':['A03','A21'],'A28':['A25']}
assert sum(r['owner'] is None for r in x['actions'])==1
assert sum(r['due_date'] is None for r in x['actions'])==1
print('R2 identity, independent date arithmetic, counts, dependency and null audits passed')
