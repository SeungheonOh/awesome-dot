"""Behavioral harness. Execute only as an approved, reviewed owned copy.
Expected results are literal texts or independently constructed edits; this file
never imports the reference implementation or uses its merge algorithm.
"""
import argparse,copy,importlib.util,json,os,pathlib,tempfile,traceback,stat,signal
from unittest.mock import patch
from contextlib import ExitStack

class ProbeUnknown(Exception):
 pass
CHECKS=['views_and_edits','fast_forward_base','disjoint_modifications','insert_delete_endings','identical_adjacent_hunks','conflict_retention','pending_blocks_mutation','resolution_choices','rename_remove','save_reload','failed_save_atomicity','corrupt_snapshots','bounds_nofollow']
BASE='one\ntwo\nthree\nfour\nfive\n'

def read_owned(path,limit=8_388_608):
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 try:
  st=os.fstat(fd)
  if not stat.S_ISREG(st.st_mode) or st.st_size>limit:raise ValueError('not a bounded regular fixture')
  chunks=[];remaining=limit+1
  while remaining:
   chunk=os.read(fd,min(65536,remaining))
   if not chunk:break
   chunks.append(chunk);remaining-=len(chunk)
  raw=b''.join(chunks)
  if len(raw)>limit:raise ValueError('fixture too large')
  return raw
 finally:os.close(fd)

def expect_raises(cls,func):
 try:func()
 except cls:return
 except Exception as e:raise AssertionError('expected '+str(cls)+', got '+type(e).__name__) from e
 raise AssertionError('expected '+str(cls))

def state(w,n='doc'):return w.get(n)

def conflict(w,n='doc'):
 w.add(n,BASE);w.edit(n,BASE.replace('two\n','LOCAL\n'));s=w.receive(n,BASE.replace('two\n','REMOTE\n'))
 assert s['conflict']=={'base':BASE,'local':BASE.replace('two\n','LOCAL\n'),'incoming':BASE.replace('two\n','REMOTE\n')}
 return s

def views_and_edits(m,p):
 w=m.MergeWorkspace(p);assert w.names()==[]
 assert w.add('doc',BASE)=={'base':BASE,'text':BASE,'dirty':False,'conflict':None}
 assert w.edit('doc','draft')['dirty'];assert not w.edit('doc',BASE)['dirty']
 view=w.get('doc');view['text']='outside';assert w.get('doc')['text']==BASE
 conflict(w,'review');view=w.get('review');view['conflict']['incoming']='outside'
 assert w.get('review')['conflict']['incoming']==BASE.replace('two\n','REMOTE\n')

def fast_forward_base(m,p):
 w=m.MergeWorkspace(p);w.add('doc',BASE)
 incoming=BASE+'six\n';s=w.receive('doc',incoming)
 assert s=={'base':incoming,'text':incoming,'dirty':False,'conflict':None}
 local=incoming.replace('one\n','ONE\n');w.edit('doc',local)
 assert w.receive('doc',incoming)=={'base':incoming,'text':local,'dirty':True,'conflict':None}
 s=w.receive('doc',local);assert s['base']==local and s['text']==local and not s['dirty']

def disjoint_modifications(m,p):
 w=m.MergeWorkspace(p)
 for i in range(6):
  for j in range(6):
   if i==j:continue
   name='d'+str(i)+str(j);base=[f'line-{k}\n' for k in range(6)];local=base[:];remote=base[:];expected=base[:]
   local[i]=f'local-{i}\n';remote[j]=f'remote-{j}\n';expected[i]=local[i];expected[j]=remote[j]
   w.add(name,''.join(base));w.edit(name,''.join(local));s=w.receive(name,''.join(remote))
   assert s=={'base':''.join(remote),'text':''.join(expected),'dirty':True,'conflict':None},(i,j,s)

