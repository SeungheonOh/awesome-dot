import argparse,json,os,stat,sys,hashlib
from decimal import Decimal,InvalidOperation
from pathlib import Path
MAX_JSON=524288
MAX_TEXT=131072
MAX_REVIEW=65536

def safe_read(root,name,limit):
    root=Path(os.path.abspath(root))
    if name not in ALLOWED_FILES and name not in ('review_1.json','review_2.json'):
        raise ValueError('Unapproved artifact name')
    for part in (root,*root.parents):
        st=part.lstat()
        if stat.S_ISLNK(st.st_mode):raise ValueError('Symlink directory rejected')
    if not root.is_dir():raise ValueError('Submission directory required')
    dirfd=os.open(str(root),os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        fd=os.open(name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=dirfd)
        try:
            st=os.fstat(fd)
            if not stat.S_ISREG(st.st_mode) or st.st_nlink!=1:raise ValueError('Only singly linked regular artifact files are accepted')
            if st.st_size>limit:raise ValueError('Artifact exceeds declared byte limit')
            with os.fdopen(fd,'rb',closefd=False) as f:data=f.read(limit+1)
            if len(data)>limit:raise ValueError('Artifact exceeds declared byte limit')
            return data.decode('utf-8')
        finally:os.close(fd)
    finally:os.close(dirfd)

def unique_object(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('Duplicate JSON key')
        d[k]=v
    return d

def parse_json(s):
    return json.loads(s,object_pairs_hook=unique_object,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Non-finite JSON number')))

def exact(a,b):
    # JSON booleans must never pass as integer money, counts, or IDs.
    if type(a)!=type(b):return False
    if isinstance(b,dict):return set(a)==set(b) and all(exact(a[k],v) for k,v in b.items())
    if isinstance(b,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def same_unordered_objects(a,b):
    if not isinstance(a,list) or len(a)!=len(b):return False
    return sorted((json.dumps(x,sort_keys=True) for x in a))==sorted((json.dumps(x,sort_keys=True) for x in b))

def compare_fields(actual,expected,ids,fields):
    errors=[]
    for cid in ids:
        if cid not in actual:errors.append(cid+': missing');continue
        for key in fields:
            a=actual[cid].get(key);b=expected[cid][key]
            equal=(isinstance(a,list) and len(a)==len(set(a)) and set(a)==set(b)) if key=='dependencies' else exact(a,b)
            if not equal:errors.append(cid+'.'+key+': expected '+repr(b)+', got '+repr(a)[:120])
    return errors

def semantic_results(review_dir,semantic_ids,artifact_hashes):
    result={cid:{'status':'unknown','reason':'Two independent masked reviews have not been supplied'} for cid in semantic_ids}
    if review_dir is None:return result
    reviews=[]
    try:
        for name in ('review_1.json','review_2.json'):
            reviews.append(parse_json(safe_read(review_dir,name,MAX_REVIEW)))
        if reviews[0].get('reviewer_id')==reviews[1].get('reviewer_id') or not all(r.get('reviewer_id') for r in reviews):raise ValueError('Two distinct reviewer IDs required')
        if not all(r.get('condition_masked') is True and r.get('independent') is True for r in reviews):raise ValueError('Independent condition-masked reviews required')
        if not all(r.get('case_id')==CASE_ID for r in reviews):raise ValueError('Wrong review case')
        if not artifact_hashes or not all(r.get('artifact_sha256')==artifact_hashes for r in reviews):raise ValueError('Review is not bound to these exact output artifacts')
        for cid in semantic_ids:
            votes=[r.get('checks',{}).get(cid,{}) for r in reviews]
            if not all(v.get('status') in ('pass','fail') and isinstance(v.get('rationale'),str) and v['rationale'].strip() for v in votes):continue
            if votes[0]['status']==votes[1]['status']:
                result[cid]={'status':votes[0]['status'],'reason':'Agreement of two independent masked reviews','reviews':votes}
            else:result[cid]={'status':'unknown','reason':'Reviewers disagree; adjudication required','reviews':votes}
    except Exception as ex:
        for cid in semantic_ids:result[cid]={'status':'unknown','reason':'Invalid review packet: '+str(ex)[:250]}
    return result

def grade(submission_dir,review_dir=None):
    private=Path(__file__).resolve().parent
    expected=parse_json((private/'expected.json').read_text(encoding='utf-8'))
    rubric=parse_json((private/'rubric.json').read_text(encoding='utf-8'))
    checks={c['id']:{'status':'unknown','reason':'Not evaluated'} for c in rubric['checks']}
    objective=[c['id'] for c in rubric['checks'] if c['mode']=='objective']
    semantic=[c['id'] for c in rubric['checks'] if c['mode']=='semantic']
    errors=[];artifact_hashes={}
    try:
        raw_json=safe_read(submission_dir,JSON_FILE,MAX_JSON)
        prose=safe_read(submission_dir,TEXT_FILE,MAX_TEXT)
        artifact_hashes={JSON_FILE:hashlib.sha256(raw_json.encode('utf-8')).hexdigest(),TEXT_FILE:hashlib.sha256(prose.encode('utf-8')).hexdigest()}
        data=parse_json(raw_json)
        if not isinstance(data,dict):raise ValueError('Top-level JSON must be an object')
        if not prose.strip():raise ValueError('Required handoff text is empty')
        checks.update(evaluate(data,expected,prose))
    except Exception as ex:
        errors.append(type(ex).__name__+': '+str(ex)[:500])
        for cid in objective:checks[cid]={'status':'fail','reason':'Unreadable or unsafe required artifact: '+errors[-1]}
    checks.update(semantic_results(review_dir,semantic,artifact_hashes))
    n_pass=sum(checks[cid]['status']=='pass' for cid in objective)
    n_fail=sum(checks[cid]['status']=='fail' for cid in objective)
    return {'case_id':CASE_ID,'synthetic':True,'objective':{'passed':n_pass,'failed':n_fail,'total':len(objective)},'semantic':{'passed':sum(checks[c]['status']=='pass' for c in semantic),'failed':sum(checks[c]['status']=='fail' for c in semantic),'unknown':sum(checks[c]['status']=='unknown' for c in semantic),'total':len(semantic)},'checks':checks,'artifact_errors':errors,'artifact_sha256':artifact_hashes,'not_candidate_execution':True}

def verdict(errors):return {'status':'fail' if errors else 'pass','reason':'; '.join(errors[:15]) if errors else 'All required facts agree'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--submission-dir',required=True);ap.add_argument('--result');ap.add_argument('--semantic-review-dir');args=ap.parse_args()
    result=grade(args.submission_dir,args.semantic_review_dir)
    text=json.dumps(result,indent=2)
    if args.result:Path(args.result).write_text(text+'\n',encoding='utf-8')
    else:print(text)
    return 0

CASE_ID='R2'
JSON_FILE='action_register.json'
TEXT_FILE='handoff.txt'
ALLOWED_FILES=(JSON_FILE,TEXT_FILE)

def evaluate(data,expected,prose):
    out={};rows=data.get('actions',[])
    if not isinstance(rows,list):raise ValueError('actions must be a list')
    ids=[x.get('action_id') for x in rows if isinstance(x,dict)]
    exp={x['action_id']:x for x in expected['actions']}
    actual={x['action_id']:x for x in rows if isinstance(x,dict) and isinstance(x.get('action_id'),str)}
    out['R2-01']=verdict([] if len(rows)==len(ids)==34 and len(set(ids))==34 and set(ids)==set(exp) else ['Expected all and only 34 unique canonical action IDs'])
    special=['A03','A09','A10','A11','A20','A21','A27','A33']
    out['R2-02']=verdict(compare_fields(actual,exp,[x for x in exp if x not in special],['status']))
    out['R2-03']=verdict(compare_fields(actual,exp,special,['status']))
    transfers=['A02','A06','A10','A23','A31']
    out['R2-04']=verdict(compare_fields(actual,exp,transfers,['owner']))
    out['R2-05']=verdict(compare_fields(actual,exp,[x for x in exp if x not in transfers],['owner']))
    changed=['A02','A06','A08','A10','A13','A14','A20','A23','A25','A30','A31','A33']
    out['R2-06']=verdict(compare_fields(actual,exp,changed,['due_date']))
    out['R2-07']=verdict(compare_fields(actual,exp,[x for x in exp if x not in changed],['due_date']))
    out['R2-08']=verdict([] if exact(data.get('aliases'),expected['aliases']) else ['Explicit duplicate aliases do not match'])
    out['R2-09']=verdict(compare_fields(actual,exp,list(exp),['dependencies']))
    err=compare_fields(actual,exp,list(exp),['overdue'])
    tot=data.get('totals',{})
    if not isinstance(tot,dict) or any(not exact(tot.get(k),v) for k,v in expected['totals'].items()):err.append('Incorrect by-status, active or overdue totals')
    out['R2-10']=verdict(err)
    valid={'B00',*('M%d'%i for i in range(1,6)),*('F%d'%i for i in range(1,10))}
    # Essential citation sets correspond to supplied final decisions; B00 supplements unchanged facts.
    essential={'A01':{'M2'},'A02':{'M4'},'A03':{'M5'},'A04':{'M4'},'A05':{'M2'},'A06':{'M1'},'A07':{'M3'},'A08':{'M5'},'A09':{'M4','F6'},'A10':{'F6'},'A11':{'M3','F7'},'A12':{'M3','F7'},'A13':{'M5'},'A14':{'M5'},'A15':{'M5'},'A16':{'M5'},'A17':{'M4'},'A18':{'M4','F7'},'A19':{'M3'},'A20':{'M3'},'A21':{'F5','M5'},'A22':{'M2'},'A23':{'F2'},'A24':{'M4'},'A25':{'M4'},'A26':{'M3'},'A27':{'M5'},'A28':{'M4'},'A29':{'M4'},'A30':{'M2'},'A31':{'F4'},'A32':{'F3'},'A33':{'M4','F7'},'A34':{'M4','F7'}}
    err=[]
    for cid,needed in essential.items():
        x=actual.get(cid,{})
        if not isinstance(x.get('title'),str) or not x['title'].strip():err.append(cid+': missing meaningful title')
        if 'blocker' not in x or (x['blocker'] is not None and not isinstance(x['blocker'],str)):err.append(cid+': blocker field invalid')
        if x.get('status') in ('open','blocked','unresolved'):
            if not isinstance(x.get('next_step'),str) or not x['next_step'].strip():err.append(cid+': active action lacks next step')
        elif x.get('next_step') is not None:err.append(cid+': closed action should have null next_step')
        if x.get('status') in ('blocked','unresolved') and (not isinstance(x.get('blocker'),str) or not x['blocker'].strip()):err.append(cid+': blocked/unresolved action lacks obstacle description')
        evid=x.get('evidence_ids')
        if not isinstance(evid,list) or not all(isinstance(z,str) for z in evid):err.append(cid+': invalid evidence list');continue
        if not set(evid)<=valid:err.append(cid+': unknown evidence ID')
        if not needed&set(evid):err.append(cid+': no supporting current-state decision source')
        if set(evid)&{'F8','F9'}:err.append(cid+': cites post-cutoff state as evidence')
    out['R2-11']=verdict(err)
    return out

if __name__=='__main__':raise SystemExit(main())
