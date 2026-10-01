# A cabinet in an L-shaped bench's open corner

This additional fictional case checks a limitation of a bounding-box-only approach. The measured furniture shape is supplied as the union of two rectangles. Treating that union as a filled bounding rectangle would wrongly reject a usable nominal position.

## Supplied packet

M1 is an invented owner measurement sheet dated 2026-09-30. All dimensions are centimeters. The origin is the inside northwest corner, x increases right/east and y down/south. These are plan directions. The room is the usable rectangle `(0,0)` to `(400,300)`, with no other reported intrusions.

| Supplied component | x | y | Width | Depth | Meaning |
|---|---:|---:|---:|---:|---|
| B-horizontal | 20 | 20 | 180 | 50 | Horizontal component of one L-shaped bench |
| B-vertical | 20 | 70 | 50 | 130 | Vertical component of that same bench |
| E | 300 | 0 | 80 | 300 | Protected entry reserve from the south opening to y=0 |

The bench is exactly the union of B-horizontal and B-vertical. Their shared edge belongs to the same piece, not a collision between separate furniture. M2 confirms the bench and cabinet are the only in-scope furniture footprints.

The cabinet has unrotated width 80 and depth 60. Both candidates rotate it 90° clockwise. The final northwest anchor is `(90,90)` in A and `(60,90)` in B. No original front-facing direction is supplied, so its rotated front or operating needs cannot be inferred.

The supplied south-wall opening extends from x=300 to x=380 at y=300. E exactly connects that opening to y=0. Furniture must stay inside the room without touching its walls, and the two pieces must not overlap or touch each other. Boundary contact with E is allowed; no extra distance requirement is specified.

Measurement/placement uncertainty, protrusions beyond the stated footprints, operating envelopes, heights and the physical delivery route are unmeasured. The request is to compare these nominal plans, not to move or buy anything. An opening's nominal width is not proof of delivery fit.

## Result

**A meets the supplied nominal constraints. B fails:** its cabinet overlaps the vertical bench component over `(60,90)` to `(70,170)`, measuring **10 × 80 cm = 800 cm²**. Neither result is an independently verified or tolerance-checked physical fit.

| Item | Final x, y | Final width × depth | East, south |
|---|---|---|---|
| Bench horizontal, both plans | 20, 20 | 180 × 50 | 200, 70 |
| Bench vertical, both plans | 20, 70 | 50 × 130 | 70, 200 |
| Cabinet A, rotated | 90, 90 | 60 × 80 | 150, 170 |
| Cabinet B, rotated | 60, 90 | 60 × 80 | 120, 170 |
| Entry reserve E | 300, 0 | 80 × 300 | 380, 300 |

- All furniture is strictly inside the room in both plans. The bench's west/north/east/south margins are 20/20/200/100 cm; A's cabinet margins are 90/90/250/130 cm; B's are 60/90/280/130 cm
- In A, the cabinet is 20 cm below the horizontal component and 20 cm right of the vertical component. It occupies the actual open notch, with no furniture contact
- In B, the cabinet still clears the horizontal component, but overlaps the vertical component by 10 cm horizontally and 80 cm vertically
- The bench ends at x=200, at least 100 cm left of E. A's cabinet ends at x=150, and B's at x=120. E remains unobstructed and connects its stated endpoints
- The bench's solid bounding rectangle would be `(20,20,180,180)`. Both cabinets fall inside that box, but the box includes empty space. Its overlap alone is not a sound reason to reject A

Use A as the nominal option to verify. The 20 cm separations are calculated available margins, not an invented minimum or a guarantee that measurement errors fit inside them. Before moving, verify maximum usable/occupied shapes, uncertainty bounds, cabinet orientation and operating needs, heights and the complete delivery route. The plan establishes no structural, regulatory, accessibility, comfort or assembly conclusion.

## Reproduce the nominal geometry

