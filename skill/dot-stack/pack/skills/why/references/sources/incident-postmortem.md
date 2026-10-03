# Incident and postmortem angle

Use this angle when null guards, retries, timeouts, rate limits, flags, egress checks, or recovery behavior plausibly responded to an incident. It is not proof that defensive code has an incident-driven origin, and it is not a mandate to search every system for a small question.

Within each selected source, look for a bounded timeline around introduction or revision:

- Code history: revert/reapply sequences, regression tests, linked incident IDs, and recovery changes
- Issues: reliability work, explicit incident follow-ups, reopening, and parent action items
- Documents: full postmortem, timeline, contributing factors, and corrective actions
- Team chat: the relevant incident discussion, decision, and later correction
- Observability: service impact, alert definition, trace/log evidence, and incident chronology
- Error history: matching stack paths, release associations, and new grouping after a fix
- Analytics: user-visible failure rates or retry outcomes, with instrumentation and denominator checks

Follow explicit links rather than matching dates alone. A postmortem action item that names the code change is stronger than several correlated graphs. Distinguish detection, mitigation, root-cause repair, rollout, and later validation. A mitigation can be intentional even when it does not fix the root cause.

Read the postmortem's full relevant context, including amendments. Multiple sources that cite the same incident are not independent causes. Preserve failed mitigation and reverted fixes so the next plan does not repeat them. Do not blame an individual from incomplete operational records.

Return the incident identity, timeline, target connection, exact stated rationale, observed impact, and unresolved alternatives. If only dates align, say the connection is circumstantial. Contacting incident participants or changing production settings requires separate authority.
