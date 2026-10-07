"""Inspect replayed observations without running candidate code."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import json
from replay import replay
from schema import validate
from bounded_json import read_artifact, ArtifactError

if __name__ == '__main__':
    try:
        scenarios, _ = validate(read_artifact(Path(sys.argv[1])))
        print(json.dumps({scenario['id']: replay(scenario['actions']) for scenario in scenarios}, indent=2))
    except ArtifactError as error:
        print(json.dumps({'error': str(error)})); sys.exit(2)
