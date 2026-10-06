"""Static integrity report and explicit-approval behavioral runner.
This gate is not an OS/process sandbox. Human review supplies the execution
safety boundary; resource limits only bound a reviewed consumer's run.
"""
import argparse,ast,hashlib,json,os,pathlib,stat,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent
LIMITS={'wall_seconds':30,'cpu_seconds':20,'address_space_bytes':536870912,'file_bytes':8388608,'open_files':64,'source_bytes':131072,'captured_log_bytes':65536}

def read(path,limit):
 p=pathlib.Path(os.path.abspath(path));fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY)
 try:
  for part in p.parts[1:-1]:
   nxt=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  f=os.open(p.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
  try:
   s=os.fstat(f)
   if not stat.S_ISREG(s.st_mode) or s.st_size>limit:raise ValueError('not a bounded regular file: '+str(p))
   chunks=[];remaining=limit+1
   while remaining:
    b=os.read(f,min(65536,remaining))
    if not b:break
    chunks.append(b);remaining-=len(b)
   raw=b''.join(chunks)
   if len(raw)>limit:raise ValueError('file exceeded bound')
   return raw
  finally:os.close(f)
 finally:os.close(fd)

def digest(raw):return hashlib.sha256(raw).hexdigest()
def dump(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def prepare(source_path,work_root):
 raw=read(source_path,LIMITS['source_bytes']);harness=read(HERE/'probe.py',131072);runner=read(__file__,131072)
 root=pathlib.Path(os.path.abspath(work_root))
 if root.parent.resolve(strict=True)!=root.parent:raise ValueError('work-root parent must not contain symlinks')
 root.mkdir(mode=0o700,exist_ok=False);reviewed=root/'reviewed';reviewed.mkdir();(root/'tmp').mkdir()
 (reviewed/'source.py').write_bytes(raw);(reviewed/'probe.py').write_bytes(harness)
 report={'case':'R4','phase':'static_only','source_sha256':digest(raw),'source_bytes':len(raw),'behavioral_status':'unknown','imports':[],'review_flags':[],'protected_inputs':[]}
 try:
  tree=ast.parse(raw,filename='source.py')
  report['syntax']='valid'
  for node in ast.walk(tree):
   if isinstance(node,ast.Import):report['imports'] += [x.name for x in node.names]
   elif isinstance(node,ast.ImportFrom):report['imports'].append('.'*node.level+(node.module or ''))
   elif isinstance(node,ast.Call):
    name=node.func.id if isinstance(node.func,ast.Name) else node.func.attr if isinstance(node.func,ast.Attribute) else '<dynamic>'
    if name in {'eval','exec','compile','__import__','system','popen','Popen','run','connect','urlopen','CDLL','fork','spawn'}:report['review_flags'].append({'line':node.lineno,'call':name})
  report['top_level_node_types']=[type(x).__name__ for x in tree.body]
 except SyntaxError as e:report['syntax']='invalid';report['syntax_error']=str(e)
 manifest_path=HERE/'manifest.json'
 if manifest_path.exists():
  manifest=json.loads(read(manifest_path,200000));packet=pathlib.Path(source_path).absolute().parent.parent
  for relative,expected in manifest.get('protected_sha256',{}).items():
   try:actual=digest(read(packet/relative,8_000_000));status='match' if actual==expected else 'changed'
   except Exception as e:actual=None;status='unreadable: '+str(e)
   report['protected_inputs'].append({'path':relative,'status':status,'sha256':actual})
 plan={'case':'R4','source_original':str(pathlib.Path(source_path).absolute()),'work_root':str(root),'source_sha256':digest(raw),'harness_sha256':digest(harness),'runner_sha256':digest(runner),'limits':LIMITS,'argv':[sys.executable,'-I','-B',str(reviewed/'probe.py'),'--module',str(reviewed/'source.py'),'--root',str(root/'tmp'),'--result',str(root/'probe_result.json')],'effects':['Import exactly reviewed/source.py and reviewed/probe.py after approval','Create/read/replace/remove fixtures only beneath this evaluator-owned work_root/tmp','Write probe_result.json, bounded stdout.log/stderr.log and final report within work_root','No network, credentials, external reads/writes, or candidate subprocesses are permitted','This is reviewed owned-copy execution, not OS/process isolation'],'approval_required':'Root reviewer must inspect exact copied source, copied harness, this runner, and static report; approve this exact plan hash before run. A static report alone is not approval.'}
 dump(root/'static_report.json',report);dump(root/'plan.json',plan)
 print(json.dumps({'phase':'static_only','work_root':str(root),'static_report':str(root/'static_report.json'),'plan':str(root/'plan.json'),'plan_sha256':digest(read(root/'plan.json',200000)),'behavioral_status':'unknown'},indent=2))

def apply_limits():
 import resource
 resource.setrlimit(resource.RLIMIT_CPU,(LIMITS['cpu_seconds'],LIMITS['cpu_seconds']))
 resource.setrlimit(resource.RLIMIT_AS,(LIMITS['address_space_bytes'],LIMITS['address_space_bytes']))
 resource.setrlimit(resource.RLIMIT_FSIZE,(LIMITS['file_bytes'],LIMITS['file_bytes']))
 resource.setrlimit(resource.RLIMIT_NOFILE,(LIMITS['open_files'],LIMITS['open_files']))
 resource.setrlimit(resource.RLIMIT_CORE,(0,0))

def execute(plan_path,approval_path):
 plan_raw=read(plan_path,200000);plan=json.loads(plan_raw);approval=json.loads(read(approval_path,65536))
 if approval.get('approved') is not True or approval.get('approved_by') not in {'root','/root'} or approval.get('plan_sha256')!=digest(plan_raw):raise ValueError('exact root approval of plan hash is required')
 root=pathlib.Path(plan['work_root'])
 if root.resolve(strict=True)!=root:raise ValueError('work root must have no symlinks')
 if pathlib.Path(plan_path).absolute()!=root/'plan.json':raise ValueError('plan must be stored in its work root')
 source=read(root/'reviewed/source.py',LIMITS['source_bytes']);harness=read(root/'reviewed/probe.py',131072)
 if digest(source)!=plan['source_sha256'] or digest(harness)!=plan['harness_sha256'] or digest(read(__file__,131072))!=plan['runner_sha256']:raise ValueError('reviewed artifact changed after plan creation')
 expected_argv=[sys.executable,'-I','-B',str(root/'reviewed/probe.py'),'--module',str(root/'reviewed/source.py'),'--root',str(root/'tmp'),'--result',str(root/'probe_result.json')]
 if plan['argv']!=expected_argv or plan['limits']!=LIMITS:raise ValueError('plan command or bounds changed')
 if (root/'probe_result.json').exists():raise ValueError('work root already has a behavioral result; prepare a fresh plan')
 env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'LANG':'C.UTF-8','PYTHONHASHSEED':'0','HOME':str(root),'TMPDIR':str(root/'tmp')}
 status='finished';returncode=None
 with open(root/'stdout.log','xb') as out,open(root/'stderr.log','xb') as err:
  try:
   process=subprocess.run(expected_argv,cwd=root,env=env,stdout=out,stderr=err,timeout=LIMITS['wall_seconds'],preexec_fn=apply_limits,check=False);returncode=process.returncode
  except subprocess.TimeoutExpired:status='timeout'
 result={'case':'R4','phase':'behavioral','execution_status':status,'returncode':returncode,'source_sha256':plan['source_sha256'],'plan_sha256':digest(plan_raw)}
 if status=='finished' and returncode==0:
  try:result['behavior']=json.loads(read(root/'probe_result.json',200000))
  except Exception as e:result['behavior']={'status':'ungraded','error':str(e)}
 else:result['behavior']={'status':'ungraded','reason':'process did not complete; all behavioral outcomes remain unknown'}
 for name in ['stdout.log','stderr.log']:
  # The process file-size limit bounds complete logs; display just a small excerpt.
  result[name]=read(root/name,LIMITS['file_bytes'])[:LIMITS['captured_log_bytes']].decode('utf8',errors='replace')
 dump(root/'behavioral_report.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
 s=sub.add_parser('static');s.add_argument('--submission',required=True);s.add_argument('--work-root',required=True)
 r=sub.add_parser('run');r.add_argument('--plan',required=True);r.add_argument('--approval-file',required=True)
 args=p.parse_args()
 if args.command=='static':prepare(args.submission,args.work_root)
 else:execute(args.plan,args.approval_file)
