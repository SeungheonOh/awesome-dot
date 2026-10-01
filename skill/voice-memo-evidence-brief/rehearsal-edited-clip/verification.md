# Verification of the edited-clip brief

A fresh synthetic packet was processed using the skill instructions without its earlier fixture or an expected answer. The [result](result.md) preserves the resulting brief and evidence appendix, with local reference links and one claim-label clarification added. No audio file was supplied, opened or transcribed.

## Repeatable source-time checks

Run this single block with Python 3. It uses exact rational arithmetic from the [supplied editing log](input.md), writes nothing and opens no media. Each citation interval must be split at a cut; the full S2 text remains associated with its pair of spans because no word-level alignment was supplied.

```python
from fractions import Fraction as F

# clip start, clip end, original start, original end; integer milliseconds
edit_map = [(0, 20000, 60000, 80000),
            (20000, 30000, 200000, 220000),
            (30000, 45000, 500000, 515000)]
segments = {
    'S1': (5000, 10000), 'S2': (18000, 24000), 'S3': (24000, 29000),
    'S4': (31000, 36000), 'S5': (35000, 40000), 'S6': (43000, 45000),
}

def map_interval(start, end):
    if not 0 <= start < end <= 45000:
        raise ValueError('Invalid or out-of-clip interval')
    pieces = []
    for c0, c1, o0, o1 in edit_map:
        lo, hi = max(start, c0), min(end, c1)
        if lo < hi:
            rate = F(o1-o0, c1-c0)
            pieces.append((lo, hi, o0+(lo-c0)*rate, o0+(hi-c0)*rate))
    if sum(hi-lo for lo, hi, _, _ in pieces) != end-start:
        raise ValueError('Source mapping does not cover the whole citation')
    return pieces

assert [F(o1-o0, c1-c0) for c0, c1, o0, o1 in edit_map] == [1, 2, 1]
assert all(edit_map[i][1] == edit_map[i+1][0] for i in range(2))
expected = {
    'S1': [(5000, 10000, 65000, 70000)],
    'S2': [(18000, 20000, 78000, 80000), (20000, 24000, 200000, 208000)],
    'S3': [(24000, 29000, 208000, 218000)],
    'S4': [(31000, 36000, 501000, 506000)],
    'S5': [(35000, 40000, 505000, 510000)],
    'S6': [(43000, 45000, 513000, 515000)],
}
assert {key: map_interval(*value) for key, value in segments.items()} == expected
assert map_interval(19000, 21000) == [(19000, 20000, 79000, 80000),
                                     (20000, 21000, 200000, 202000)]
assert map_interval(29000, 31000) == [(29000, 30000, 218000, 220000),
                                     (30000, 31000, 500000, 501000)]
assert map_interval(0, 1) == [(0, 1, 60000, 60001)]
assert map_interval(44999, 45000) == [(44999, 45000, 514999, 515000)]
overlap = (max(segments['S4'][0], segments['S5'][0]),
           min(segments['S4'][1], segments['S5'][1]))
assert overlap == (35000, 36000)
assert map_interval(*overlap) == [(35000, 36000, 505000, 506000)]
for invalid in [(-1, 1000), (1000, 1000), (44000, 45001)]:
    try:
        map_interval(*invalid)
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid interval accepted')
print('PASS: six segment maps, both cut boundaries, 2x span, clip endpoints, overlap and three invalid intervals')
```

Observed on Python 3.12.14: exit 0 and the stated PASS line. The two cut-boundary probes are arithmetic tests, not additional transcript excerpts. Original total duration is unknown, so original-duration bounds were not checked. The supplied edit log was used as evidence; its authenticity was not independently established.

## Separate source-to-claim review

- S3 leaves A's preparation commitment current and removes the earlier publication commitment and confirmed-Friday interpretation from the current action list; both S1 and S3 remain cited
- S2 preserves its conditional wording and `[Lee/Leigh?]` uncertainty; “can send” is not treated as accepted work or proof of approval
- S4's reported internal-only approval and S5's report of B's non-approval for external release can both be true. Neither proves the relevant authority or an actual external action
- S6 preserves `[inaudible]`, its unassigned label and the missing continuation. No recipient, accepted owner or referent is invented
- All six excerpts and supplied labels are unchanged. S2 is not divided into guessed word-to-time assignments. S4/S5 overlap is preserved rather than forced into sequential turns
- Recording date/timezone remain unknown. No due date was derived from the analysis date, and media time was not presented as calendar time

These are checks of fictional text, arithmetic and the produced interpretation. The code does not infer commitments or verify speech. No acoustic review, speaker identification, playback-link behavior, original-recording integrity, live document save, external delivery or task execution was tested.