def insert_delete_endings(m,p):
 w=m.MergeWorkspace(p)
 cases=[
 ('a\nb\nc\nd\ne\n','a\nLOCAL\nb\nc\nd\ne\n','a\nb\nc\nd\nREMOTE\n','a\nLOCAL\nb\nc\nd\nREMOTE\n'),
 ('a\nb\nc\nd\ne\n','a\nc\nd\ne\n','a\nb\nc\nd\nREMOTE\n','a\nc\nd\nREMOTE\n'),
 ('a\r\nb\r\nc\r\nd','A\r\nb\r\nc\r\nd','a\r\nb\r\nc\r\nD','A\r\nb\r\nc\r\nD'),
 ('a\nb\nc\nd\n','A\nb\nc\nd\n','a\nb\nc\nd\nend','A\nb\nc\nd\nend')]
 for i,(base,local,remote,expected) in enumerate(cases):
  n='d'+str(i);w.add(n,base);w.edit(n,local);s=w.receive(n,remote)
  assert s['conflict'] is None and s['text']==expected and s['base']==remote,(i,s)

def identical_adjacent_hunks(m,p):
 w=m.MergeWorkspace(p)
 w.add('doc',BASE);local=BASE.replace('two\n','TWO\n').replace('five\n','FIVE\n');remote=BASE.replace('two\n','TWO\n').replace('four\n','FOUR\n')
 w.edit('doc',local);s=w.receive('doc',remote)
 assert s['text']=='one\nTWO\nthree\nFOUR\nFIVE\n' and s['conflict'] is None
 w.add('adjacent',BASE);w.edit('adjacent',BASE.replace('two\n','TWO\n'));s=w.receive('adjacent',BASE.replace('three\n','THREE\n'))
 assert s['text']=='one\nTWO\nTHREE\nfour\nfive\n' and s['conflict'] is None
 w.add('insert',BASE);w.edit('insert','new\n'+BASE);s=w.receive('insert','new\n'+BASE.replace('five\n','FIVE\n'))
 assert s['text']=='new\n'+BASE.replace('five\n','FIVE\n') and not s['dirty']

def conflict_retention(m,p):
 w=m.MergeWorkspace(p);before=conflict(w);assert w.get('doc')==before
 # Insertion at a replacement boundary is conservatively conflicting.
 w.add('boundary',BASE);local=BASE.replace('two\n','insert\ntwo\n');incoming=BASE.replace('two\n','TWO\n')
 w.edit('boundary',local);s=w.receive('boundary',incoming)
 assert s['base']==BASE and s['text']==local and s['conflict']=={'base':BASE,'local':local,'incoming':incoming}
 # Two distinct insertions at one position must also retain all three versions.
 w.add('inserts',BASE);local='left\n'+BASE;incoming='right\n'+BASE;w.edit('inserts',local);s=w.receive('inserts',incoming)
 assert s['conflict']=={'base':BASE,'local':local,'incoming':incoming}

def pending_blocks_mutation(m,p):
 w=m.MergeWorkspace(p);before=conflict(w)
 for call in [lambda:w.edit('doc','replacement'),lambda:w.receive('doc','another'),lambda:w.receive('doc',before['conflict']['incoming'])]:
  expect_raises(m.ConflictPending,call);assert w.get('doc')==before

def resolution_choices(m,p):
 w=m.MergeWorkspace(p)
 for choice in ['local','incoming','manual']:
  old=conflict(w,choice);remote=old['conflict']['incoming'];manual='reviewed\nfinal\n'
  s=w.resolve(choice,choice,manual if choice=='manual' else None)
  chosen=old['conflict'][choice] if choice!='manual' else manual
  assert s=={'base':remote,'text':chosen,'dirty':chosen!=remote,'conflict':None}
 before=conflict(w,'invalid')
 for call in [lambda:w.resolve('invalid','bogus'),lambda:w.resolve('invalid','manual'),lambda:w.resolve('invalid','local','extra')]:
  expect_raises(ValueError,call);assert w.get('invalid')==before
 expect_raises(ValueError,lambda:w.resolve('incoming','incoming'))

