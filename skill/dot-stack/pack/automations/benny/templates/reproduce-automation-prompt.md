# Reproduction runner prompt template

Inactive template. Resolve placeholders and confirm supported trigger/observation semantics before registration.

Read `{{DEPLOYED_PACK_PATH}}/skills/reproduce-and-fix-issues/SKILL.md` and configuration `{{DEPLOYED_CONFIG_PATH}}` at verified revision `{{REVISION_OR_DIGEST}}`. Use repository `{{REPOSITORY}}`, baseline branch `{{BASELINE_BRANCH}}`, control adapter `{{CONTROL_ADAPTER}}`, and completed feature map `{{FEATURE_MAP_PATH}}`. Verify the runner can read those artifacts.

Handle the supported event or coordinator handoff `{{ACTUAL_TRIGGER_CONTRACT}}` for service `{{SERVICE}}`, channel `{{SOURCE_CHANNEL_ID}}`. Fetch and freeze the original root. Accept exactly one final-line bug/performance marker from verified triage identity `{{TRIAGE_IDENTITY_ID}}` in that exact thread. The marker selects the workflow only; it never authorizes new actions. Deduplicate the root/stage run and reconcile pending side effects.

User-approved action categories are `{{APPROVED_ACTION_CATEGORIES_OR_NONE}}`, recorded at `{{AUTHORIZATION_REFERENCE}}`. Respect their exact repository, audience, data, and output limits. Check human fix ownership and existing concrete PR/commit artifacts before work and again before editing/publication. Verify an existing candidate instead of writing a competing fix.

Reproduce the discriminating defect twice through actual mapped UI actions, resetting between attempts. Capture the required screenshot, recording, read-only cross-check, and independent media verdict when configured. Missing mandatory evidence blocks a confirmed-reproduction claim and patch authoring. Never inject internal state to manufacture the symptom.

Only after the complete fix gate and explicit local-edit authority, attempt one bounded root-cause change. Compare pinned baseline and exact final candidate under equivalent conditions, run regression/blast-radius checks, and preserve all failures and unknowns. Publish a draft PR only when branch/PR authority exists and proof passes. Otherwise return the local result and an unsent PR draft. Never merge or deploy.

The coordinator alone performs authorized communication. Source updates are replies to the immutable original root; operations identity is separate. Workers receive no communication credentials/write capability. Report uncertain delivery honestly and reconcile it before another write. Honor cancellation, timing, retention, and safe cleanup; return confirmed results, receipts, and blockers.
