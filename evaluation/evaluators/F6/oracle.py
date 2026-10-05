"""Direct entity calculation, deliberately independent of the SQL reference."""
import json
from pathlib import Path
COLUMNS=['channel','order_count','line_row_count','known_gross_minor','incomplete_order_count','complete_zero_order_count','gross_minor','refund_minor','net_minor','unallocated_refund_count']
DATA=json.loads((Path(__file__).parent/'oracle-inputs.json').read_text())
def expected(params):
    # An event/entity ledger: each source ID is visited once; no SQL or reference query is used.
    order_by_id={o['order_id']:o for o in DATA['orders']}
    chosen={o['order_id']:o for o in DATA['orders'] if o['status'] in {'settled','shipped'} and params['period_start']<=o['ordered_at']<params['period_end']}
    amounts={id:0 for id in chosen};counts={id:0 for id in chosen}
    for line in DATA['line_items']:
        id=line['order_id']
        if id in chosen:
            amounts[id]+=line['quantity']*line['unit_minor'];counts[id]+=1
    output={}
    for id,order in chosen.items():
        channel=order['channel']
        row=output.setdefault(channel,[channel,0,0,0,0,0,0,0,0,0])
        row[1]+=1;row[2]+=counts[id];row[3]+=amounts[id]
        row[4]+=int(order['items_complete']==0)
        row[5]+=int(order['items_complete']==1 and amounts[id]==0)
    orphan=['__unallocated__',0,0,0,0,0,0,0,None,0]
    for refund in DATA['refunds']:
        if refund['event_at']>params['as_of']:continue
        id=refund['order_id']
        if id in chosen:output[chosen[id]['channel']][7]+=refund['amount_minor']
        elif id not in order_by_id:orphan[7]+=refund['amount_minor'];orphan[9]+=1
    for row in output.values():
        row[6]=None if row[4] else row[3]
        row[8]=None if row[6] is None else row[6]-row[7]
    output[orphan[0]]=orphan
    return [output[k] for k in sorted(output)]
