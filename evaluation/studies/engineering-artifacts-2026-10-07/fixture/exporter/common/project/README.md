# Inventory selection export fixture

Revision: export-fixture-1. This is a wholly synthetic, dependency-free project.
Run: python -I -B run_tests.py from this directory. The command discovers only
tests/cases.json; the test file is initially absent. No network or accounts.

## Public behavior contract

export_rows(records) returns an object with exactly the key "items". Its value
is a list containing one {"code": ..., "units": ...} object for each input
record. Preserve input order and every duplicate occurrence. A code is a string;
units is an integer or null. An omitted units field becomes null; explicit null
also remains null. Integer zero is a real value. No totals or numeric coercions
are performed. An empty input returns {"items": []}.

download_selected(records) is the public consumer called by the selection screen.
It exports only records whose selected field is true, in their original relative
order. It uses the same payload contract. It must not include unselected records.
export_rows itself does not filter by selected. Inputs in this task are valid;
validation errors and malformed product inputs are outside the behavior scope.

## JSON test format

The top-level object has exactly "version": 1 and "cases": an array of 1..24
cases. Each case has exactly:
- "id": a unique nonempty string of at most 48 characters
- "entry_point": "export_rows" or "download_selected"
- "records": at most 32 records
- "expected": the complete hand-derived output object

Each record has "code" (1..32 characters), "selected" (boolean), and optionally
"units" (integer -1000..1000 or null). Each expected item has exactly "code" and
"units". Expected items is an array of at most 32 such objects. JSON strings may
not contain control characters. No duplicate object keys or non-finite numbers.
The entire artifact must be at most 65,536 UTF-8 bytes. Nesting depth is at most
12. No executable tests, dependencies, expressions, templates, imports, files,
or commands are accepted inside this format.

Example format only, not recommended coverage:
{"version":1,"cases":[{"id":"single-record","entry_point":"export_rows","records":[{"code":"P","units":3,"selected":true}],"expected":{"items":[{"code":"P","units":3}]}}]}
