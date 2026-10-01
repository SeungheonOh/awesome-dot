---
id: garden-negotiators
title: "Garden Negotiators Strategy Game"
summary: "Create an asymmetric turn-based resource game about negotiating a shared garden plan."
category: web-games
level: advanced
timebox_minutes: 150
capabilities: ["code", "files", "websites"]
tags: ["strategy", "negotiation", "shared-device"]
status: recipe-not-run
---

# Garden Negotiators Strategy Game

Create an asymmetric turn-based resource game about negotiating a shared garden plan.

## Scenario

A neighborhood workshop wants a playful way to discuss competing priorities without using real residents or real budgets. Each fictional gardener has different goals, while everyone shares water and planting space. The facilitator wants meaningful tradeoffs, visible agreements, and a short game that ends predictably.

## Inputs to prepare

- [PLAYER COUNT] from two to four
- [ROUND COUNT] and shared resource limits
- [FICTIONAL ROLE GOALS] and role visibility
- [TRADE RULES] and preferred reading level

## Copy this prompt into dot

```text
dot, design and implement Garden Negotiators as a shared-device turn-based browser game if available tools support it. Use [PLAYER COUNT], [ROUND COUNT], [FICTIONAL ROLE GOALS], and [TRADE RULES]. Start by proposing a small payoff table and an example turn so I can review whether each role has a meaningful path to success.

Players propose planting actions, trade water or seeds, and vote on a shared garden plan. All trades require both players to confirm before resources change. Each round has a finite action allowance. The group succeeds only if the final garden satisfies a public survival threshold; individual role scores are then displayed separately. If the shared threshold fails, explain the unmet conditions instead of assigning blame. Include pass, cancel-proposal, turn summary, and restart controls.

Deliver editable source, fictional role cards, a facilitator guide, and reproducible sample playthroughs showing both group success and failure. Test rejected trades, insufficient resources, tied votes, a player passing every turn, and restart during an unresolved offer. Make public information keyboard-accessible and color-independent. Clearly explain that shared-screen hidden goals are not secure secrets. Use no real neighborhood data, accounts, or behavioral tracking. Keep previews private and ask before publication; identify any balance judgments that remain untested.
```

## Iterate with a purpose

### 1. Audit role balance

```text
Compare several scripted strategies on the same starting resources, then propose bounded rule changes for roles that cannot reasonably contribute.
```

### 2. Add scenario constraints

```text
Add a drought scenario with a public resource reduction and a separate teaching note about how incentives change.
```

### 3. Support facilitated debriefs

```text
Add a local endgame summary of agreed trades and shared outcomes, with optional discussion questions and a clear delete-session action.
```

## Expected deliverables

- Turn-based shared-device prototype
- Fictional role cards and payoff table
- Success and failure sample playthroughs
- Facilitator guide and balance caveats

## Acceptance checks

- A trade changes resources only after both participants confirm
- Rejected or canceled offers leave inventories unchanged
- Insufficient resources prevent an action with a readable explanation
- Tied votes follow one explicit deterministic rule
- The game ends after the configured number of rounds even if every player passes
- Group success and individual scores remain clearly separate
- Restart clears pending trades, votes, inventories, and turn history

## Access, privacy and stop conditions

- The game illustrates tradeoffs and is not a model of actual community preferences
- Shared-device hidden information cannot be treated as confidential
- Human playtesting is required before claiming balanced roles
- Publishing or storing participant data requires separate approval

## Two possible extensions

- Create printable role cards for a browser-free session
- Add an optional rule-variant comparison worksheet
