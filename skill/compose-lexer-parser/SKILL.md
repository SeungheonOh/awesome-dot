---
name: compose-lexer-parser
description: Connect an ordered lexical specification to a token-based parser while preserving longest-match rules, priority, source spans and separate failure evidence. Use when turning raw text into a declared grammar's token stream or diagnosing lexer/parser boundary errors.
---

# Compose a lexer and parser

## When to use

Use when a parser already accepts terminal labels but the actual input is source text. The useful output is a traceable pipeline from source spans to token names to parser actions. Do not silently treat literal source characters, token categories and grammar nonterminals as interchangeable.

## Required inputs

- Ordered lexical rules with token names and literal or pattern definitions
- Declared pattern dialect, character domain and treatment of whitespace/comments
- Token-based grammar, start symbol and parser strategy
- Source input, offset units and work/output bounds

Ask for a missing priority or skipping policy when it belongs to an existing language. For an exploratory tool, choose and label a bounded policy explicitly. A convenient policy does not establish compatibility with a real language implementation.

## Workflow

### 1. Validate both sides of the boundary

Identify grammar nonterminals and terminal labels. Check that lexical token names have an intended role on the parser side. A rule named `number` may match `123`; the parser consumes the name `number`, while diagnostics retain `123` as its lexeme.

State the pattern dialect precisely. A restricted finite-automaton syntax is not JavaScript, PCRE or a Unicode regular-expression standard. Reject unsupported operators rather than approximating them. Do not execute user-authored semantic actions as host-language code merely to produce a token.

### 2. Establish progress before scanning

Reject lexical rules that accept an empty string unless a separately designed protocol defines how they advance. An empty match can cause a loop or make token boundaries ambiguous. Require nonempty literal rules and bound the number and size of rules.

Define whether ignored whitespace is handled before matching or through ordinary lexical rules. Under a pre-skip policy, those characters cannot be part of a matched token. Do not quietly discard an unknown character: report its exact position and stop complete-tokenization claims.

### 3. Choose longest match before priority

At the current position, evaluate each rule as an anchored prefix matcher and retain its longest accepted prefix. Choose the greatest consumed length across all rules; use declared rule order only to break an equal-length tie. Selecting the first rule that matches anything implements a different lexer.

Record token name, original lexeme, half-open source span and selected rule identity. Keep competing equal-length matches as evidence when useful. Rule-order changes can alter classification without altering token length, so treat them as semantic changes.

A straightforward NFA scanner can have substantial repeated-prefix work. Bound source length, emitted tokens and active-state work, and label a limit as incomplete rather than silently returning a valid-looking prefix. Do not claim linear time merely because a finite automaton is involved.

### 4. Preserve the position contract

Choose byte offsets, Unicode code points, UTF-16 code units or another explicit unit and use it consistently. Do not label JavaScript string indices as byte positions. Preserve the original lexeme rather than normalizing case or Unicode unless that normalization is part of the language contract.

Keep skipped-character accounting separate from emitted token spans. Token indices are not source offsets, especially after whitespace is removed or a multi-character literal becomes one token.

### 5. Feed names into the parser, retain evidence beside it

Pass the selected token names to the parser and preserve the lexical ledger for diagnostics. Do not replace a token with its lexeme unless the grammar explicitly expects that literal. Keep lexical failure, parser-table conflict, syntactic rejection and resource exhaustion distinguishable.

If the parser cannot choose deterministically from its table, report that conflict rather than guessing. A successful lexer run does not prove syntactic validity; a successful parse does not prove semantic correctness or successful execution.

When source, rule order, dialect, input mode or grammar changes, invalidate the dependent ledger and parse trace. If exporting reproducible evidence, include the declared rules and policy along with token names/spans and parser results. Lexemes may contain private input; a token trace is not automatically sanitized.

### 6. Verify the composition independently

Test keyword-versus-identifier overlap, a longer identifier beginning with a keyword, zero-length patterns, unmatched punctuation, end-of-input, skipped whitespace and a multi-code-unit literal. Confirm that ties change with rule priority but a longer match still wins.

For bounded fixtures, independently enumerate every nonempty prefix at each position, test complete-prefix membership, sort accepted candidates by descending length then priority, and compare the entire token ledger. Keep this exhaustive oracle small; testing a few prefixes is not proof of complete tokenization for arbitrary input.

## Worked example

Declare rule 1 as literal `if` producing IF, and rule 2 as pattern `(i|f|x)+` producing ID. On `if ifx`, the first span matches both rules at length two, so rule 1 emits IF. After skipping one space, the second span matches rule 2 at length three; it emits ID even though rule 1 matches its first two characters. The spans are [0,2) and [3,6).

For an expression grammar expecting `number + ( number )`, lexical rules for decimal digits, plus and parentheses can turn `12 + (3)` into those token labels while retaining lexemes `12`, `+`, `(`, `3`, `)`. Passing raw `12` directly to that parser would incorrectly conflate a value with its token category.

A literal emoji followed by `x` occupies UTF-16 spans [0,2) and [2,3), illustrating why offset units must accompany the report.

## Reference and evidence

This workflow was exercised with 400 small exhaustive-prefix oracle comparisons, priority/keyword examples, Unicode literal spans and UI invalidation tests. See [Cornell's lexical-analysis implementation notes](https://www.cs.cornell.edu/courses/cs4120/2022sp/notes.html?id=leximpl) for longest-match and priority semantics. These tests do not establish compatibility with another language's lexer dialect.
