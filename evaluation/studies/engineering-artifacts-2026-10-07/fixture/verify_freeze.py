"""Verify all frozen inputs, graders and authored controls before any trial."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent


def frozen_paths():
    return sorted(path for path in ROOT.rglob('*') if path.is_file()
                  and path.relative_to(ROOT).parts[0] not in ('validation','authoring')
                  and path.name != 'freeze-manifest.json')


def main():
    manifest = json.loads((ROOT/'freeze-manifest.json').read_text())
    actual = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in frozen_paths()}
    expected = manifest['sha256']
    missing = sorted(set(expected)-set(actual))
    extra = sorted(set(actual)-set(expected))
    changed = sorted(path for path in set(actual)&set(expected) if actual[path] != expected[path])
    if missing or extra or changed:
        print(json.dumps({'verified':False,'missing':missing,'extra':extra,'changed':changed},indent=2))
        return 1
    if list(ROOT.rglob('__pycache__')) or list(ROOT.rglob('*.pyc')):
        print(json.dumps({'verified':False,'error':'bytecode cache present'}))
        return 1
    print(json.dumps({'verified':True,'frozen_files':len(actual),'candidate_trials_run':0},indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
