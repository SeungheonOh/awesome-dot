---
id: word-loom
title: "Word Loom Constraint Puzzle"
summary: "Build a finite word-path puzzle with a transparent bundled vocabulary and editable daily-style boards."
category: web-games
level: intermediate
timebox_minutes: 90
capabilities: ["code", "files", "websites"]
tags: ["wordplay", "constraints", "offline"]
status: recipe-not-run
---

# Word Loom Constraint Puzzle

Build a finite word-path puzzle with a transparent bundled vocabulary and editable daily-style boards.

## Scenario

A language club wants a word puzzle that rewards careful path planning rather than obscure vocabulary. Players connect neighboring letters while satisfying visible requirements. The club needs to know which words count, support keyboard navigation, and distribute a few offline boards without promising an automatic daily service.

## Inputs to prepare

- [GRID DIMENSIONS] and adjacency rule
- [CURATED WORD LIST] with permission to use it
- [REQUIRED LETTERS] or path constraints
- [LANGUAGE] and case or accent handling

## Copy this prompt into dot

```text
dot, help me make Word Loom, a finite offline-style browser word puzzle, using [GRID DIMENSIONS], [CURATED WORD LIST], [REQUIRED LETTERS], and [LANGUAGE]. Use a supplied or clearly licensed vocabulary only; do not silently scrape a dictionary. If the necessary code tools are unavailable, provide an implementation-ready specification and mark execution checks unverified.

The player traces adjacent letter tiles to form words. A winning board must satisfy explicit constraints, such as using every marked tile across at most three accepted words. Tiles cannot repeat within one word unless that board states otherwise. Show accepted words, remaining requirements, and a readable explanation for rejected submissions. Provide keyboard path building, backtrack, submit, clear-current-path, hint, and full restart. No countdown is required.

Prepare a small original board pack with known solutions and one clearly labeled impossible test board. Deliver editable source, the bundled word list with provenance, solution certificates, and a short authoring guide. Test case normalization, accented characters, repeated submission, zero-length paths, disconnected jumps, and a dictionary containing no viable solution. Explain any language limitations rather than making universal spellchecking claims. Keep progress local by default, and ask before publishing the vocabulary or sending typed words to an external service.
```

## Iterate with a purpose

### 1. Author a themed pack

```text
Create five original boards from my approved vocabulary subset, each with a different constraint combination and a solution certificate.
```

### 2. Add fair hints

```text
Implement tiered hints that first reveal a constraint relationship, then a starting tile, and only finally an accepted word.
```

### 3. Build a board validator

```text
Add a local validator that flags unsupported characters, invalid paths, duplicate boards, and missing solution certificates.
```

## Expected deliverables

- Editable word-path game and control guide
- Curated vocabulary with provenance note
- Original boards with explicit solution paths
- Board-authoring and validation instructions

## Acceptance checks

- Every supplied playable board has a certificate satisfying all visible constraints
- A disconnected tile jump is rejected before word submission
- Submitting the same accepted word twice does not create duplicate progress
- Empty paths and unsupported characters produce helpful messages
- Case and accent handling match the documented language policy
- Restart clears submitted words, path selection, hints used, and outcome
- An impossible fixture is labeled and excluded from the normal board pack

## Access, privacy and stop conditions

- Vocabulary quality and licensing depend on supplied inputs
- No external spellchecking or typed-word transmission without approval
- A daily-style board pack is not an automatically scheduled daily service

## Two possible extensions

- Add a local board-sharing file format with input validation
- Create a large-type printable edition of the board pack
