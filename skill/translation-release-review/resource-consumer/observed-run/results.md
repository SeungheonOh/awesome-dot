# Observed offline consumer run

Node 24.19.0; ICU 78.3; CLDR 48.0; Unicode 17.0.

The saved JSON files passed this consumer’s contract gate. The following sentences and fallback metadata came from executing the consumer. They are not screenshots or proof of native integration. Counts are rendered as plain ungrouped decimal digits.

## Actual output

| Case | Used locale / category | Fallback | Text |
| --- | --- | --- | --- |
| en-US-drafts-0 | en-US / other | none | 0 drafts in Ideas. |
| en-US-drafts-1 | en-US / one | none | 1 draft in Ideas. |
| en-US-drafts-2 | en-US / other | none | 2 drafts in Ideas. |
| en-US-drafts-21 | en-US / other | none | 21 drafts in Ideas. |
| en-US-drafts-1000000 | en-US / other | none | 1000000 drafts in Ideas. |
| fr-FR-drafts-0 | fr-FR / one | none | 0 brouillon dans Idées. |
| fr-FR-drafts-1 | fr-FR / one | none | 1 brouillon dans Idées. |
| fr-FR-drafts-2 | fr-FR / other | none | 2 brouillons dans Idées. |
| fr-FR-drafts-21 | fr-FR / other | none | 21 brouillons dans Idées. |
| fr-FR-drafts-1000000 | fr-FR / many | none | 1000000 brouillons dans Idées. |
| fr-FR-welcome | fr-FR / — | none | Bienvenue dans Brume Notes, Anaïs. |
| fr-FR-saveWarning | fr-FR / — | none | Ne fermez pas Brume Notes pendant l’enregistrement de carnet.txt. Ne réessayez pas, sauf si une erreur s’affiche. |
| fr-FR-closeWarning | fr-FR / — | none | Ne fermez pas. |
| fr-FR-help | fr-FR / — | none | Aide pour Brume Notes : https://help.brume.invalid/guide?lang=en&amp;topic=drafts |
| fr-FR-entryHint | fr-FR / — | none | Saisissez « Idées ». ⏎ Dossier : C:\Brume\Drafts |
| fr-FR-patternHint | fr-FR / — | none | Modèle : {draft} ; valeur : {count} &amp; &lt;nom&gt;. |
| missing-many-recovery | en-US / other | missing-branch | 1000000 drafts in Idées. |
| missing-key-recovery-zero | en-US / other | missing-key | 0 drafts in Idées. |
| missing-bundle-fr-CA | en-US / other | missing-bundle | 0 drafts in Idées. |
| changed-contract-customer | fr-FR / — | none | Bienvenue dans Brume Notes, Zoé. |
| semantic-negative-control | fr-FR / — | none | Fermez. |

The ⏎ marker in the table denotes a real newline; the JSON output preserves it as a JSON escape. The semantic negative control deliberately renders a wrong instruction. It is not part of the French candidate.

## Controls

| Control | Observed result | Detail |
| --- | --- | --- |
| malformed-json-escape | rejected | SyntaxError |
| wrong-resource-kind | rejected | E_STRUCTURE |
| unknown-schema-field | rejected | E_STRUCTURE |
| placeholder-case-change | rejected | E_PLACEHOLDER |
| missing-placeholder | rejected | E_PLACEHOLDER |
| duplicate-placeholder | rejected | E_PLACEHOLDER |
| malformed-opening-brace | rejected | E_GRAMMAR |
| malformed-closing-brace | rejected | E_GRAMMAR |
| unsupported-icu-expression | rejected | E_GRAMMAR |
| url-language-change | rejected | E_EXACT |
| product-token-change | rejected | E_EXACT |
| missing-many-release | rejected | E_BRANCH |
| missing-other-release | rejected | E_BRANCH |
| missing-key-release | rejected | E_KEY |
| unexpected-plural-category | rejected | E_BRANCH |
| short-warning-too-long | rejected | E_LENGTH |
| count-negative | rejected | E_COUNT |
| count-fraction | rejected | E_COUNT |
| count-not-finite | rejected | E_COUNT |
| count-not-a-number | rejected | E_COUNT |
| count-numeric-string | rejected | E_COUNT |
| count-above-bound | rejected | E_COUNT |
| missing-call-argument | rejected | E_ARGUMENTS |
| extra-call-argument | rejected | E_ARGUMENTS |
| wrong-call-type | rejected | E_ARGUMENTS |
| unknown-message-key | rejected | E_KEY |
| incomplete-source-cannot-fallback | rejected | E_KEY |
| malformed-target-cannot-fallback | rejected | E_GRAMMAR |
| invalid-fallback-option-string-false | rejected | E_OPTIONS |
| invalid-fallback-option-null | rejected | E_OPTIONS |
| invalid-fallback-option-number | rejected | E_OPTIONS |
| invalid-fallback-option-undefined | rejected | E_OPTIONS |
| explicit-false-keeps-strict-gate | rejected | E_BRANCH |
| explicit-false-complete-target | accepted | complete target compiled with strict gate enabled |
| fallback-traces | observed | whole-message English fallback; release still blocked for incomplete French |
| changed-contract-rejects-two | rejected | E_COUNT |
| changed-contract-rejects-old-call-site | rejected | E_ARGUMENTS |
| changed-placeholder-contract | accepted | new argument and resources compiled; old call rejected |
| lost-negation | mechanically accepted; meaning review must reject | no semantic guarantee |

## Input identity

| Input | SHA-256 |
| --- | --- |
| source.en-US.json | faa0716bfcedbf34cc8f4f0731d515e03244bb571ba9a4060ed98f06f3914ba7 |
| target.fr-FR.json | b0ccf735a702df40863e88a150674d20050f59303c9cf1d86ceffc6048ac4d1e |
| contract.json | 27292beb63f7a4bc0971ec760024963235f8ea4376d8b16efbf0f26e2e1a639f |
| consumer.mjs | 2a9edddb4e24b7bdb87012c3560bd468ca957708c0657cd9e8f5d3c9b8226152 |
| verify.mjs | 043d1c97dfdcd4a01254cbbaa088d67e6af58e0380478e1240d835c26d2607db |
| json-preflight.py | 93e2aa961fd37581d12e270fa5984e5048397ec904213ed62ebc71357e63ed47 |

All listed inputs were reread at the end and their hashes matched. Fallback output carries a fallback-used release blocker; requested-locale release validity is false for every fallback control. Successful rendering without fallback still does not establish release approval. A successful run does not certify linguistic meaning or UI behavior.

## Not tested

- real framework parser/compiler
- native application integration
- visual layout
- screen-reader behavior
- independent native-speaker approval
