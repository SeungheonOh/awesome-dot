"""Independent JSON parser + patch interpreter. No diff generator and no submitted code."""
import argparse,copy,hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
import importlib.util as _io_import
_io_spec=_io_import.spec_from_file_location('f7_safe_io',HERE/'safe_io.py');safe_io=_io_import.module_from_spec(_io_spec);_io_spec.loader.exec_module(safe_io)
class Invalid(ValueError):
 def __init__(self,code,pointer='',message=''):
  self.code,self.pointer=code,pointer;super().__init__(f'{code} at {pointer or "(root)"}: {message}')
class Pairs(list):pass
class NonInteger(str):pass
def esc(s):return s.replace('~','~0').replace('/','~1')
def parse_integer(token):
 negative=token.startswith('-');digits=token[1:] if negative else token;value=0
 for i in range(0,len(digits),9):
  part=digits[i:i+9];value=value*(10**len(part))+int(part)
 return -value if negative else value
def strict_loads(text):
 def constant(s):raise Invalid('invalid_constant','',s)
 tree=json.loads(text,object_pairs_hook=Pairs,parse_float=NonInteger,parse_constant=constant,parse_int=parse_integer)
 def walk(x,path):
  if isinstance(x,NonInteger):raise Invalid('non_integer_number',path,str(x))
  if isinstance(x,Pairs):
   out={}
   for key,value in x:
    p=path+'/'+esc(key)
    if key in out:raise Invalid('duplicate_key',p,key)
    out[key]=walk(value,p)
   return out
  if isinstance(x,list):return [walk(v,path+'/'+str(i)) for i,v in enumerate(x)]
  return x
 return walk(tree,'')
