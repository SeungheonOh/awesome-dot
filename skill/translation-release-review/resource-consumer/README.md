# Consume a translated resource before releasing it

This supplement adds an executable resource check to a translation review. Original fictional app messages are saved as English and French JSON, loaded into a small offline consumer, and checked against actual returned text. Start with [the observed run](observed-run/results.md); use [the adaptation guide](adapt-to-real-app.md) for a real application.

**Result:** the supplied candidate passed the stated JSON, contract and consumer checks. It remains a review candidate. Framework compilation, UI rendering and independent linguistic approval were not established here. A deliberately corrupted French warning passed mechanics, making the separate meaning review necessary.

## Brief and files

Brume Notes is a fictional note-taking app. The source is `en-US`; the target is `fr-FR` for customers in France, with formal `vous` in instructions. “Draft” becomes “brouillon”; “folder” becomes “dossier”. Product name, help URL and example path are exact tokens. All messages, names and paths are invented. No real product policy, account or endpoint is being verified.

| File | Purpose |
| --- | --- |
| [source.en-US.json](source.en-US.json) | Frozen English source, seven stable message keys |
| [target.fr-FR.json](target.fr-FR.json) | Saved French resource with locale-specific plural branches |
| [contract.json](contract.json) | Argument types/counts, protected literals, count bound and copy budget |
| [consumer.mjs](consumer.mjs) | Actual plain-text compiler/interpolator using installed `Intl.PluralRules` |
| [json-preflight.py](json-preflight.py) | Independent UTF-8, JSON and duplicate-member preflight |
| [verify.mjs](verify.mjs) | Actual consumer calls, corruptions and changed-contract checks |
| [observed-run/results.md](observed-run/results.md) | Readable output, controls and source hashes |
| [observed-run/consumer-output.json](observed-run/consumer-output.json) | Complete returned output, runtime options and release blockers |
| [linguistic-review.md](linguistic-review.md) | Bilingual meaning decisions and review limits |
| [adapt-to-real-app.md](adapt-to-real-app.md) | Use the real framework parser/compiler and inspect the UI |
| [references.md](references.md) | Current primary API references |

Corruptions are made in memory, never saved over the candidate. Source and target remain separate. SHA-256 hashes identify exact input bytes. Placeholder names and multiplicities are checked by message and branch, not just as a global total.

## Reproduce without replacing evidence

The observed run used existing Node **24.19.0**, ICU **78.3**, CLDR **48.0**, Unicode **17.0** and Python **3.12.14**. There are no packages to install. Use an existing compatible Node with ES modules, `structuredClone`, `Intl.PluralRules` and both locales; the stated version is the tested one.

From this folder:

```sh
python3 json-preflight.py && node verify.mjs run-local-1
```

Choose a new output directory name for each run: 1–64 lowercase letters, digits or hyphens, starting with a letter. The directory is created beside the runner, even from another working directory. An existing directory causes failure before its contents are touched. Result files also use exclusive creation. A failed run may leave a partial directory; inspect it and use a new name after correcting the cause.

Python writes nothing. It rejects duplicate object members, malformed escapes, non-JSON numeric constants and invalid UTF-8. JavaScript parses the saved bytes again and applies the resource contract. The JavaScript step alone does **not** detect duplicate members discarded by parsing.

The run records **21 actual outputs and 39 control observations**, rereads saved results, and confirms unchanged input hashes. The [preservation check](preservation-check.md) records an actual attempt to reuse the result directory and verifies byte-identical existing results afterward.

The scripts never evaluate resource text or interpolated values, open the example link, make network requests, or contact an endpoint.

## The bounded grammar

This is a small documented adapter, not ICU MessageFormat, an HTML engine or an arbitrary framework parser.

1. Parse JSON once. JSON escapes `\n`, `\"` and `\\` decode to newline, quotation mark and backslash before template parsing. [JSON parsing reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse)
2. `{name}` is a named argument: 1–64 ASCII letters/digits/underscores, starting with a letter or underscore, case-sensitive. No whitespace, expression, formatting suffix or nested selector is accepted inside it.
3. `{{` and `}}` produce literal braces. `{{draft}}` renders `{draft}` without requiring an argument named `draft`. A lone or malformed brace fails.
4. Insert arguments as plain data once; never parse their values again. `{count} & <nom>` stays that exact text. Tags and URLs have no special effect here.
5. Text resources contain only `kind: "text"` and `value`. Plurals contain only `kind: "plural"`, `countArgument` and `forms`, whose strings use the same grammar. Unknown fields, keys, kinds or categories fail.

