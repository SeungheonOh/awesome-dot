# Benny: bounded issue intake

Benny is a dormant two-stage recipe pack: classify an issue report, then reproduce a trusted bug and optionally prepare a verified draft fix. It includes instructions and templates, not a running service or a universally supported scheduler.

Start with [setup intent](FOR_AGENTS.md). The three nested `SKILL.md` files are read directly by a configured runner; they are not added to the plugin's discoverable root skill list.

## What the two stages do

1. **Triage** reads the original thread and attachments, traces likely ownership, deduplicates against a configured tracker, and prepares one concise verdict. Authorized writes stay in that original thread and configured tracker.
2. **Reproduction** trusts only a verdict from the configured triage identity in that thread. It checks human ownership and existing fixes, reproduces the symptom twice through the real app, and verifies a candidate against a pinned baseline. An optional bounded fix may become a draft PR only under explicit standing authority and passing evidence gates.

No source-channel root posts, cross-posts, guessed owners, automatic merges, or production deployments. Workers return findings to the coordinator. Unknown delivery is reconciled before another write.

## Installation and activation are different

Copy this pack to the target repository's `.dot-stack/automations/benny/` after requesting installation. Preserve local edits. Keep user configuration, routing, and feature maps outside the pack, such as `.dot-stack/benny/`. Use the [configuration example](templates/configuration.example.yaml) as a schema-shaped worksheet; its placeholders and disabled settings must be resolved.

A runner needs the committed pack/config revision or another verified immutable distribution. It also needs actual authorized connectors, an execution environment, and the required app-control evidence capabilities. Setup can prepare a reviewable plan when any of these is absent. Enabling a live trigger requires a supported host operation and user authority for its audience, action category, and data. The pack itself grants none.

## Proof before normal traffic

Use the setup skill's synthetic contract tests first, then an explicitly approved harmless integration test. Verify thread coordinates, sender trust, duplicate delivery, missing/deleted parents, uncertain writes, and disabled actions. Keep the installation/activation receipt with runner IDs, configuration digest, checked capabilities, and unresolved limitations. Never describe an untested recipe as live.
