# Reviewed authored task-routing regression

Twelve fictional requests, ten complete candidate workflow guides plus the router, and **39 deliberately authored response controls**. Two source-first author reviewers approved all 39 labels after the v2 clarity recheck: 27 adequate and 12 inadequate. These counts describe authored fixtures, not observed model success. **No model trials or scenario executions were run.**

This package tests the contract for choosing an adequate route and next action over the supplied ten-guide slice. It is separate from measured artifact studies and estimates no routing uplift, natural discovery quality, tool performance, or end-to-end task success.

## Read the package

- [Public request packets](public/requests.v1.json), [common instruction](public/common-instruction.md), [observable interface](public/interface.md), and [response schema](public/output-schema.v1.json)
- [Pinned source identities](source-manifest.json) for all eleven full entry points
- [Semantic rubric](author/rubric.v2.json) and [review template](author/semantic-review-template.v2.json)
- [Authored controls](controls/README.md) and [control index](controls/index.v2.json)
- [Methods and limits](METHODS.md), [completed author review](REVIEW.md), and [public provenance](PROVENANCE.md)
- [Public allowlist manifest](MANIFEST.json) and [read-only verifier](verify.py)

R01–R02 cover clear selection; R03 overlapping valid routes; R04–R05 material clarification; R06–R07 bounded no-fit; R08–R10 missing input, capability, or authority with useful partial work; and R11–R12 genuine artifact dependencies. Equivalent ordinary substeps are allowed. More guide names or longer responses do not earn credit.

## Check locally

From the repository root, with standard-library Python 3:

```sh
python -I -B evaluation/contracts/task-routing/verify.py
python -I -B evaluation/contracts/task-routing/verify.py --response evaluation/contracts/task-routing/controls/responses/R09-negative.json --case R09
python -I -B evaluation/test_task_routing_contract_links.py -v
```

The first command verifies the public allowlist, preserved bytes, source anchors, prospective recipe hashes, and all 39 authored response shapes. The second additionally inspects a deliberately inadequate response that still conforms to the interface. **Its semantic adequacy stays null.** The third tests exact copied-guide link exceptions with ordinary local fixtures. The verifier does not launch models, execute scenarios or guide commands, import submitted code, write files, or call the network. It is a separate check, not part of the core evaluation verifier or CI workflow.

For an external freeze check, add `--manifest-sha256` with the independently retained SHA-256 of this package's `MANIFEST.json`. The manifest excludes only itself. A locally consistent set of hashes does not establish execution history or semantic truth.

## Frozen source context

The eleven source guides remain byte-identical to their public [b8fd615 revision](https://github.com/SeungheonOh/dot-skills/tree/b8fd6155afbc87c8c7f237d0e26200644c82847d). Copied entry points retain 34 relative links to context deliberately outside this package. The [omitted-reference map](provenance/omitted-links.json) gives each exact original target, immutable URL, and Git blob. Use those original URLs for context; the linked examples, scripts and artifacts are not supplied inputs or additional candidates. The router's retained `../` link names the copied slice, not a full repository listing.

Source-first author review used procedural separation on a shared filesystem, not OS-enforced blindness. The exact v2 approvals are subsequent to the immutable author freeze; public metadata reflects those approvals without changing any request, interface, source guide, control response, or semantic requirement. See [the projection mapping](provenance/publication-map.json).