Templates are limited to 4,096 UTF-16 code units; string call values to 200 Unicode code points. Every branch must match its contract’s argument names and multiplicities. Named arguments may change order. Each declared protected literal must occur exactly once in each applicable branch. This checks listed literals; it does not analyze arbitrary added prose or markup.

`closeWarning` has a static 14-code-point budget. `Ne fermez pas.` fits without losing negation. This is neither a pixel width nor a grapheme count, and no text is truncated.

## Category selection and counts

Counts are finite nonnegative safe-integer JavaScript Numbers from **0 to 1,000,000 inclusive**. Strings, fractions, negative numbers, NaN, Infinity and out-of-range values fail before selection. The contract may tighten the maximum: the changed-contract test lowers it to 1 and proves that 2 then fails. `Number.isSafeInteger` supplies the type/integer check; the bound is this adapter’s rule. [Reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/isSafeInteger)

The consumer explicitly requests cardinal rules for each bundle locale. `select()` returns a category, for which the consumer supplies a whole sentence. `resolvedOptions().pluralCategories` supplies the required category set. The strict gate requires all runtime-reported categories, even if a tightened application domain makes some unreachable. [ECMAScript selection](https://tc39.es/ecma402/#sec-intl.pluralrules.prototype.select), [resolved options](https://tc39.es/ecma402/#sec-intl.pluralrules.prototype.resolvedoptions)

| Count | English observation | French observation |
| --- | --- | --- |
| 0 | `other`: 0 drafts in Ideas. | `one`: 0 brouillon dans Idées. |
| 1 | `one`: 1 draft in Ideas. | `one`: 1 brouillon dans Idées. |
| 2 | `other`: 2 drafts in Ideas. | `other`: 2 brouillons dans Idées. |
| 1,000,000 | `other`: 1000000 drafts in Ideas. | `many`: 1000000 brouillons dans Idées. |

These are measured on the recorded runtime. French `one` is a grammatical category, not a numeric equality to 1. French `many` and `other` share wording here but remain distinct branches; copying English branches would omit `many`.

The resolved rule locales are `en` and `fr`; resource identities and intended audiences remain `en-US` and `fr-FR`. Resource locale identities are matched exactly. Count display is ungrouped `String(count)` for transparent checks. Real localized number formatting is a separate integration check. Rerun when locale data, runtime or options change. [MDN overview](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules)

## Fallback is recovery evidence, not release approval

Default compilation rejects missing French keys or required branches. Only diagnostic controls enable `allowIncompleteTarget`. The option, when present, must be an actual boolean: `false` retains strict compilation, and `true` enables the diagnostic mode. Strings such as `"false"`, `null`, numbers and an explicitly supplied `undefined` are rejected; omitting the option uses strict compilation. Present but malformed translations still fail, as does an incomplete English source.

Recovery returns the whole English message and **reselects using English rules**, with `usedLocale`, `category`, `fallback` and `releaseBlockers: ["fallback-used"]`. At 0, a missing French message returns `0 drafts in Idées.` using English `other`, although French would use `one`. The caller’s folder name stays unchanged; the mixed-language output is visible.

An unknown bundle request such as `fr-CA` uses English with `missing-bundle`. It is not an approved French Canadian translation or a language-negotiation hierarchy. Replace this explicit example policy with the real app’s behavior. Every fallback control has false requested-locale release validity. A render without fallback still does not establish linguistic or UI approval.

## Keep four evidence layers separate

| Layer | Established here | Outside this result |
| --- | --- | --- |
| JSON / schema / mechanics | Saved-file parsing, this adapter’s contract, arguments, exact literals and branches | Real framework compilation or semantic equivalence |
| Consumer behavior | Executed text, selection, rejected calls and observable fallback | UI loading, escaping, caching or native mounting |
| Linguistic meaning | Bilingual draft review of seven keys, including negation and exception scope | Independent native-speaker or specialist approval |
| Visual / native integration | Not tested | Layout, clipping, on-screen newlines, focus and accessible output |

The control `Ne fermez pas.` → `Fermez.` fits the budget and has valid structure. It passes mechanics while reversing the instruction. It exists only in memory and labeled diagnostic output; [meaning review](linguistic-review.md) rejects it. A green checker cannot approve that text.

## Independent readback

An independent inspected run reproduced both saved result files exactly, including the 21 returned outputs and 39 control observations. Ten additional cases checked invalid placeholder names, renamed two-occurrence interpolation with literal placeholder-looking values, the 200/201-code-point boundary, required categories outside a tightened count domain, and compiled behavior after callers changed the original inputs. Reusing an existing output directory was refused without changing its files. These checks establish the stated plain-text consumer behavior; the separate bilingual draft review does not establish native-speaker, framework or visual approval.
