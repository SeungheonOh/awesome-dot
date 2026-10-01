# Synthetic Example: An Extra Page at Exact Boundaries

This original fixture models a correctness failure only. Its inputs are invented, it needs only Python's standard library, and it does not read a real application's files or contact any service.

## Request and contract

Fictional request: “Fix the local page-count calculation and verify the boundary cases.”

The function receives non-negative integer `total` and positive integer `page_size`. It returns the smallest number of pages needed for those records. Empty input requires zero pages. Validation of values outside that domain is outside this example's contract.

## Broken implementation

```python
def page_count(total, page_size):
    return total // page_size + 1
```

## Regression checks

The same checks run against both implementations. They include empty input, a partial first page, two exact boundaries, and a partial page on either side of the second boundary.

```python
import sys

cases = [(0, 5, 0), (1, 5, 1), (5, 5, 1),
         (6, 5, 2), (10, 5, 2), (11, 5, 3)]
failed = 0
for total, page_size, expected in cases:
    actual = page_count(total, page_size)
    ok = actual == expected
    failed += not ok
    print(f'{"PASS" if ok else "FAIL"} page_count({total}, {page_size}): '
          f'expected {expected}, got {actual}')
print(f'SUMMARY: {len(cases) - failed} passed, {failed} failed')
sys.exit(1 if failed else 0)
```

## Diagnosis and minimal patch

The integer quotient already counts complete pages. Adding one unconditionally invents a page when the input is empty or exactly fills a page. This is a product correctness defect, since Python runs successfully and the assertions contradict the stated contract.

For this integer domain, rounding up the quotient uses integer arithmetic and returns zero for empty input:

```diff
 def page_count(total, page_size):
-    return total // page_size + 1
+    return (total + page_size - 1) // page_size
```

## Fixed implementation

```python
def page_count(total, page_size):
    return (total + page_size - 1) // page_size
```

## Reproduce without creating application files

From this skill's folder, run the command below. It extracts the three Python blocks above, runs the unchanged checks with each implementation in separate local Python processes, prints both exit codes, and requires the expected fail-then-pass sequence. There are no external dependencies, persistent writes, or network requests.

```sh
python3 - <<'PY'
from pathlib import Path
import re
import subprocess
import sys

blocks = re.findall(r'^```python\n(.*?)^```$',
                    Path('EXAMPLE.md').read_text(), re.M | re.S)
if len(blocks) != 3:
    raise SystemExit('Expected broken implementation, checks, and fixed implementation')
before, checks, after = blocks
for label, source, expected_code in [('BEFORE', before, 1), ('AFTER', after, 0)]:
    print(label, flush=True)
    result = subprocess.run([sys.executable, '-I', '-c', source + '\n' + checks],
                            text=True, capture_output=True, check=False)
    print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, end='', file=sys.stderr)
    print(f'EXIT: {result.returncode}', flush=True)
    if result.returncode != expected_code:
        raise SystemExit(f'{label}: unexpected exit code')
PY
```

## Recorded verification

The command above was run on 2026-10-01 with Python 3.12.14 from this skill's folder. Actual output:

```text
BEFORE
FAIL page_count(0, 5): expected 0, got 1
PASS page_count(1, 5): expected 1, got 1
FAIL page_count(5, 5): expected 1, got 2
PASS page_count(6, 5): expected 2, got 2
FAIL page_count(10, 5): expected 2, got 3
PASS page_count(11, 5): expected 3, got 3
SUMMARY: 3 passed, 3 failed
EXIT: 1
AFTER
PASS page_count(0, 5): expected 0, got 0
PASS page_count(1, 5): expected 1, got 1
PASS page_count(5, 5): expected 1, got 1
PASS page_count(6, 5): expected 2, got 2
PASS page_count(10, 5): expected 2, got 2
PASS page_count(11, 5): expected 3, got 3
SUMMARY: 6 passed, 0 failed
EXIT: 0
```

The outer verifier exited 0, meaning that the expected baseline failure and repaired pass both occurred. No real repository tests, broad application build, lint check, or remote CI job ran. These checks establish only the six listed cases for the two contained implementations.

## Example completion report

“Reproduced the extra-page defect for empty input and exact page boundaries. The one-line change uses rounded-up integer division and keeps the documented input contract unchanged. The synthetic checks failed 3 of 6 cases before the change and passed 6 of 6 afterward. Broader application behavior was not tested.”

In a real task, add the actual changed file paths, final revision or worktree identity, and project commands. Do not reuse this fixture's results as evidence for the user's checkout.
