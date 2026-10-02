# Saved-output preservation check

Observed on **2026-10-02** after the successful offline run.

- A second invocation with the existing `observed-run` directory exited nonzero with `EEXIST`
- Both existing result files retained the same SHA-256 digests before and after that attempt
- All six recorded inputs matched the hashes recorded by the successful run
- The source and target message bytes remained unchanged throughout checking
- Every fallback output carries the explicit `fallback-used` release blocker
- The final checker observed 21 outputs and 39 controls, including invalid fallback-option types and explicit boolean behavior

This establishes the tested no-clobber behavior and readback identity. It does not establish application deployment, native rendering or publication.

| Preserved result | SHA-256 |
| --- | --- |
| results.md | f1de409eb8e8c3495009cb31773959d26f9a6ccc3e3b3d2c89bfd733b1df698b |
| consumer-output.json | d18f4a1890b34d4deb3c58b6f95a39749d04ff0746d65f2c609b03818181be4f |
