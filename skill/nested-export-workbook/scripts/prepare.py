"""Bounded, strict adapter for the fictional pocket-shelf/1 schema. No XLSX I/O."""
import argparse
import hashlib
import json
import re
from pathlib import Path


class Held(ValueError):
    pass


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Held(f"Duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def exact_integer(token):
    # This small adapter has no decimal measure. Refuse conversion, never round.
    if token == "-0" or len(token.lstrip("-")) > 15:
        raise Held("Unsupported number: negative zero or more than 15 digits")
    return int(token)


def unsupported_number(token):
    raise Held(f"Unsupported numeric token: {token}")


def load_source(path):
    raw = path.read_bytes()
    if len(raw) > 65536:
        raise Held("Source exceeds this adapter's 64 KiB limit")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                          parse_int=exact_integer, parse_float=unsupported_number,
                          parse_constant=unsupported_number)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Held(f"Malformed UTF-8 JSON: {exc}") from exc
    validate(data)
    return raw, data


def string(value, where):
    if type(value) is not str or len(value.encode("utf-16-le", errors="surrogatepass")) // 2 > 32767:
        raise Held(f"Unsupported text at {where}")
    if any(ord(c) in range(0xD800, 0xE000) or (ord(c) < 32 and c not in "\t\n\r")
           or ord(c) in (0xFFFE, 0xFFFF) for c in value):
        raise Held(f"Unsupported XML character at {where}")


def view_text(value, where):
    string(value, where)
    if re.match(r"^\d{4}-\d{2}-\d{2}(?:$|[Tt ])", value) or value.startswith("'="):
        raise Held(f"Unsupported direct text conversion at {where}; choose an explicit encoded-text mapping")


def object_shape(value, required, optional, where):
    if type(value) is not dict:
        raise Held(f"Expected object at {where}")
    if set(value) - set(required) - set(optional) or set(required) - set(value):
        raise Held(f"Unsupported or missing fields at {where}")


def optional_text(obj, name, where):
    if name in obj and obj[name] is not None:
        view_text(obj[name], where + "/" + name)


def validate(data):
    object_shape(data, ["format", "exportedAt", "collections"], [], "root")
    if data["format"] != "pocket-shelf/1":
        raise Held("Unsupported format; inspect the actual schema before adapting")
    string(data["exportedAt"], "/exportedAt")
    if type(data["collections"]) is not list or not 1 <= len(data["collections"]) <= 100:
        raise Held("Expected 1–100 collections")
    child_count = 0
    for p, parent in enumerate(data["collections"]):
        at = f"/collections/{p}"
        object_shape(parent, ["id", "name"], ["note", "items", "labels"], at)
        view_text(parent["id"], at + "/id")
        view_text(parent["name"], at + "/name")
        optional_text(parent, "note", at)
        for rel in ("items", "labels"):
            value = parent.get(rel)
            if value is not None and type(value) is not list:
                raise Held(f"Expected array/null/absent at {at}/{rel}")
            child_count += len(value or [])
        for i, child in enumerate(parent.get("items") or []):
            loc = f"{at}/items/{i}"
            object_shape(child, ["id", "name"], ["quantity", "note"], loc)
            view_text(child["id"], loc + "/id")
            view_text(child["name"], loc + "/name")
            optional_text(child, "note", loc)
            if child.get("quantity") is not None and type(child["quantity"]) is not int:
                raise Held(f"Expected integer/null/absent at {loc}/quantity")
        for i, label in enumerate(parent.get("labels") or []):
            view_text(label, f"{at}/labels/{i}")
    if child_count > 300:
        raise Held("More than 300 child occurrences; revise the bounded plan")


def state(value):
    if value is None:
        return "NULL"
    if type(value) is str:
        return "EMPTY_STRING" if value == "" else "STRING"
    if type(value) is int:
        return "INTEGER"
    if type(value) is list:
        return "EMPTY_ARRAY" if not value else "ARRAY"
    if type(value) is dict:
        return "OBJECT"
    raise Held("Unsupported value")


def field_state(obj, field):
    return state(obj[field]) if field in obj else "MISSING"


def escape(token):
    return str(token).replace("~", "~0").replace("/", "~1")


def column(number):
    value = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        value = chr(65 + remainder) + value
    return value