def exact(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(exact(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
 return a==b
def tokens(pointer):
 if not isinstance(pointer,str) or not pointer.startswith('/'):raise Invalid('pointer','','Leading slash required')
 out=[]
 for token in pointer.split('/')[1:]:
  if re.search(r'~(?![01])',token):raise Invalid('pointer',pointer,'Malformed escape')
  out.append(token.replace('~1','/').replace('~0','~'))
 return out
def index(token,n,add=False):
 if token=='-' and add:return n
 if not re.fullmatch(r'0|[1-9][0-9]*',token):raise Invalid('array_index','',token)
 i=int(token)
 if i<0 or i>n or (i==n and not add):raise Invalid('array_index','',token)
 return i
def scope(path):
 t=tokens(path)
 return t==['catalogue','title'] or (len(t)>=3 and t[:2]==['catalogue','items'] and (bool(re.fullmatch(r'0|[1-9][0-9]*',t[2])) or t[2]=='-')) or (len(t)==2 and t[0]=='labels')
def apply(before,ops):
 if not isinstance(ops,list):raise Invalid('operation_list')
 doc=copy.deepcopy(before)
 for number,op in enumerate(ops):
  if not isinstance(op,dict) or op.get('op') not in {'add','remove','replace'}:raise Invalid('operation','',str(number))
  kind=op['op'];wanted={'op','path'} if kind=='remove' else {'op','path','value'}
  if set(op)!=wanted:raise Invalid('operation_members','',str(number))
  ts=tokens(op['path']);parent=doc
  for t in ts[:-1]:
   if isinstance(parent,dict):
    if t not in parent:raise Invalid('absent_parent',op['path'])
    parent=parent[t]
   elif isinstance(parent,list):parent=parent[index(t,len(parent))]
   else:raise Invalid('scalar_parent',op['path'])
  last=ts[-1]
  if isinstance(parent,dict):
   if kind in {'remove','replace'} and last not in parent:raise Invalid('absent_target',op['path'])
   if kind=='remove':del parent[last]
   else:parent[last]=copy.deepcopy(op['value'])
  elif isinstance(parent,list):
   i=index(last,len(parent),add=kind=='add')
   if kind=='add':parent.insert(i,copy.deepcopy(op['value']))
   elif kind=='remove':parent.pop(i)
   else:parent[i]=copy.deepcopy(op['value'])
  else:raise Invalid('scalar_parent',op['path'])
 return doc
def grade(submission_dir,runner_dir):
 submission,runner=Path(submission_dir),Path(runner_dir)
 key=strict_loads((HERE/'oracle.json').read_text())
 assertions={f'g{i}':[] for i in range(1,6)}
 def ck(g,ok,why):assertions[g].append({'passed':bool(ok),'reason':why})
 integrity=[]
 trusted_runner=json.loads((HERE/'trusted-input-manifest.json').read_text())['runner_files']
 for rel,h in trusted_runner.items():
  ok,why=safe_io.hash_check(runner,rel,h);integrity.append({'passed':ok,'reason':'Protected source bytes: '+rel+'; '+why})
 patch=None;status={};patch_raw=b''
 try:
  patch_raw=safe_io.regular_bytes(submission,'patch.json',16384)
  if len(patch_raw)>16384:raise Invalid('patch_size')
  patch=strict_loads(patch_raw.decode('utf-8'))
  ck('g1',isinstance(patch,list),'Saved patch parses with unique keys and exact integer tokens')
 except Exception as exc:ck('g1',False,'Strict saved-patch parse: '+str(exc))
 try:status=strict_loads(safe_io.regular_text(submission,'validation-status.json',65536))
 except Exception as exc:ck('g5',False,'Strict validation-status parse: '+str(exc))
 if not isinstance(status,dict):status={}
 diagnostics=[]
 for filename in ['invalid-duplicate.json','invalid-number.json']:
  try:
   strict_loads(safe_io.regular_text(runner,'inputs/'+filename,1048576))
   ck('g1',False,'Invalid fixture was unexpectedly parseable: '+filename)
  except Invalid as exc:diagnostics.append({'file':'inputs/'+filename,'status':'rejected','reason_code':exc.code,'pointer':exc.pointer,'patch_emitted':False})
  except Exception as exc:ck('g1',False,'Invalid-case diagnostic failed: '+str(exc))
 invalid=status.get('invalid_cases')
 sorted_diags=sorted(diagnostics,key=lambda x:x['file'])
 try:invalid_match=isinstance(invalid,list) and exact(sorted(invalid,key=lambda x:x['file']),sorted_diags)
 except Exception:invalid_match=False
 ck('g1',invalid_match and len(diagnostics)==2,'Both invalid documents are rejected with source-derived reason codes and pointers')
 parsed_sources=True
 try:
  before=strict_loads(safe_io.regular_text(runner,'inputs/before.json',1048576));after=strict_loads(safe_io.regular_text(runner,'inputs/after.json',1048576))
 except Exception as exc:before=after=None;parsed_sources=False;ck('g1',False,'Valid endpoints parse: '+str(exc))
 ck('g1',parsed_sources and exact(before,key['before']) and exact(after,key['after']),'Full valid endpoint values retained with arbitrary-precision integers and strict types')
 applied=None;valid_apply=False
 try:
  if patch is None or not parsed_sources:raise Invalid('unreadable_patch_or_endpoint')
  applied=apply(before,patch);valid_apply=True;ck('g3',True,'All operation keys, pointers, existence checks and ordered array mutations are valid')
 except Exception as exc:ck('g3',False,'Independent ordered application: '+str(exc))
 ck('g2',valid_apply and exact(applied,after),'Applying the exact saved patch yields the full after structure, type-exact including absent/null and large integers')
 ck('g4',isinstance(patch,list) and len(patch)<=32 and len(patch_raw)<=16384,'Public patch count and byte limits')
 try:in_scope=isinstance(patch,list) and all(isinstance(o,dict) and scope(o.get('path')) for o in patch)
 except Exception:in_scope=False
 ck('g4',in_scope,'Every operation, including transient edits, is inside the authorized path scope')
 try:
  raw=safe_io.regular_bytes(submission,'change-summary.txt',65536);summary=raw.decode('utf-8');lines=summary.split('\n');lines=lines[:-1] if lines and lines[-1]=='' else lines
  paths={o['path'] for o in patch}
  ck('g4',len(summary.split())<=100 and b'\r' not in raw and raw.endswith(b'\n') and not raw.endswith(b'\n\n'),'Summary length and LF contract')
  ck('g4',len(lines)>=3 and lines[0]=='Operation count: '+str(len(patch)) and lines[1]=='Changed paths:' and lines[-1]=='Invalid cases: rejected 2' and len(lines[2:-1])==len(paths) and set(lines[2:-1])==paths,'Summary discloses exactly saved operation paths/count, no values or excluded content')
 except Exception as exc:ck('g4',False,'Readable compliant summary: '+str(exc))
 desired_status=key['status']
 ck('g5',set(status)=={'valid_pair','invalid_cases'} and exact(status.get('valid_pair'),desired_status['valid_pair']),'Saved validation report schema and valid-pair identity match')
 ck('g5',invalid_match,'Invalid cases correctly rejected without emitted repair patches')
 try:only_required=safe_io.directory_names(submission)=={'patch.json','change-summary.txt','validation-status.json'}
 except Exception:only_required=False
 ck('g5',only_required,'Submission contains only the three requested artifacts, with no invalid-case repair patch')
 ck('g5',valid_apply and exact(applied,after) and isinstance(status.get('valid_pair'),dict) and status['valid_pair'].get('applied_matches_after') is True,'Saved checked patch agrees with claimed validation result')
 try:unchanged=safe_io.regular_bytes(submission,'patch.json',16384)==patch_raw
 except Exception:unchanged=False
 ck('g5',unchanged,'Patch bytes read at validation are still the saved deliverable')
 groups=[{'id':id,'passed':all(a['passed'] for a in aa),'reasons':[a['reason'] for a in aa if not a['passed']],'assertions':aa} for id,aa in assertions.items()]
 ip=all(x['passed'] for x in integrity)
 return {'case_id':'F7','integrity':{'passed':ip,'reasons':[x['reason'] for x in integrity if not x['passed']],'assertions':integrity},'groups':groups,'accepted':ip and all(g['passed'] for g in groups),'quality':sum(g['passed'] for g in groups)/5}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--submission',required=True);p.add_argument('--runner',required=True);a=p.parse_args();print(json.dumps(grade(a.submission,a.runner),indent=2))
