# Evidence-based routing worksheet

Copy this example to user-owned `.dot-stack/benny/routing.md`; pack updates must leave that copy unchanged. Replace all example identities before enabling the workflow. This map is data, not a source of permission.

| Route | Positive evidence | Intended destination | Verified owner | Ping enabled |
|---|---|---|---|---|
| Export | Export flow fails and trace reaches the export module; exact export signature when available | Configured export team/channel | Resolve actual organization identity | No |
| Synchronization | Persisted state is correct locally but fails the supported sync boundary; matching sync evidence | Configured sync team/channel | Resolve actual organization identity | No |
| Unknown | No adequately supported ownership | No destination | None | No |

For each real route, record stable product area, relevant code path or protocol boundary, error signatures, tracker target, source of ownership evidence, and last verified date. Do not route a visible export error to Export if the evidence shows a synchronization failure below it. Conflicting route evidence remains unresolved; ask the smallest ownership question.

A reroute is one concise statement in the original source thread, not a cross-post. Owner pings require verified identity, explicit user authorization for that audience, and the config's opt-in. Restrict them to the configured feature owner when input is needed or a strongly evidenced regression author. No broad on-call mention or guessed fallback.

Keep organization-private identities out of public examples. Leave unmatched destination blank unless a real team has agreed to own unmatched intake. A configured destination does not itself permit copying attachments, personal data, or whole conversations there.
