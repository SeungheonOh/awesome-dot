"""Public discovery command: python -I -B run_tests.py (stdlib only)."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import json
import exporter
from schema import validate
from bounded_json import read_candidate, ArtifactError


def main():
    try:
        cases = validate(read_candidate(Path(__file__).resolve().parent, ('tests','cases.json')))
    except ArtifactError as error:
        print(json.dumps({'discovered': False, 'error': str(error)}))
        return 2
    failed = [case['id'] for case in cases
              if getattr(exporter, case['entry_point'])(case['records']) != case['expected']]
    print(json.dumps({'discovered': True, 'executed': len(cases), 'failed': failed}))
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())
