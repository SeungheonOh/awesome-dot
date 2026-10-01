# Use dot at work without blurring the boundaries

Your organization's approved tools, data-handling requirements and access controls come first. This guide is a planning checklist, not a statement about your company's policy or a substitute for security, legal or compliance advice.

## Before you provide work material

- Check that the account and tool are approved for the type of data involved
- Identify whether the material includes customer information, employee information, credentials, confidential strategy or restricted source code
- Prefer a minimal excerpt, synthetic example or sanitized export when it answers the question
- Remove secrets and unnecessary identifying details; do not assume a filename or chat is private enough
- Know where the output may be stored and who may be able to view it

Sanitization should preserve the behavior being analyzed. Replacing a value with a placeholder may change an error or invalidate a calculation. Say what you changed and which conclusions the sample can support.

## Separate four permissions

| Permission | Example | Does not automatically include |
| --- | --- | --- |
| Read | Inspect a specified repository or document | Editing, sharing or publishing it |
| Draft | Prepare a ticket, patch or message | Sending, committing or posting it |
| Change | Apply an approved edit in a named location | Deploying, merging or expanding access |
| Share | Send an identified artifact to specified recipients | Public release or future unrelated disclosures |

These are practical distinctions, not a complete policy. Some actions require a separate approval or direct user step even when the overall task was requested.

## Connected apps and computers

Ask dot which account, app or computer it will use. An open browser tab does not prove the account is connected, and chatting from a laptop does not by itself grant access to its files. Use the smallest relevant scope. If access is unavailable, ask what can be done from a sanitized sample without treating that sample as full production evidence.

## A safe first engineering task

Start with a read-only explanation, a test plan, a draft ticket or an analysis of a synthetic example. Check whether dot distinguishes source evidence from inference. Expand to edits and execution only when the environment, authority and verification steps are clear.

## Before publishing any output

1. Read the actual artifact, not only its summary
2. Verify names, claims, links and audience
3. Remove unintended confidential or personal material
4. Check asset licenses and attribution when relevant
5. Confirm the exact destination and visibility
6. Record which checks ran and what remains uncertain

## Stop and ask when

- The task would expose information to a new service or audience
- An action would change account access, security settings or credentials
- A result could create a consequential business, legal or financial commitment
- Required policy, permissions or data classification are unclear
- The available evidence cannot support the requested conclusion

A useful assistant can still prepare the safe portion while a decision is pending. It should explain the exact blocked step rather than claiming the entire project is impossible.
