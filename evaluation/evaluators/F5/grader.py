"""Source-anchored F5 outcomes. No model or external dependencies."""
import argparse, hashlib, json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
import importlib.util as _io_import
_io_spec=_io_import.spec_from_file_location('f5_safe_io',HERE/'safe_io.py');safe_io=_io_import.module_from_spec(_io_spec);_io_spec.loader.exec_module(safe_io)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text(encoding='utf-8'))
def grade(submission_dir, runner_dir):
    submission, runner = Path(submission_dir), Path(runner_dir)
    key = load(HERE/'oracle.json')
    checks = {f'g{i}': [] for i in range(1,6)}
    def check(g, condition, reason): checks[g].append({'passed':bool(condition),'reason':reason})
    integrity = []
    trusted_runner=load(HERE/'trusted-input-manifest.json')['runner_files']
    for rel, digest in trusted_runner.items():
        ok,why=safe_io.hash_check(runner,rel,digest)
        integrity.append({'passed':ok,'reason':f'Original bytes: {rel}; {why}'})
    try:
        raw=safe_io.regular_bytes(submission,'candidate.txt',1048576)
        txt=raw.decode('utf-8'); lines=[x for x in txt.split('\n') if x.strip()]
    except Exception as exc:
        txt=''; raw=b'';lines=[]
        check('g5',False,f'Candidate readable: {type(exc).__name__}')
    try: ledger=json.loads(safe_io.regular_text(submission,'decisions.json',1048576))
    except Exception as exc:
        ledger={};check('g5',False,f'Ledger readable JSON: {type(exc).__name__}')
    if not isinstance(ledger,dict):ledger={}
    headers=[];sections={};current=None
    for line in lines:
        match=re.fullmatch(r'(\d+)\. (.+) \[([A-Z]+)\]',line)
        if match:
            n,title,anchor=match.groups();headers.append((int(n),title,anchor));current=anchor
            sections.setdefault(anchor,[])
        elif current: sections[current].append(line)
    expected_order=key['expected_anchor_order']
    check('g1',[x[2] for x in headers]==expected_order,'Accepted move and anchor order match A2')
    for anchor,sentence in [('BENCH','Each bench receives three blue cloths.'),('WELCOME','Place visitor badges in the amber tray.'),('HOURS','For the host checklist, see section 4, Closing.')]:
        check('g1',sentence in sections.get(anchor,[]),f'Accepted sentence at {anchor}')
    expected_headers=[(1,'Welcome','WELCOME'),(2,'Opening hours','HOURS'),(3,'Supplies','BENCH'),(4,'Closing','CLOSE'),(5,'Supplies','SHARED'),(6,'Questions','CONTACT')]
    check('g2',headers==expected_headers,'Exactly six required headings, anchors, order and numbers')
    protected='Keep the archive ledger inside the laboratory.'
    check('g2',sections.get('CLOSE',[]).count(protected)==1 and txt.count(protected)==1,'Protected sentence exact, once, at CLOSE')
    check('g2',bool(lines) and lines[0]=='Community Laboratory Handbook','Title preserved exactly')
    records=ledger.get('records',[])
    if not isinstance(records,list):records=[]
    byid={x.get('id'):x for x in records if isinstance(x,dict) and isinstance(x.get('id'),str)}
    expected_byid={x['id']:x for x in key['records']}
    note='Version note: DRAFT — opening hours unresolved; baseline hours retained'
    check('g3',len(lines)>1 and lines[1]==note and lines.count(note)==1,'Explicit global unresolved draft label')
    check('g3',sections.get('HOURS',[])==['Open Tuesday and Thursday, 17:00–20:00.','For the host checklist, see section 4, Closing.'],'Baseline hours retained and independent moved-section reference current')
    for id in ['U-HOURS','D-HOURS-CARD']:
        got=byid.get(id,{})
        wanted=expected_byid[id]
        details=got.get('details')
        if id=='U-HOURS' and isinstance(details,dict):
            details=dict(details)
            alt=details.get('alternatives')
            if isinstance(alt,list) and all(isinstance(x,dict) for x in alt):details['alternatives']=sorted(alt,key=lambda x:json.dumps(x,sort_keys=True))
            wanted_details=dict(wanted['details']);wanted_details['alternatives']=sorted(wanted_details['alternatives'],key=lambda x:json.dumps(x,sort_keys=True))
        else:wanted_details=wanted['details']
        check('g3',got.get('status')==wanted['status'] and details==wanted_details,f'{id} follows authorized uncertainty/dependency treatment')
    check('g4',lines==key['candidate_lines'],'Every substantive candidate line has its authorized basis; no extra unapproved edits')
    for id in ['N-EMAIL','N-CUPBOARD']:
        check('g4',byid.get(id,{}).get('status')=='not_applied',f'{id} explicitly excluded')
    check('g5',raw.endswith(b'\n') and not raw.endswith(b'\n\n') and b'\r' not in raw,'UTF-8/LF candidate with one terminal newline')
    check('g5',set(ledger)=={'candidate_file','candidate_sha256','source_sha256','records'},'Required ledger top-level schema')
    check('g5',ledger.get('candidate_file')=='candidate.txt' and ledger.get('candidate_sha256')==hashlib.sha256(raw).hexdigest(),'Ledger identifies exact saved candidate bytes')
    check('g5',ledger.get('source_sha256')==key['source_hashes'],'Ledger original source hashes agree')
    check('g5',len(records)==8 and len(byid)==8 and set(byid)==set(expected_byid),'Exactly the eight requested dispositions')
    valid_refs={f'{f}#{a}' for f in ['baseline.txt','edit-a.txt','edit-b.txt'] for a in expected_order}|{f'acceptance.txt#A{i}' for i in range(1,8)}|{f'lineage.txt#L{i}' for i in range(1,6)}
    for id,wanted in expected_byid.items():
        got=byid.get(id,{})
        refs=got.get('source_refs',[])
        refs_valid=isinstance(refs,list) and all(isinstance(v,str) for v in refs)
        required=set(wanted['source_refs'])
        if id=='C-MOVE':
            required={'acceptance.txt#A2'}
            supported=refs_valid and bool(set(refs)&{'baseline.txt#CLOSE','baseline.txt#SHARED'}) and bool(set(refs)&{'edit-b.txt#CLOSE','edit-b.txt#SHARED'})
        else:supported=True
        check('g5',refs_valid and required.issubset(refs) and set(refs).issubset(valid_refs) and supported,f'{id}: supporting and authorizing locators resolve')
        gd=got.get('details');wd=wanted['details']
        if id=='U-HOURS' and isinstance(gd,dict):
            gd=dict(gd);wd=dict(wd)
            if isinstance(gd.get('alternatives'),list):gd['alternatives']=sorted(gd['alternatives'],key=lambda x:json.dumps(x,sort_keys=True))
            wd['alternatives']=sorted(wd['alternatives'],key=lambda x:json.dumps(x,sort_keys=True))
        check('g5',set(got)=={'id','status','anchors','source_refs','details'} and got.get('status')==wanted['status'] and got.get('anchors')==wanted['anchors'] and gd==wd,f'{id}: ledger matches source disposition and candidate')
    groups=[{'id':g,'passed':all(c['passed'] for c in cs),'reasons':[c['reason'] for c in cs if not c['passed']],'assertions':cs} for g,cs in checks.items()]
    ip=all(c['passed'] for c in integrity)
    return {'case_id':'F5','integrity':{'passed':ip,'reasons':[c['reason'] for c in integrity if not c['passed']],'assertions':integrity},'groups':groups,'accepted':ip and all(g['passed'] for g in groups),'quality':sum(g['passed'] for g in groups)/5}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--submission',required=True);p.add_argument('--runner',required=True);a=p.parse_args()
    print(json.dumps(grade(a.submission,a.runner),ensure_ascii=False,indent=2))
