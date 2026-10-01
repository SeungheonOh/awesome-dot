# Observed verification

## Run

Executed on 2026-10-01 with Python 3.12.14 on Linux, using only the Python standard library. No additional software was installed. The check reads these local fixture files and makes no network requests:

```bash
python3 check_example.py
```

Observed exit status: `0`.

```text
PASS: exact saved copy, original fingerprint, retained facts, record and release boundary
PASS: rejected comment leak
PASS: rejected link-target leak
PASS: rejected lost constraint
PASS: rejected changed attendance
PASS: rejected invisible character
PASS: rejected source drift
PASS: rejected wrong final hash
PASS: rejected unknown output surface
PASS: rejected unauthorized release claim
PASS: 9 negative cases; all saved fixtures unchanged
LIMIT: text bytes only; no PDF, Office, image or provider-history verification
```

## What this establishes

- The saved 158-byte `venue-copy.txt` was read back and matches the exact approved title and all six factual lines, including the cleanup constraint
- The saved 532-byte `source.md` matches its frozen fingerprint; the checker also confirms that all three input fixtures are unchanged after its run
- The source's frontmatter, contact section, internal planning, HTML comment and link are not included in the new output; the full-byte comparison catches unexpected content even when its recorded hash is updated to match
- The record identifies the intended audience, binds its checks to the final output hash, preserves uncertainty about metadata outside the file bytes and reports preparation only
- Negative cases run only in memory; they do not create contaminated files or change the committed example

The main guide and example were read for scope and permission boundaries. Record locators, retained-content rows and the meaning of each hold were manually checked against the source and policy; the script validates selected record fields, not every assertion in that record. Local Markdown links were checked against existing files. Official Microsoft and Adobe references in the guide were opened on 2026-10-01 to support the specific inspection, sanitization and cropping cautions.

## What this does not establish

This fixture does not test PDF redaction, Office revision removal, hidden binary objects, image pixels, OCR, embedded metadata, file-system attributes, cloud-document histories or remote access. No live recipient was resolved and nothing was sent, uploaded or shared. The invented reader and source policy do not grant authority for a real file.

The fixed expected text and hashes make this a reproducible regression example, not a general sanitizer. They are not a malicious-tampering defense: someone who changes the policy, expected values and record together can change what the test accepts. A real run needs its own approved content map, original-preservation evidence, supported format inspections and final delivery checks.

The broader workflow's format branches remain to be executed against actual authorized documents with suitable tools. Until relevant hidden content can be checked, the affected copy must remain held for sharing. An unchanged source is preserved for the user; this process does not erase its contents from original storage, backups or other people's copies.
