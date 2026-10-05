# Effective inputs

Read this when a command combines input sources or when the same invocation behaves differently across callers. Keep the result in the existing command contract; no configuration framework is required.

## Separate presence from value

List only sources the command actually supports. Choose a precedence order that fits the established interface. An explicit config file and command-line override may be sufficient. If environment values exist, name the variables, conversion rules, and treatment of an empty value. Avoid silently importing unrelated process configuration.

Retain whether an option was supplied until precedence has been resolved. Apply the default only after deciding which supported source supplies the value. A boolean that is false, a numeric value of zero, and an empty string can all be explicit choices. Validate each according to its meaning rather than falling through to another source. For repeated options, choose replacement, accumulation, or rejection deliberately; do not accidentally inherit different merge rules from two libraries.

Parsing and semantic validation are different jobs. The parser can reject unsupported options and convert simple values. The resolver applies presence, origin, and cross-field rules. The core should receive usable domain values, not repeatedly consult the environment or reinterpret raw tokens while processing records.

For Python 3.12 `argparse`, an omitted option can be represented by an appropriate sentinel or suppressed attribute rather than a domain default. Its ordinary error handling and help are already provided. Complex configuration parsing and file lifecycle management belong after argument parsing: `FileType` can open a file before a later argument is rejected. See the [Python 3.12 argparse reference](https://docs.python.org/3.12/library/argparse.html). These are Python examples, not requirements to replace another language's established parser.

## Preserve the origin of a path

For each path-valued setting, identify both its selected value and its base directory. Derive the base from the source of that value; do not merge raw strings first and then interpret every relative path against one convenient directory. Resolve once before task I/O. Retain enough origin information to explain an error without dumping secrets or the full environment.

Distinguish input lookup paths from display paths if callers rely on a stable representation. Making an internal path absolute need not change a machine-output field that promises a relative name. Decide how stdin, repeated stdin operands, and a filename beginning with an option prefix are expressed only when those uses are supported. Use the parser's operand delimiter instead of writing a second grammar.

Avoid an implicit directory search unless the task needs one. When discovery already exists, retain its documented order and distinguish “no optional config found” from “selected config unreadable or invalid.” Check the chosen runtime's conversion and path behavior before claiming portability.

## Test the choice that could be lost

Use small cases that make two plausible implementations disagree: an explicit valid false-like value overriding a nonempty configured value; the same config invoked from two directories; or a malformed selected file that would otherwise be mistaken for an absent one. Inspect the effective behavior through the command. A resolver unit test can localize the defect but does not show that the public parser actually passed the intended value.

Keep help and version on an informational path. A caller asking for usage should not have to supply readable task data, create an output directory, or accept file truncation.