HEADERS = {
    "Collections": ["Source order", "Collection ID", "Name", "Note", "Note state", "Items state", "Items count", "Labels state", "Labels count", "Source pointer"],
    "Items": ["Parent order", "Item order", "Item ID", "Name", "Quantity", "Quantity state", "Note", "Note state", "Source pointer", "Parent pointer"],
    "Labels": ["Parent order", "Label order", "Label", "Source pointer", "Parent pointer"],
    "Source paths": ["Node order", "Source pointer", "Parent pointer", "Key/index", "State", "Scalar JSON", "View cells"]
}


def make_plan(source_name, raw, data):
    rows = {name: [] for name in HEADERS}
    mapping = {}
    missing = []
    def mapped(pointer, sheet, row, col):
        mapping[pointer] = f"{sheet}!{column(col)}{row}"
    def expected(obj, fields, pointer):
        for field in fields:
            if field not in obj:
                missing.append((pointer + "/" + escape(field), pointer, field))
    for p, parent in enumerate(data["collections"]):
        ptr = f"/collections/{p}"
        r = len(rows["Collections"]) + 2
        rows["Collections"].append([p, parent["id"], parent["name"], parent.get("note"), field_state(parent, "note"),
                                    field_state(parent, "items"), len(parent["items"]) if type(parent.get("items")) is list else None,
                                    field_state(parent, "labels"), len(parent["labels"]) if type(parent.get("labels")) is list else None, ptr])
        mapping[ptr] = f"Collections!A{r}:J{r}"
        for field, col in [("id", 2), ("name", 3), ("note", 4), ("items", 6), ("labels", 8)]:
            mapped(ptr + "/" + field, "Collections", r, col)
        expected(parent, ["note", "items", "labels"], ptr)
        for i, item in enumerate(parent.get("items") or []):
            iptr = f"{ptr}/items/{i}"
            ir = len(rows["Items"]) + 2
            rows["Items"].append([p, i, item["id"], item["name"], item.get("quantity"), field_state(item, "quantity"),
                                  item.get("note"), field_state(item, "note"), iptr, ptr])
            mapping[iptr] = f"Items!A{ir}:J{ir}"
            for field, col in [("id", 3), ("name", 4), ("quantity", 5), ("note", 7)]:
                mapped(iptr + "/" + field, "Items", ir, col)
            expected(item, ["quantity", "note"], iptr)
        for i, label in enumerate(parent.get("labels") or []):
            lptr = f"{ptr}/labels/{i}"
            lr = len(rows["Labels"]) + 2
            rows["Labels"].append([p, i, label, lptr, ptr])
            mapped(lptr, "Labels", lr, 3)
    def walk(value, pointer="", parent="", key=""):
        kind = state(value)
        token = json.dumps(value, ensure_ascii=False, separators=(",", ":")) if kind not in ("ARRAY", "OBJECT", "EMPTY_ARRAY") else None
        # JSON evidence can be longer than its decoded string. Reject before authoring.
        if token is not None:
            string(token, pointer + " (JSON token)")
        rows["Source paths"].append([len(rows["Source paths"]), pointer, parent, str(key), kind, token, mapping.get(pointer)])
        if type(value) is dict:
            for k, v in value.items():
                walk(v, pointer + "/" + escape(k), pointer, k)
        if type(value) is list:
            for k, v in enumerate(value):
                walk(v, pointer + "/" + str(k), pointer, k)
    walk(data)
    actual_count = len(rows["Source paths"])
    for pointer, parent, key in missing:
        rows["Source paths"].append([None, pointer, parent, key, "MISSING", None, mapping[pointer]])
    return {"source": {"file": source_name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                       "selection": "entire supplied JSON document", "format": data["format"], "exportedAt": data["exportedAt"]},
            "headers": HEADERS, "rows": rows,
            "counts": {"collections": len(rows["Collections"]), "items": len(rows["Items"]), "labels": len(rows["Labels"]),
                       "actual_source_nodes": actual_count, "missing_schema_fields": len(missing)},
            "index_base": 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    raw, data = load_source(args.source)
    plan = make_plan(args.source.name, raw, data)
    args.plan.parent.mkdir(parents=True, exist_ok=True)
    with args.plan.open("x", encoding="utf-8") as file:
        json.dump(plan, file, indent=2, ensure_ascii=False)
        file.write("\n")


if __name__ == "__main__":
    main()