def rename_remove(m,p):
 w=m.MergeWorkspace(p);before=conflict(w);w.add('other','clean')
 assert w.rename('doc','renamed')==before and w.names()==['other','renamed']
 assert w.rename('renamed','renamed')==before
 expect_raises(ValueError,lambda:w.rename('renamed','other'));assert w.get('renamed')==before
 w.remove('other');assert w.names()==['renamed'];expect_raises(KeyError,lambda:w.get('other'))
 w.save();v=m.MergeWorkspace(p);assert v.names()==['renamed'] and v.get('renamed')==before

def save_reload(m,p):
 w=m.MergeWorkspace(p);w.add('clean','ready');w.add('draft',BASE);w.edit('draft',BASE.replace('one\n','ONE\n'));conflict(w,'review');w.add('deleted','bye');w.save();w.remove('deleted');w.rename('draft','renamed')
 expected={n:w.get(n) for n in w.names()};w.save();assert {n:w.get(n) for n in w.names()}==expected
 v=m.MergeWorkspace(p);assert {n:v.get(n) for n in v.names()}==expected
 s=v.receive('renamed',BASE.replace('five\n','FIVE\n'))
 assert s['text']=='ONE\ntwo\nthree\nfour\nFIVE\n' and s['conflict'] is None
 v.resolve('review','local');v.save();q=m.MergeWorkspace(p);assert q.get('review')==v.get('review')


def failed_save_atomicity(m,p):
 w=m.MergeWorkspace(p);w.add('doc',BASE);w.save();target=p/'workspace.json';old=read_owned(target)
 w.edit('doc','unfinished\n');before=w.get('doc')
 # Observe both standard atomic-renaming primitives and directly imported aliases.
 originals=(os.replace,os.rename);aliases=[name for name,value in vars(m).items() if any(value is original for original in originals)]
 observed=[]
 def fail_replacement(*args,**kwargs):
  observed.append(True);raise OSError('simulated replacement failure')
 with ExitStack() as stack:
  stack.enter_context(patch('os.replace',side_effect=fail_replacement));stack.enter_context(patch('os.rename',side_effect=fail_replacement))
  for name in aliases:stack.enter_context(patch.object(m,name,side_effect=fail_replacement))
  try:w.save()
  except OSError:pass
 if not observed:raise ProbeUnknown('save did not use an observed standard replacement primitive; atomic failure behavior needs separate review')
 assert read_owned(target)==old,'failed save changed durable checkpoint'
 assert w.get('doc')==before,'failed save changed live state'
 assert sorted(x.name for x in p.iterdir())==['workspace.json'],'failed save leaked temporary files'
 assert m.MergeWorkspace(p).get('doc')['text']==BASE
 w.save();assert m.MergeWorkspace(p).get('doc')==before


def corrupt_snapshots(m,p):
 valid={'schema_version':1,'documents':[{'name':'doc','base':'a','text':'b','conflict':None}]}
 bad=[b'{broken',json.dumps({'schema_version':2,'documents':[]}).encode(),json.dumps({'schema_version':True,'documents':[]}).encode()]
 variations=[]
 for change in [lambda d:d['documents'].append(copy.deepcopy(d['documents'][0])),lambda d:d['documents'][0].update(name='../escape'),lambda d:d['documents'][0].update(text=7),lambda d:d['documents'][0].update(conflict={'base':'wrong','local':'b','incoming':'c'}),lambda d:d['documents'][0].update(extra='no'),lambda d:d.update(extra=True),lambda d:d.update(documents={})]:
  v=copy.deepcopy(valid);change(v);variations.append(v)
 bad += [json.dumps(v).encode() for v in variations]
 for raw in bad:
  (p/'workspace.json').write_bytes(raw);expect_raises(ValueError,lambda:m.MergeWorkspace(p));assert read_owned(p/'workspace.json')==raw


