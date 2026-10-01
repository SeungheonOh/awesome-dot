#!/usr/bin/env python3
"""Fictional axis-aligned nominal geometry check; standard library only."""
import argparse
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from itertools import combinations
from pathlib import Path
import platform
import xml.etree.ElementTree as ET


def dec(value):
    if not isinstance(value, (str, Decimal)):
        raise ValueError("Use decimal strings, not binary floats")
    try:
        value = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("Invalid decimal string") from exc
    if not value.is_finite():
        raise ValueError("Non-finite value")
    return value


@dataclass(frozen=True)
class Rect:
    x: Decimal
    y: Decimal
    w: Decimal
    d: Decimal

    def __post_init__(self):
        for key in ("x", "y", "w", "d"):
            object.__setattr__(self, key, dec(getattr(self, key)))
        if self.w <= 0 or self.d <= 0:
            raise ValueError("Dimensions must be positive")


def rotated(x, y, width, depth, degrees):
    if degrees not in (0, 90, 180, 270):
        raise ValueError("Only quarter turns are modeled")
    if degrees in (90, 270):
        width, depth = depth, width
    return Rect(x, y, width, depth)


def spans(a, b):
    return (min(a.x + a.w, b.x + b.w) - max(a.x, b.x),
            min(a.y + a.d, b.y + b.d) - max(a.y, b.y))


def overlaps(a, b):
    ix, iy = spans(a, b)
    return ix > 0 and iy > 0


def touches(a, b):
    ix, iy = spans(a, b)
    return ix >= 0 and iy >= 0 and (ix == 0 or iy == 0)


ROOM = Rect("0", "0", "420", "320")
A = {
    "desk": rotated("100", "5", "140", "60", 0),
    "sofa": rotated("160", "235", "180", "80", 0),
    "bookcase": rotated("385", "10", "80", "30", 90),
    "table": rotated("345", "275", "40", "40", 0),
}
ZONES = {
    "entry-route": Rect("0", "0", "90", "320"),
    "door-reserve": Rect("0", "230", "90", "90"),
    "desk-work": Rect(A["desk"].x, A["desk"].y + A["desk"].d,
                      A["desk"].w, "80"),
}
B = {**A, "sofa": rotated("170", "115", "180", "80", 0)}


def encloses(a, b):
    return (b.x >= a.x and b.y >= a.y and b.x + b.w <= a.x + a.w
            and b.y + b.d <= a.y + a.d)


def contained(r):
    return encloses(ROOM, r)


def check(items, zones, allowed_pairs=(), allowed_walls=()):
    """Zones prohibit positive-area intrusion; their boundary contact is allowed."""
    problems = []
    for name, r in items.items():
        if not contained(r):
            problems.append(("out-of-room", name))
        walls = {"west": r.x == 0, "north": r.y == 0,
                 "east": r.x + r.w == ROOM.w, "south": r.y + r.d == ROOM.d}
        for wall, contact in walls.items():
            if contact and (name, wall) not in allowed_walls:
                problems.append(("wall-contact", name, wall))
        for zone, z in zones.items():
            if overlaps(r, z):
                problems.append(("zone-obstruction", name, zone))
    for name, z in zones.items():
        if not contained(z):
            problems.append(("zone-out-of-room", name))
    for (an, a), (bn, b) in combinations(items.items(), 2):
        if overlaps(a, b):
            problems.append(("furniture-overlap", an, bn))
        elif touches(a, b) and frozenset((an, bn)) not in allowed_pairs:
            problems.append(("furniture-contact", an, bn))
    return problems


def svg_text():
    ns = "http://www.w3.org/2000/svg"
    ET.register_namespace("", ns)
    def element(parent, tag, attrs=None, text=None):
        node = ET.SubElement(parent, f"{{{ns}}}{tag}", attrs or {})
        node.text = text
        return node
    root = ET.Element(f"{{{ns}}}svg", {"viewBox": "-20 -40 460 435", "role": "img",
                                      "aria-labelledby": "title desc"})
    element(root, "title", {"id": "title"}, "Candidate A: nominal room layout in cm")
    element(root, "desc", {"id": "desc"}, "Origin northwest; x right, y down. Blue entry route, purple door reserve and amber desk-work zone remain clear. Unmeasured geometry omitted; physical fit unverified.")
    element(root, "rect", {"x": "-20", "y": "-40", "width": "460", "height": "435", "fill": "white"})
    element(root, "text", {"x": "0", "y": "-18", "font-size": "12"}, "A · 420 × 320 cm · (0,0) top left · x →, y ↓")
    all_rects = {"room": ROOM, **ZONES, **A}
    fills = {"room": "#fff", "entry-route": "#dceef9", "door-reserve": "#e4d8f6", "desk-work": "#fff0b9"}
    for name, r in all_rects.items():
        element(root, "rect", {"id": name, "x": str(r.x), "y": str(r.y),
                               "width": str(r.w), "height": str(r.d),
                               "fill": fills.get(name, "#dce8de"), "stroke": "#444", "stroke-width": "1"})
    for name, r in A.items():
        label = "B" if name == "bookcase" else name
        element(root, "text", {"x": str(r.x + 5), "y": str(r.y + 18), "font-size": "11"}, label)
    element(root, "text", {"x": "105", "y": "90", "font-size": "11"}, "desk work: 140 × 80")
    element(root, "text", {"x": "12", "y": "155", "font-size": "11"}, "route: 90")
    element(root, "text", {"x": "7", "y": "267", "font-size": "10"}, "door reserve")
    element(root, "line", {"id": "opening", "x1": "0", "y1": "320", "x2": "90", "y2": "320", "stroke": "#753fad", "stroke-width": "4"})
    element(root, "text", {"x": "0", "y": "344", "font-size": "11"}, "Purple bottom edge: supplied south-wall opening")
    element(root, "text", {"x": "0", "y": "364", "font-size": "11"}, "B: bookcase rotated 90° clockwise, front west")
    element(root, "text", {"x": "0", "y": "384", "font-size": "11"}, "Nominal schematic only · unknown margins/geometry remain")
    return ET.tostring(root, encoding="unicode") + "\n"


