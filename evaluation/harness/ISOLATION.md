# Isolation requirements

This harness is not a containment system. No candidate execution boundary or untrusted-Python grading boundary is enabled or verified by this repository.

Before a model trial, independently demonstrate that the candidate can access only its task packet, designated treatment files, approved tools, and writable output area. Exclude evaluator answers and controls, other attempts, ambient catalogs and instruction files, live accounts, and unauthorized network destinations. Enumerate the actual runtime's instructions, catalogs, tools, and access paths.

A working directory, ephemeral session flag, sandbox label, separate folder, or ordinary subprocess does not establish those properties. Preserve existing access restrictions. Do not copy credentials, change security settings, or weaken boundaries to force execution.

Candidate descendants must be quiescent before artifact collection. Content hashes and no-follow reads help detect changed or unsafe files; they do not replace operating-system enforcement. Preserve an independent ledger head because a valid suffix deletion cannot be detected from the remaining ledger alone.

Evaluators require a separate reviewed boundary for untrusted output. F8's production-facing grader deliberately does not run submitted Python. Its exact-hash author-fixture API is only for original local control tests. SQL authorizer/resource restrictions are specialized protections, not a general generated-code sandbox.

Blinding also needs enforced reviewer access and independent procedure. A random artifact label and an attestation do not prove independence. Sanitized metric-event retention is insufficient for a positive process-integrity review, so that gate remains pending.

The complete [pretrial checklist](../docs/protocol.md#before-model-trials) includes runtime startup, model/event semantics, timezone data, grader review, protocol freeze, and exact trial authorization. There is no live-dispatch override in this scaffold.
