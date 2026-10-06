"""Small public smoke test. Read module source before running."""
import importlib.util
from pathlib import Path
import tempfile
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('merge_workspace',ROOT/'output/merge_workspace.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
(ROOT/'tmp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='smoke-',dir=ROOT/'tmp') as path:
 w=module.MergeWorkspace(path);w.add('release','alpha\nbeta\ngamma\n')
 w.edit('release','ALPHA\nbeta\ngamma\n')
 state=w.receive('release','alpha\nbeta\nGAMMA\n')
 assert state['text']=='ALPHA\nbeta\nGAMMA\n' and state['dirty']
 w.save();v=module.MergeWorkspace(path)
 assert v.get('release')==state,'save/reload lost the merge base or unfinished work'
print('smoke test passed')
