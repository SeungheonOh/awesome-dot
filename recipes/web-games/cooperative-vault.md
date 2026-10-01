---
id: cooperative-vault
title: "Cooperative Vault Information Game"
summary: "Make a cooperative split-information puzzle playable on a shared device without network accounts."
category: web-games
level: advanced
timebox_minutes: 120
capabilities: ["code", "files", "websites"]
tags: ["cooperative", "information-asymmetry", "puzzles"]
status: recipe-not-run
---

# Cooperative Vault Information Game

Make a cooperative split-information puzzle playable on a shared device without network accounts.

## Scenario

Two friends want a cooperative puzzle where conversation matters more than speed. One sees symbols and the other sees interpretation rules. They will use one device, so the design must explain pass-and-play limitations, prevent accidental reveals where practical, and avoid presenting screen hiding as strong privacy.

## Inputs to prepare

- [ROLE COUNT] fixed at two or expanded to three
- [PUZZLE LENGTH] and number of stages
- [SYMBOL SET] with text equivalents
- [HINT STYLE] and shared-device arrangement

## Copy this prompt into dot

```text
dot, build Cooperative Vault, a finite split-information puzzle for [ROLE COUNT] players, using [PUZZLE LENGTH], [SYMBOL SET], and [HINT STYLE]. If code and browser tools are available, implement a shared-device version first. Do not add online multiplayer or accounts unless I request them separately.

Give one role a panel of symbols and another a rulebook that maps relationships to a code. Players must describe what they see and agree on a submission. Include explicit role-switch cover screens and a shared final-entry screen. Explain that this prevents casual accidental reveals only; it is not secure separation of secrets on one device. All symbols need stable text names, keyboard navigation, and large readable labels.

A correct code advances the stage; completing every stage wins. An incorrect code identifies the stage, consumes a configurable attempt, and offers a hint. Exhausted attempts end the session with retry and reset options. Deliver source, original puzzle data, role sheets, and complete solution walkthroughs. Check repeated symbols, contradictory-rule fixtures, exhausted attempts, role switching after submission, and restart from the final stage. Keep answer data out of the default visible interface, while acknowledging it exists in local source. Ask before publishing or adding remote communication, and report verification limits plainly.
```

## Iterate with a purpose

### 1. Add a printable companion

```text
Generate printable role sheets from the same puzzle data so players can compare a paper-and-screen setup with pass-and-play.
```

### 2. Improve hint fairness

```text
Add graduated hints that expose one relationship at a time and track hint use separately from attempts.
```

### 3. Create a puzzle authoring check

```text
Add a local validator for missing symbol names, contradictory rules, unsupported codes, and stages with multiple valid answers.
```

## Expected deliverables

- Shared-device cooperative puzzle source
- Original staged puzzle data and solutions
- Role-switch and accessibility guide
- Printable-ready role-sheet content
- Attempt-limit and reset verification checklist

## Acceptance checks

- Correct codes advance exactly one stage and the final stage produces a win
- Incorrect submissions consume the documented number of attempts
- Exhausted attempts show a clear terminal state with working reset
- Role switching does not erase current valid progress or reveal the other role by default
- Repeated symbol names remain unambiguous in both roles
- Contradictory fixtures are rejected during puzzle validation
- Full reset clears codes, attempts, hints, role selection, and stage progress

## Access, privacy and stop conditions

- Cover screens do not provide secure confidentiality on a shared device
- Browser source can expose puzzle answers to a determined player
- Remote multiplayer, accounts, publication, and communication integrations need separate approval

## Two possible extensions

- Add a facilitator view for an approved in-person workshop
- Create a three-role puzzle with a separately verified information dependency