The following standard-library check evaluates only this exact union of two axis-aligned rectangles. It is not a general polygon engine. The two components have no positive-area overlap, so their cabinet intersection areas can be summed without double-counting. Boundary contact remains a separate test.

```python
from decimal import Decimal as D
from itertools import combinations

# x, y, width, depth; values transcribed from M1 and the candidate anchors.
def rect(*values):
    return tuple(D(str(v)) for v in values)

room = rect(0, 0, 400, 300)
bench = [rect(20, 20, 180, 50), rect(20, 70, 50, 130)]
reserve = rect(300, 0, 80, 300)
base_width, base_depth = D(80), D(60)
rotated_width, rotated_depth = base_depth, base_width
assert (rotated_width, rotated_depth) == (D(60), D(80))
cabinets = {"A": rect(90, 90, rotated_width, rotated_depth),
            "B": rect(60, 90, rotated_width, rotated_depth)}


def intersection(a, b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    east = min(a[0] + a[2], b[0] + b[2])
    south = min(a[1] + a[3], b[1] + b[3])
    return x, y, max(D(0), east-x), max(D(0), south-y)


def area(a, b):
    _, _, width, depth = intersection(a, b)
    return width * depth


def touches_or_overlaps(a, b):
    return (min(a[0]+a[2], b[0]+b[2]) >= max(a[0], b[0])
            and min(a[1]+a[3], b[1]+b[3]) >= max(a[1], b[1]))


def contained(r, strict=False):
    x, y, width, depth = r
    assert width > 0 and depth > 0
    if strict:
        return 0 < x and 0 < y and x+width < room[2] and y+depth < room[3]
    return 0 <= x and 0 <= y and x+width <= room[2] and y+depth <= room[3]

# An internal seam is allowed within the same bench. No overlapping area is counted twice.
assert all(area(a, b) == 0 for a, b in combinations(bench, 2))
assert touches_or_overlaps(*bench)
assert contained(reserve) and reserve[1] == 0 and reserve[1]+reserve[3] == room[3]
assert (reserve[0], reserve[0]+reserve[2]) == (D(300), D(380))
assert all(contained(component, strict=True) for component in bench)

results = {}
for name, cabinet in cabinets.items():
    assert contained(cabinet, strict=True)
    assert all(area(item, reserve) == 0 for item in bench + [cabinet])
    overlaps = [area(cabinet, component) for component in bench]
    contact = any(touches_or_overlaps(cabinet, component) for component in bench)
    results[name] = {"area": sum(overlaps), "nominal_pass": not contact}
assert results == {"A": {"area": D(0), "nominal_pass": True},
                   "B": {"area": D(800), "nominal_pass": False}}
assert intersection(cabinets["B"], bench[1]) == rect(60, 90, 10, 80)
assert area(cabinets["B"], bench[0]) == 0

# A solid-box substitution is a demonstrated false rejection for A.
bounding_box = rect(20, 20, 180, 180)
assert area(cabinets["A"], bounding_box) == D(4800)
assert sum(area(cabinets["A"], part) for part in bench) == 0

# Boundary contact has zero area but still violates this request's furniture rule.
contact_case = rect(70, 90, rotated_width, rotated_depth)
assert sum(area(contact_case, part) for part in bench) == 0
assert any(touches_or_overlaps(contact_case, part) for part in bench)
print("PASS: actual L-shaped union; rotated 60x80 cabinet; A nominally passes;")
print("      B overlaps by 10x80=800 cm2; bounding-box false rejection and contact checked")
```

Run the fence from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('skill/room-layout-fit-check/l-shaped-example.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'l-shaped-layout-check', 'exec'))
PY
```

Observed locally on 2026-10-01 with Python 3.12.14: the exact block passed. The source-to-result interpretation was also reviewed against the fictional packet. This checks nominal geometry and the stated counterexamples only; no room measurements, actual furniture, unknown tolerances, operating envelopes or delivery route were verified.
