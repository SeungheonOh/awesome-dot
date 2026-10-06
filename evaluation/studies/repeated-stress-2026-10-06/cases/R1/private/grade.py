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

CASE_ID='R1'
JSON_FILE='reconciliation.json'
TEXT_FILE='review_notes.txt'
ALLOWED_FILES=(JSON_FILE,TEXT_FILE)
MONEY=('approved_usd_cents','reimbursement_usd_cents','excluded_usd_cents','held_usd_cents','credit_usd_cents')

def evaluate(data,expected,prose):
    out={}
    rows=data.get('claims',[])
    if not isinstance(rows,list):raise ValueError('claims must be a list')
    ids=[x.get('claim_id') for x in rows if isinstance(x,dict)]
    exp={x['claim_id']:x for x in expected['claims']}
    actual={x['claim_id']:x for x in rows if isinstance(x,dict) and isinstance(x.get('claim_id'),str)}
    out['R1-01']=verdict([] if len(rows)==len(ids)==30 and len(set(ids))==30 and set(ids)==set(exp) else ['Expected all and only 30 unique canonical claim IDs'])
    err=[]
    for cid,x in actual.items():
        for key in MONEY:
            value=x.get(key,'MISSING')
            if value is None and cid=='C026' and key in ('approved_usd_cents','excluded_usd_cents','held_usd_cents'):continue
            if type(value) is not int or value<0:err.append(cid+'.'+key+' must be nonnegative integer cents')
        if 'duplicate_of' not in x or (x['duplicate_of'] is not None and not isinstance(x['duplicate_of'],str)):err.append(cid+': invalid duplicate_of')
        if not isinstance(x.get('note'),str) or not x['note'].strip():err.append(cid+': missing explanation')
        if not isinstance(x.get('evidence_ids'),list) or not all(isinstance(z,str) for z in x['evidence_ids']):err.append(cid+': evidence_ids must be strings')
    if not isinstance(data.get('totals'),dict):err.append('Missing totals object')
    out['R1-02']=verdict(err)
    out['R1-03']=verdict(compare_fields(actual,exp,list(exp),['disposition']))
    groups={'04':['C003','C004','C008','C011','C012','C015','C016'],'05':['C001','C002','C006','C009','C013','C014','C029'],'06':['C005','C010','C021','C027'],'07':['C022','C023','C024'],'08':['C007','C019','C020','C025','C030'],'09':['C017','C018','C026','C028']}
    for n,cids in groups.items():out['R1-'+n]=verdict(compare_fields(actual,exp,cids,list(MONEY)+['duplicate_of']))
    err=[];totals=data.get('totals',{})
    for k,v in expected['totals'].items():
        got=totals.get(k) if isinstance(totals,dict) else None
        if k=='unvalued_holds':
            equal=isinstance(got,list) and len(got)==1 and isinstance(got[0],dict) and got[0].get('claim_id')=='C026' and got[0].get('currency')=='EUR' and isinstance(got[0].get('original_amount'),str)
            try:equal=equal and Decimal(got[0]['original_amount'])==Decimal('24.00')
            except (InvalidOperation,KeyError,TypeError):equal=False
        else:equal=exact(got,v)
        if not equal:err.append('Incorrect total '+k)
    out['R1-10']=verdict(err)
    valid={'P1','P2','T1',*('E%02d'%i for i in range(1,7))}
    for row in expected['claims']:valid.update(row['evidence_ids'])
    valid.add('S229')
    # Any sufficient source set is accepted; redundant citation styles are not required.
    essential={'C001':[{'R001'},{'S001'}],'C002':[{'P1','R002'},{'P1','S002'}],'C003':[{'P1','R003'}],'C004':[{'P1','R004'}],'C005':[{'P1','R005'}],'C006':[{'R006'},{'S006'}],'C007':[{'R001'},{'E05'}],'C008':[{'P2','R008'},{'P2','S008'}],'C009':[{'P2','R009'},{'P2','S009'}],'C010':[{'R010','E01'}],'C011':[{'P2','R011'},{'P2','S011'}],'C012':[{'P2','R012'}],'C013':[{'R013','E02'},{'S013','E02'}],'C014':[{'R014','S014'}],'C015':[{'R015','S015'}],'C016':[{'S016'}],'C017':[{'E05'},{'C017','P1'},{'C017','P2'}],'C018':[{'R018'},{'E05'}],'C019':[{'R019','E03'},{'S019','E03'}],'C020':[{'S020','E03'}],'C021':[{'R021','E01'}],'C022':[{'R022','S122'},{'S022','S122'}],'C023':[{'R023','S123'},{'S023','S123'}],'C024':[{'R024','S124','E04'},{'S024','S124','E04'}],'C025':[{'R025'},{'C025'},{'T1'}],'C026':[{'R026'},{'E05'}],'C027':[{'R027'}],'C028':[{'R028','S028'},{'E05'}],'C029':[{'R029','S029'}],'C030':[{'S030'},{'C030'}]}
    valid.update(exp);valid.add('EST-27')
    err=[]
    for cid,alternatives in essential.items():
        ids=actual.get(cid,{}).get('evidence_ids',[])
        if not isinstance(ids,list) or not all(isinstance(z,str) for z in ids):err.append(cid+': invalid evidence list');continue
        cited=set(ids)
        if not cited<=valid:err.append(cid+': unknown source IDs')
        if not any(needed<=cited for needed in alternatives):err.append(cid+': no sufficient supporting evidence set')
    out['R1-11']=verdict(err)
    return out

if __name__=='__main__':raise SystemExit(main())
