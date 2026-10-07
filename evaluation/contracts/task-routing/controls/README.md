# Authored controls, not model results

[The index](index.v2.json) binds 39 synthetic response files to their case, authored label, and rationale. Every file conforms to the public response shape, including negative controls. Positive and equivalent controls are intended adequate; negatives are intended inadequate. Both source-first author reviewers approved all 39 exact-v2 control labels: 27 adequate and 12 inadequate. The [review projections](../provenance/review-projections.json) identify the original signoffs and their limits.

The checker never uses English keywords, rationale text, or route membership to decide semantic adequacy. Positive and negative controls can have identical allowset diagnostics while differing in an essential contract obligation. A meaningful review must catch errors such as guessed blank-cell semantics, false PDF visual readiness, autosaving disclosure, or stale artifact lineage.

These are public regression fixtures, not model answers. Any future comparison must exclude all controls, rubric, reviews, other cases and prior outputs from model contexts. Directory separation on a shared filesystem is not an access boundary.
