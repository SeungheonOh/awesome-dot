#!/usr/bin/env python3
"""Create or verify the fictional native PDF example; never send or submit it.

Requires already-available public packages reportlab and pypdf.
Use --output-dir DIR to create, or --check DIR to verify existing files.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLANK = "room-enquiry-blank.pdf"
DRAFT = "room-enquiry-draft.pdf"
MAX_BYTES = 2 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_map():
    data = json.loads((HERE / "field-map.json").read_text())
    fields = {row["name"]: row for row in data["fields"]}
    require(len(fields) == 14, "Expected 14 uniquely named fields")
    source = (HERE / "source-brief.md").read_text()
    parts = re.split(r"^## (F[0-9]+) [^\n]+\n", source, flags=re.M)
    sections = dict(zip(parts[1::2], parts[2::2]))
    for row in fields.values():
        require(row["source"] in sections, "Missing source locator")
        if row["status"] in ("fill", "preserve"):
            answer = row.get("display_value", row["value"])
            require(answer in sections[row["source"]], "Answer not found at its source locator: " + row["name"])
        if row.get("max_length"):
            require(len(row["value"]) <= row["max_length"], "Field length exceeded")
        if row.get("options") and row["value"]:
            require(row["value"] in row["options"], "Unsupported choice value")
    datetime.strptime(fields["preferred_date"]["value"], "%Y-%m-%d")
    start = datetime.strptime(fields["start_time"]["value"], "%H:%M")
    end = datetime.strptime(fields["end_time"]["value"], "%H:%M")
    require(end > start, "This same-day example needs an end after its start")
    require(int(fields["attendee_count"]["value"]) > 0, "Invalid attendance")
    require(fields["projector_needed"]["value"] == "/No", "Unexpected projector branch")
    require(fields["projector_notes"]["value"] == "", "Inactive branch must stay blank")
    for name in ("setup_access", "setup_minutes", "extra_notes"):
        require(fields[name]["value"] == "", "Unsupported answer must stay blank")
    require(data["ready_to_submit"] is False, "Missing required answer blocks readiness")
    return data, fields


def create_blank(path, fields):
    from reportlab.lib.colors import HexColor, white
    from reportlab.pdfgen.canvas import Canvas

    canvas = Canvas(str(path), pagesize=(612, 792), invariant=1, pageCompression=1)
    canvas.setTitle("Fictional Community Room Use Enquiry")
    canvas.setAuthor("Fictional workflow example")
    canvas.setSubject("Non-binding enquiry fixture; no external destination")
    form = canvas.acroForm
    ink, muted, line = HexColor("#17242E"), HexColor("#48545D"), HexColor("#80939E")

    def text(x, y, value, size=9.5, bold=False, color=ink):
        canvas.setFillColor(color)
        canvas.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        canvas.drawString(x, y, value)

    def field(name, x, y, width, label=None):
        row = fields[name]
        text(x, y + 31, (label or row["label"]) + (" *" if row["required"] else ""))
        flags = "required" if row["required"] else ""
        if row.get("read_only"):
            flags = "readOnly"
        kw = dict(name=name, tooltip=row["label"], x=x, y=y, width=width, height=23,
                  value=row["value"] if row["status"] == "preserve" else "",
                  fontName="Helvetica", fontSize=11, borderColor=line,
                  fillColor=HexColor("#F0F2F3") if row.get("read_only") else white,
                  textColor=ink, borderWidth=0.7, forceBorder=True)
        if row["type"] == "/Ch":
            kw["value"] = [kw["value"]]  # An explicit blank choice, not a default answer.
            form.choice(**kw, options=row["options"], fieldFlags="combo " + flags)
        else:
            form.textfield(**kw, maxlen=row["max_length"], fieldFlags=flags)

    text(48, 748, "Community Room Use Enquiry", 21, True)
    text(48, 726, "FICTIONAL EXAMPLE  |  PRIVATE DRAFT  |  NOT SUBMITTED", 9, True, muted)
    text(48, 707, "An enquiry only. This form does not reserve a room or confirm availability.", 10)
    text(48, 691, "* Required answer. Dates: YYYY-MM-DD. Times: 24-hour, room-local.", 9.5, color=muted)
    field("group_name", 48, 638, 516)
    field("activity", 48, 584, 516)
    field("preferred_date", 48, 525, 168)
    field("start_time", 238, 525, 151)
    field("end_time", 411, 525, 153)
    field("attendee_count", 48, 466, 168)
    field("room_preference", 238, 466, 326)
    field("seating", 48, 407, 516)
    text(48, 375, "Projector needed *")
    for x, value in ((205, "Yes"), (296, "No")):
        form.radio(name="projector_needed", tooltip="Projector needed", value=value,
                   selected=False, x=x, y=370, size=14, buttonStyle="circle",
                   fieldFlags="radio required noToggleToOff", fillColor=white,
                   textColor=ink, borderColor=line, borderWidth=0.7)
        text(x + 22, 374, value, 11)
    field("projector_notes", 48, 321, 516, "Projector setup details (required only if Yes)")
    field("setup_access", 48, 262, 247)
    field("setup_minutes", 317, 262, 247, "Early-access minutes (required if Yes)")
    field("extra_notes", 48, 203, 516, "Extra notes (optional)")
    field("staff_reference", 48, 144, 516, "Staff use only (read-only; do not change)")
    text(48, 112, "Leave unsupported answers blank for review. Do not sign or submit this example.", 9.5)
    text(48, 95, "Form version 1  |  One page  |  No contact, payment or signature fields", 9, color=muted)
    canvas.showPage()
    canvas.save()


def deref(obj):
    return obj.get_object() if hasattr(obj, "get_object") else obj


def inherited(widget, key, default=None):
    current, seen = widget, set()
    while current is not None:
        require(id(current) not in seen, "Cyclic field-parent chain")
        seen.add(id(current))
        if key in current:
            return deref(current[key])
        current = deref(current["/Parent"]) if "/Parent" in current else None
    return default


def full_name(widget):
    current, parts, seen = widget, [], set()
    while current is not None:
        require(id(current) not in seen, "Cyclic field name")
        seen.add(id(current))
        if "/T" in current:
            parts.insert(0, str(current["/T"]))
        current = deref(current["/Parent"]) if "/Parent" in current else None
    return ".".join(parts)


def widgets(reader):
    result = []
    for page_number, page in enumerate(reader.pages, 1):
        for ref in page.get("/Annots", []):
            widget = deref(ref)
            require(widget.get("/Subtype") == "/Widget", "Unexpected annotation")
            require(not widget.get("/A") and not widget.get("/AA"), "Unexpected widget action")
            result.append((page_number, full_name(widget), widget))
    return result


def canonical_fields(reader):
    form = deref(reader.trailer["/Root"]["/AcroForm"])
    require(not form.get("/XFA") and not form.get("/SigFlags"), "Unsupported form feature")
    names, visited, canonical_widgets = [], set(), set()
    def visit(ref, parent=None):
        node = deref(ref)
        token = id(node)
        require(token not in visited, "Repeated or cyclic canonical field object")
        visited.add(token)
        if parent is None:
            require("/Parent" not in node, "Top-level field has an unexpected parent")
        else:
            require("/Parent" in node and deref(node["/Parent"]) is parent,
                    "Field child does not refer back to its canonical parent")
        if "/T" in node:
            names.append(full_name(node))
        if node.get("/Subtype") == "/Widget":
            canonical_widgets.add(token)
        for child in node.get("/Kids", []):
            visit(child, node)
    for ref in form["/Fields"]:
        visit(ref)
    page_widgets = [id(widget) for _, _, widget in widgets(reader)]
    require(len(page_widgets) == len(set(page_widgets)), "Widget appears more than once on pages")
    require(set(page_widgets) == canonical_widgets,
            "Canonical and page widgets are not the same reachable objects")
    require(len(names) == len(set(names)), "Duplicate canonical field name")
    return reader.get_fields() or {}


def control_signature(reader):
    rows = []
    for page, name, widget in widgets(reader):
        normal = deref(deref(widget.get("/AP", {})).get("/N", {}))
        states = sorted(str(k) for k in normal) if inherited(widget, "/FT") == "/Btn" else []
        rows.append((page, name, str(inherited(widget, "/FT")),
                     int(inherited(widget, "/Ff", 0)), inherited(widget, "/MaxLen"),
                     repr(inherited(widget, "/Opt", [])), list(widget["/Rect"]), states,
                     str(inherited(widget, "/TU", "")), int(widget.get("/F", 0)),
                     repr(inherited(widget, "/DV"))))
    return rows


def fill_draft(blank, draft, fields):
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(blank)
    require(set(canonical_fields(reader)) == set(fields), "Unexpected source field tree")
    require(len(widgets(reader)) == 15, "Unexpected source widgets")
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    # The fixture has a consistent tree. No field repair or flattening is needed.
    answers = {name: row["value"] for name, row in fields.items() if row["status"] == "fill"}
    writer.update_page_form_field_values(None, answers, auto_regenerate=False, flatten=False)
    # A radio group owns one value on its parent; each child owns its appearance state.
    # Remove redundant child values so they cannot shadow the canonical group value.
    for _, _, widget in widgets(writer):
        if inherited(widget, "/FT") == "/Btn" and "/Parent" in widget:
            widget.pop("/V", None)
    with draft.open("wb") as stream:
        writer.write(stream)


def identity(path):
    size = path.stat().st_size
    require(0 < size <= MAX_BYTES, "File is missing, empty or over 2 MiB")
    return {"file": path.name, "bytes": size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def verify(folder, data, fields):
    from pypdf import PdfReader
    blank, draft = folder / BLANK, folder / DRAFT
    before, after = PdfReader(blank), PdfReader(draft)
    require(len(before.pages) == len(after.pages) == 1, "Page count changed")
    original, saved = canonical_fields(before), canonical_fields(after)
    require(set(original) == set(saved) == set(fields), "Field set changed")
    require(control_signature(before) == control_signature(after), "Control definition changed")
    require(before.pages[0].get_contents().get_data() == after.pages[0].get_contents().get_data(),
            "Static labels, instructions or page content changed")
    require(before.pages[0].mediabox == after.pages[0].mediabox, "Page size changed")
    for reader in (before, after):
        root = reader.trailer["/Root"]
        require(not root.get("/OpenAction") and not root.get("/AA"), "Unexpected document action")
        require(not root.get("/Names"), "Unexpected named scripts, links or attachments")
        require(not reader.pages[0].get("/AA"), "Unexpected page action")
    for name, row in fields.items():
        initial = row["original_value"]
        require(str(original[name].get("/V", "/Off" if row["type"] == "/Btn" else "")) == initial, "Unexpected original value: " + name)
        require(str(saved[name].get("/V", "")) == row["value"], "Saved value mismatch: " + name)
        require(str(saved[name].get("/FT")) == row["type"], "Field type mismatch: " + name)
        flags = int(saved[name].get("/Ff", 0))
        require(bool(flags & 1) == row.get("read_only", False), "Read-only flag mismatch: " + name)
        require(bool(flags & 2) == row["required"], "Required flag mismatch: " + name)
    require(len(widgets(after)) == 15, "Widget count changed")
    selected = []
    for _, name, widget in widgets(after):
        row = fields[name]
        expected = row["value"]
        require(str(inherited(widget, "/V", "")) == expected, "Widget value mismatch: " + name)
        require(list(widget["/Rect"])[2] > list(widget["/Rect"])[0], "Invalid field geometry")
        if row.get("max_length"):
            require(inherited(widget, "/MaxLen") == row["max_length"], "Length limit mismatch: " + name)
        if row["type"] == "/Ch":
            require(list(inherited(widget, "/Opt")) == row["options"], "Option set mismatch: " + name)
            index = inherited(widget, "/I")
            if index is not None:
                require(list(index) == [row["options"].index(expected)], "Stale choice index: " + name)
        normal = deref(deref(widget.get("/AP", {})).get("/N", {}))
        if fields[name]["type"] == "/Btn":
            state = str(widget.get("/AS", "/Off"))
            require(state in normal, "Button state lacks an appearance")
            require(bool(deref(normal[state]).get_data()), "Empty button appearance")
            require(state in ("/Off", expected), "Wrong selected button")
            if state != "/Off":
                selected.append(state)
        else:
            require(hasattr(normal, "get_data") and bool(normal.get_data()), "Missing field appearance: " + name)
    require(selected == ["/No"], "Radio group selection is wrong")
    return {"result":"PASS", "files":[identity(blank), identity(draft)],
            "canonical_fields":14, "page_widgets":15, "filled_answers":9,
            "preserved_staff_fields":1, "unresolved_required":["setup_access"],
            "unresolved_conditional":["setup_minutes"], "inactive_fields":["projector_notes"],
            "optional_blank":["extra_notes"], "ready_to_submit":False,
            "unresolved_question":data["unresolved_question"],
            "limits":["Does not render or visually inspect pages", "Does not test editing in a PDF viewer",
                      "Does not certify accessibility", "Never submits or contacts a recipient"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--output-dir", type=Path, help="Create blank and filled PDFs in a new/empty directory")
    modes.add_argument("--check", type=Path, help="Only verify existing blank and filled PDFs")
    args = parser.parse_args()
    data, fields = load_map()
    folder = args.output_dir or args.check
    if args.output_dir:
        folder.mkdir(parents=True, exist_ok=True)
        require(not (folder / BLANK).exists() and not (folder / DRAFT).exists(), "Refusing to overwrite existing PDFs")
        create_blank(folder / BLANK, fields)
        original_hash = identity(folder / BLANK)["sha256"]
        fill_draft(folder / BLANK, folder / DRAFT, fields)
        require(identity(folder / BLANK)["sha256"] == original_hash, "Original changed during fill")
    print(json.dumps(verify(folder, data, fields), indent=2))


if __name__ == "__main__":
    main()
