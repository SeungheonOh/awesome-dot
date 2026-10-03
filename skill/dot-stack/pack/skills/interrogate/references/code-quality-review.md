# Structural quality lens

Look for a simpler structure that preserves the required behavior. A worthwhile redesign can delete branches, duplicated state, or empty layers; it should not merely move the same complexity to new files.

## Questions with useful evidence

- Can one domain operation replace callers coordinating several internal stages?
- Does a discriminated union remove invalid optional-field combinations?
- Can an existing canonical utility or policy owner replace a duplicate implementation?
- Does a new parameter expose an implementation detail the caller should not know?
- Are related updates atomic where partial completion is invalid? Is a retry safe after an uncertain result?
- Are independent operations serialized without a reason, or dependent ones parallelized incorrectly?
- Does a silent fallback hide an invariant violation rather than represent an expected failure?
- Does the change make a file difficult to understand because it mixes responsibilities, regardless of line count?

A finding should identify the current maintenance failure and a credible simpler shape. Show representative callers or an invariant that becomes easier to enforce. Estimate the extra migration or test burden qualitatively when it matters. Large files and repeated code are clues, not automatic defects. A local pure function may be better than a reusable framework.

Separate required repair from optional redesign. A speculative future extension does not justify broadening a bug fix. If an ambitious simplification is outside scope, present the bounded follow-up instead of treating it as permission to rewrite the system. Behavior-preserving claims need the relevant tests, including boundary and type checks where applicable.
