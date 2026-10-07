# Provenance and publication boundary

## Frozen identities

All source identities below use SHA-256. Full private source manifests are not distributed; their hashes bind the locally retained originals, and the public package carries the exact-copy allowlist with source-relative provenance.

- Reviewed author freeze: `6d99b47af3ba852487cd9014dedb6eb5664c49b191397e29cd0641a491ec6f77`, covering 97 files
- Operational freeze: `a8325d847723e7eaad7742aa6f2d7c1819f6695e6a96e6af1c41ddfdc82c43b1`, covering 83 files
- Final outcome lock: `45a3d67fe90b74377e0211de5d5a5c7425d866a377ed04516d6f187b9780f256`, covering 335 files
- Independent AI-assisted case review: `83e793656c7893888e3511f6bf7840ae1cebd8656db4074acb120802099571a2`
- Exact saved aggregate result: `6def369e8bf74222ecafe07a565b6787bf8d4ab6ce433e54ef7c6be5077bbdf7`
- Designated public guide origin: repository `SeungheonOh/dot-skills`, commit `020eebcabf444f18150e912ab44d5d3bde61a16e`

Before packaging, all 335 outcome-lock entries and all author/operational freeze entries were rehashed locally. Each copied public file was checked against its frozen entry. Source, outcome and historical report trees were read only and remain unchanged. No new candidate, primary scoring pass or outcome adjustment was performed.

`evidence/copied-byte-allowlist.json` enumerates every unchanged copy, its byte count and hash, and a logical bundle-relative origin. It contains no absolute machine path. The five designated guide hashes and original Git blob identities are also preserved in `evidence/guide-provenance.json`. Guide bytes are exactly those supplied to S, including guide examples that describe older work; those historical examples are not outcomes from this cohort.

## Source and effective tasks

Both task versions are retained byte-for-byte. The sole intended source-to-effective change is one replacement of “You have 900 seconds.” with “You have 1800 seconds.” in each task; it applies equally to C and S. `evidence/budget-amendment.json` preserves the frozen pre-outcome amendment record and all source/effective hashes. The verifier checks this exact byte replacement. The reviewed author versions are not retrospectively rewritten.

Inputs under `cases/` and designated guide text are fictional/public material. Original captured candidate outputs were scanned and copied unchanged. No output was silently sanitized. Requirement/expected files under `cases/*/scoring/` are authored scoring specifications disclosed after the run; they were not in candidate packets and are not evaluated-agent evidence.

## Public projections

These files are newly authored or selected-field projections and are labeled accordingly:

- `prompts/`: inspectable task/condition descriptions, never historical dispatch transcripts
- `evidence/accounting-projection.json`: saved completion values and all twelve accounting rows
- `evidence/collection-projection.json`: timing, outcome/input facts, output hashes and hashes of excluded private native evidence
- `evidence/dispatch-hash-projection.json`: intended and controller-observed reconstructed prompt hashes, with the imperfect-parity flag
- `evidence/deviation-projection.json`: safe delta, hashes, unknown impact and factual continuation disposition
- `evidence/grading/*/launch-projection.json`: original launch bounds/configuration without command/environment locations
- `evidence/authored-control-summary.json`: saved authored-control and review facts, explicitly non-agent evidence
- Reports, verification code, privacy-check record and package manifest

Raw native final messages, raw operational prompts, private continuation/authorization text, internal coordination boilerplate, agent identifiers, absolute workspace paths and full runtime/parent tool catalogs are excluded. Their omission means this public package cannot reconstruct exact native transport or independently audit all runtime access. Hashes of excluded items are provenance anchors only, not independently verifiable proof of their content.

## Saved-evidence verification and freeze

`verify.py` is portable standard-library code. It does not launch subprocesses, invoke a model, import candidate modules, execute SQL, or replay trusted grading. It rejects changed, missing or extra files against `MANIFEST.json`; symlinks, multiply linked/nonregular files; unsafe relative paths; malformed/duplicate-key/nonfinite JSON; mismatched raw statuses, hashes, denominators and summaries. Bounds are 256 inventory files, 2 MiB per file and 8 MiB total. Verification assumes a trusted, quiescent extraction directory and is not a general sandbox for concurrently attacker-controlled files.

The manifest inventories every package file except itself and records exact bytes and SHA-256 values. Its independently supplied digest is the external identity of the package. No self-authenticating manifest claim is made. The built-in positive/negative self-tests mutate in-memory evidence only. The separate filesystem-control script creates and cleans temporary fictional fixtures inside the package directory. Both remain separate from cohort evidence.

A deterministic ZIP may accompany the package outside its inventory. Its digest identifies the transport container; the manifest identifies unpacked evidence. Neither digest converts observed controller records into atomic generation-time proof, authenticated backend telemetry or an isolation guarantee.
