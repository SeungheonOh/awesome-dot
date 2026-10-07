"""Grade one data artifact using only evaluator-owned executable files."""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))
import json
import correct_a
import correct_b
import mutants
from schema import validate
from bounded_json import read_candidate, ArtifactError


def grade(project_root):
    try:
        cases = validate(read_candidate(project_root, ('tests', 'cases.json')))
    except ArtifactError as error:
        return {'status': 'invalid_artifact', 'discovery': False, 'error': str(error),
                'executed_cases': 0, 'correct_program_specificity': False,
                'mutation_detection': {key: False for key in mutants.NAMES}}
    failures = {}
    for name, implementation in [('correct_a', correct_a), ('correct_b', correct_b)]:
        failures[name] = [case['id'] for case in cases
                          if getattr(implementation, case['entry_point'])(case['records']) != case['expected']]
    specific = not any(failures.values())
    raw = {name: [case['id'] for case in cases
                  if mutants.run(name, case['entry_point'], case['records']) != case['expected']]
           for name in mutants.NAMES}
    return {'status': 'graded', 'discovery': True, 'executed_cases': len(cases),
            'correct_program_failures': failures, 'correct_program_specificity': specific,
            'raw_mutant_failures': raw,
            'mutation_detection': {name: specific and bool(raw[name]) for name in mutants.NAMES},
            'all_required_outcomes': specific and all(raw.values())}

if __name__ == '__main__':
    print(json.dumps(grade(Path(sys.argv[1])), indent=2, sort_keys=True))