def must_reject(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Invalid input accepted")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-svg", action="store_true")
    args = parser.parse_args()
    assert not check(A, ZONES)
    assert check(B, ZONES) == [("zone-obstruction", "sofa", "desk-work")]
    route = ZONES["entry-route"]
    assert route.y == 0 and route.y + route.d == ROOM.d
    assert route.x <= 0 and route.x + route.w >= 90
    assert encloses(route, ZONES["door-reserve"])
    ix, iy = spans(B["sofa"], ZONES["desk-work"])
    assert (ix, iy, ix * iy) == (Decimal("70"), Decimal("30"), Decimal("2100"))
    assert (A["bookcase"].w, A["bookcase"].d) == (Decimal("30"), Decimal("80"))
    assert rotated("1", "2", "80", "30", 270) == rotated("1", "2", "80", "30", 90)
    assert rotated("1", "2", "80", "30", 180) == rotated("1", "2", "80", "30", 0)
    assert ("out-of-room", "bookcase") in check({"bookcase": Rect("391", "10", "30", "80")}, {})
    assert not contained(Rect("-0.01", "10", "30", "80"))
    assert check({}, {"bad-zone": Rect("0", "310", "90", "20")}) == [("zone-out-of-room", "bad-zone")]
    wall_item = {"a": Rect("0", "1", "10", "10")}
    assert check(wall_item, {}) == [("wall-contact", "a", "west")]
    assert not check(wall_item, {}, allowed_walls=(("a", "west"),))
    pair = {"a": Rect("10", "10", "20", "20"), "b": Rect("30", "10", "20", "20")}
    assert check(pair, {}) == [("furniture-contact", "a", "b")]
    assert not check(pair, {}, allowed_pairs=(frozenset(("a", "b")),))
    corner = {**pair, "b": Rect("30", "30", "20", "20")}
    assert check(corner, {}) == [("furniture-contact", "a", "b")]
    collision = {**pair, "b": Rect("29.99", "10", "20", "20")}
    assert check(collision, {}, allowed_pairs=(frozenset(("a", "b")),)) == [("furniture-overlap", "a", "b")]
    assert touches(A["desk"], ZONES["desk-work"])
    assert Decimal("1") * Decimal("2.54") == Decimal("2.54")
    for value in ("0", "-1", "NaN", "Infinity", "unknown", 0.1):
        must_reject(lambda value=value: Rect("0", "0", value, "10"))
    must_reject(lambda: rotated("1", "1", "10", "20", 45))
    path = Path(__file__).with_name("candidate-a.svg")
    rendered = svg_text()
    if args.write_svg:
        path.write_text(rendered, encoding="utf-8")
    assert path.read_text(encoding="utf-8") == rendered, "SVG is not the checked fixture"
    root = ET.fromstring(rendered)
    by_id = {node.attrib["id"]: node for node in root.iter() if "id" in node.attrib}
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert all(name in by_id for name in root.attrib["aria-labelledby"].split())
    for name, r in {"room": ROOM, **ZONES, **A}.items():
        attrs = by_id[name].attrib
        assert tuple(Decimal(attrs[k]) for k in ("x", "y", "width", "height")) == (r.x, r.y, r.w, r.d)
    opening = by_id["opening"].attrib
    assert tuple(Decimal(opening[k]) for k in ("x1", "y1", "x2", "y2")) == (0, 320, 90, 320)
    print(f"PASS Python {platform.python_version()}: A nominally feasible; B rejected, desk-work obstruction 70 x 30 = 2100 cm^2")
    print("PASS rotation, room/zone bounds, connected entry route, contact rules, positive overlap, invalid inputs, SVG XML and coordinate parity")
    print("Not checked: real measurements, irregular polygons, tolerance envelopes, vertical/operating/delivery fit")


if __name__ == "__main__":
    main()