def bounds_nofollow(m,p):
 w=m.MergeWorkspace(p);w.add('doc','x');before=w.get('doc')
 # Two individually valid versions can combine beyond the document text cap.
 large=m.MergeWorkspace(p/'large');base='a\nb\nc\nd\n';large.add('doc',base)
 large.edit('doc','L'*60000+'\nb\nc\nd\n');prior=large.get('doc')
 expect_raises(ValueError,lambda:large.receive('doc','a\nb\nc\n'+'R'*60000+'\n'));assert large.get('doc')==prior
 for call in [lambda:w.add('../bad','x'),lambda:w.add('doc','duplicate'),lambda:w.edit('doc',5),lambda:w.edit('doc','x'*100001),lambda:w.rename('doc','../bad')]:
  expect_raises(ValueError,call);assert w.get('doc')==before
 for i in range(99):w.add('d'+str(i),'x')
 expect_raises(ValueError,lambda:w.add('extra','x'))
 # Size checks must happen before a live/durable change, with owned local files.
 for n in w.names():w.edit(n,'x'*30000)
 snapshot={n:w.get(n) for n in w.names()};expect_raises(ValueError,w.save);assert {n:w.get(n) for n in w.names()}==snapshot
 target=p/'workspace.json';target.write_bytes(b' '*2097153);expect_raises(ValueError,lambda:m.MergeWorkspace(p));target.unlink()
 outside=p/'owned_target';outside.write_text('preserve');target.symlink_to(outside.name)
 expect_raises((ValueError,OSError),lambda:m.MergeWorkspace(p))
 small=m.MergeWorkspace(p/'small');small.add('doc','x');(p/'small/workspace.json').symlink_to('../owned_target')
 expect_raises((ValueError,OSError),small.save);assert read_owned(outside).decode()=='preserve'
 target.unlink();target.mkdir();expect_raises((ValueError,OSError),lambda:m.MergeWorkspace(p));target.rmdir()
 # POSIX timer bounds a potentially blocking FIFO open without a child process.
 os.mkfifo(target)
 def fifo_timeout(signum,frame):raise AssertionError('nonregular FIFO read blocked')
 previous=signal.signal(signal.SIGALRM,fifo_timeout)
 signal.setitimer(signal.ITIMER_REAL,0.5)
 try:expect_raises((ValueError,OSError),lambda:m.MergeWorkspace(p))
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous);target.unlink()
 link=p/'root_link';link.symlink_to(p/'small',target_is_directory=True);expect_raises((ValueError,OSError),lambda:m.MergeWorkspace(link))


def run(module_path,root):
 spec=importlib.util.spec_from_file_location('reviewed_merge_workspace',module_path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 root.mkdir(exist_ok=True);results=[]
 for name in CHECKS:
  with tempfile.TemporaryDirectory(prefix=name+'-',dir=root) as directory:
   try:globals()[name](module,pathlib.Path(directory));result={'id':name,'status':'pass'}
   except ProbeUnknown as e:result={'id':name,'status':'unknown','reason':str(e)}
   except Exception as e:result={'id':name,'status':'fail','error':type(e).__name__+': '+str(e),'traceback':traceback.format_exc(limit=4)[-4000:]}
  results.append(result)
 return {'case':'R4','checks':results,'totals':{s:sum(x['status']==s for x in results) for s in ['pass','fail','unknown']}}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--module',required=True);parser.add_argument('--root',required=True);parser.add_argument('--result',required=True);args=parser.parse_args()
 try:result=run(pathlib.Path(args.module),pathlib.Path(args.root))
 except Exception as e:result={'case':'R4','status':'ungraded','error':type(e).__name__+': '+str(e),'checks':[{'id':c,'status':'unknown'} for c in CHECKS]}
 pathlib.Path(args.result).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result.get('totals',{'status':'ungraded'})))
