"""Run only the author's reference and known compact mutations, not submissions."""
import hashlib,importlib.util,json,os,pathlib,sys,tempfile
sys.dont_write_bytecode=True
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from evaluate import read
from probe import run
ref=read(HERE/'reference.py',131072).decode()
controls={
 'original_scaffold':(read(HERE.parent/'candidate/output/merge_workspace.py',131072).decode(),'save_reload'),
 'shallow_views':(ref.replace('doc=copy.deepcopy(self._docs[name]);', 'doc=dict(self._docs[name]);'),'views_and_edits'),
 'overwrite_pending':(ref.replace("        if doc['conflict'] is not None:raise ConflictPending(name)\n",''),'pending_blocks_mutation'),
 'forget_remote_base':(ref.replace('doc.update(base=incoming,text=merged)','doc.update(text=merged)'),'fast_forward_base'),
 'resolution_marks_clean':(ref.replace("doc.update(base=conflict['incoming'],text=resolved,conflict=None)","doc.update(base=resolved,text=resolved,conflict=None)"),'resolution_choices'),
 'duplicate_shared_hunks':(ref.replace('sorted(set(left+right),','sorted(left+right,'),'identical_adjacent_hunks'),
 'blocking_fifo_open':(ref.replace('|os.O_NONBLOCK',''),'bounds_nofollow'),
 'unbounded_merge':(ref.replace('            _text(merged)\n',''),'bounds_nofollow'),
 'truncate_final_newline':(ref.replace("return ''.join(out),False","return ''.join(out).rstrip('\\n'),False"),'insert_delete_endings')}
(HERE/'tmp').mkdir(exist_ok=True);results=[]
with tempfile.TemporaryDirectory(prefix='controls-',dir=HERE/'tmp') as directory:
 root=pathlib.Path(directory)
 for name,(source,check) in controls.items():
  path=root/(name+'.py');path.write_text(source);result=run(path,root/(name+'-fixtures'))
  assert next(x['status'] for x in result['checks'] if x['id']==check)=='fail',(name,result)
  results.append({'control':name,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'expected_detected_check':check,'totals':result['totals'],'validated':True})
 # Reference-specific regression: opening a FIFO must reject immediately, not block.
 spec=importlib.util.spec_from_file_location('reference_fifo',HERE/'reference.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 fifo_root=root/'fifo';fifo_root.mkdir();os.mkfifo(fifo_root/'workspace.json')
 try:m.MergeWorkspace(fifo_root)
 except (ValueError,OSError):results.append({'control':'reference_fifo_regression','validated':True,'expected':'reject nonregular snapshot without opening a blocking read'})
 else:raise AssertionError('FIFO snapshot accepted')
print(json.dumps(results,indent=2))
