# Add regression-oriented behavior tests

We maintain a small inventory-selection exporter. Add tests that give the team
confidence in its observable behavior. Use the documented contract and public
consumer, inspect the supplied implementation, and choose examples that would
catch realistic mistakes without locking in private implementation details.

Your only deliverable is project/tests/cases.json, following the existing JSON
format in project/README.md. Do not change product code, runner, schema, or other
files. The runner uses only Python's standard library. You may run it if tools
are available; report execution honestly. Return no additional deliverable.
