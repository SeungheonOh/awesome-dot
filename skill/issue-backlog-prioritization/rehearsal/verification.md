# Verification of the fictional decision

A fresh synthetic packet was processed using the skill instructions without its earlier worked example or an expected answer. The [result](result.md) is a condensed public version of the resulting artifact. Its source mapping, scores, gates, uncertainty and dependency conclusions were independently compared with the [input](input.md).

The negative effort coefficient reverses which endpoint gives the minimum score. Failed and unknown gates remain outside the eligible comparison even when their arithmetic scores are larger. Duplicate source rows do not create another candidate, and the ready set is distinct from the importance order.

## Repeatable arithmetic and graph checks

From this folder, copy this block into Python 3. It reads only the adjacent fictional input and writes nothing. It parses this fixed table, not arbitrary tracker exports.

```python
from pathlib import Path
import re

rows = []
for line in Path('input.md').read_text().splitlines():
    if re.match(r'^\| R\d+ \|', line):
        fields = [x.strip() for x in line.strip('|').split('|')]
        source, issue, title, version, gate, impact, urgency, effort, needs = fields
        rows.append((source, issue, title, int(version), gate, int(impact),
                     int(urgency), None if effort == 'unknown' else int(effort),
                     [] if needs == 'none' else [needs]))
assert len(rows) == 11
issues, sources = {}, {}
for source, issue, *record in rows:
    if issue in issues:
        assert issues[issue] == record
    issues[issue] = record
    sources.setdefault(issue, []).append(source)
assert len(issues) == 10 and sources['Q-13'] == ['R3', 'R11']

def values(issue):
    title, version, gate, impact, urgency, effort, needs = issues[issue]
    assert 1 <= impact <= 5 and 0 <= urgency <= 3
    effort_values = range(1, 9) if effort is None else [effort]
    assert all(1 <= e <= 8 for e in effort_values)
    return [3 * impact + 2 * urgency - e for e in effort_values]

scores = {issue: values(issue) for issue in issues}
assert {k: v[0] for k, v in scores.items() if len(v) == 1} == {
    'Q-11': 16, 'Q-12': 2, 'Q-14': 12, 'Q-15': 12,
    'Q-16': 20, 'Q-17': 19, 'Q-18': 7, 'Q-19': 4, 'Q-20': 8,
}
assert scores['Q-13'] == list(range(13, 5, -1))
assert min(scores['Q-13']) == 6 and max(scores['Q-13']) == 13
eligible = {k for k, record in issues.items() if record[2] == 'pass'}
assert eligible == set(issues) - {'Q-16', 'Q-17'}
# All supplied issues are explicitly open. No supplied completion is inferred.
ready = {k for k in eligible if not issues[k][-1]}
assert ready == {'Q-12', 'Q-13', 'Q-14', 'Q-15'}
for effort, q13_score in enumerate(scores['Q-13'], 1):
    ready_scores = {k: (q13_score if k == 'Q-13' else scores[k][0]) for k in ready}
    winners = {k for k, v in ready_scores.items() if v == max(ready_scores.values())}
    expected = ({'Q-13'} if effort == 1 else
                {'Q-13', 'Q-14', 'Q-15'} if effort == 2 else {'Q-14', 'Q-15'})
    assert winners == expected
assert issues['Q-18'][-1] == ['Q-19'] and issues['Q-19'][-1] == ['Q-18']
assert {p for record in issues.values() for p in record[-1] if p not in issues} == {'X-90'}
assert issues['Q-11'][-1] == ['Q-12']
print('PASS: duplicate, nine exact scores, reversed bounds, gates, conditional ready winners and dependency evidence')
```

Observed on Python 3.12.14: exit 0 with the stated PASS line. The arithmetic check enumerates all eight allowed effort values; it does not choose the missing value. The source-to-output comparison and partial-order wording were reviewed separately.

This exercise used fictional local text only. No live evidence, tracker access, field mapping, concurrent update, remote write/readback, person assignment or external delivery was tested. One successful rehearsal is evidence about this packet, not every backlog or connected application.
