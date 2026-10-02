# Move the evidence to the real application

Use this packet to identify checks, not to replace the app’s localization system with a new grammar. Success means the actual application loads the saved resource and presents its approved meaning in the supported locales.

## Freeze the consumer and inputs

Record source revision/hash, target locale, resource paths, localization framework/version, runtime locale data where available, and the actual build/load command. Read existing resources and their call sites. Establish whether they use ICU, platform resource files, numbered arguments, rich-text components or another grammar.

Identify where each message appears, what action it qualifies, and the real call argument types. Confirm negation, exceptions, exact tokens, URLs and supplied glossary rules. Hold only the wording whose source meaning is unresolved. Preserve original bytes or an immutable version reference and save the candidate separately.

## Use the framework’s own parser and compiler

Use its installed, existing version and current official documentation. Confirm literal braces, apostrophes, escaping, rich text, plural offsets, exact-number branches and fallback semantics. Do not call the packet’s `{name}` parser “native validation” for an unrelated syntax.

Check keys, argument names/types, branches, metadata and duplicate resource members before a loader can discard them. Preserve unrelated fields. Run the actual compile/build command and record its version, exit status and meaningful diagnostics. Then load the **saved compiled artifact** through the app’s normal localization API. Parsing source and loading compiled output are separate evidence.

If native compilation is unavailable, report that precise boundary and deliver the text candidate; do not substitute a regex result for compatibility.

## Exercise the call sites and fallback

Derive cases from the actual numeric domain. Include 0, 1 and 2, boundary values and every reachable plural category. Before expanding this packet’s integer domain, establish how decimals, negatives, large values, ordinal forms and exact-number overrides should behave.

Pass realistic long names, non-ASCII text, quotation marks, allowed newlines and literal placeholder-looking values. Compare the final return value. Confirm the app treats inserted values as data and escapes them appropriately at the UI boundary. This plain-text consumer does not HTML-escape or validate HTML; its output is not evidence that an HTML sink is handled correctly.

In isolated resource copies, remove a target key and then a required branch. Observe whether the actual consumer fails, returns an ID, selects another target branch, uses a source message, or follows another documented route. Inspect missing-translation diagnostics. Confirm the selected fallback locale also controls plural selection and number formatting where required. Do not leave the corrupted copy installed.

Record requested locale, actual bundle, selected key/branch, final text and fallback reason. Readable fallback is recovery evidence. Missing translations still block a release that requires the requested locale.

## Change the contract independently

The included checker goes beyond matching unchanged fixture strings:

- Tighten the accepted maximum from 1,000,000 to 1; verify 1 still renders and the previously valid 2 now fails
- Rename `name` to `customer` in the contract and both resources; verify the new call works and a stale `name` call fails

Use a corresponding real boundary change: a renamed argument, a newly required branch, a documented bound or an updated resource ID. Test through the actual localization API. This can reveal a checker that merely agrees with fixed expected values.

Also keep a semantic control: remove a negation while leaving valid syntax and length. Reviewers should reject the changed meaning even if tools accept it.

## Inspect the UI and accessible output

Build and open the application through its supported workflow. Visit the relevant screen on its supported device sizes. Trigger zero, singular, plural, loading, error, retry and fallback states. Check:

- The warning stays beside the action and is shown for the intended interval
- Text is not clipped or silently truncated; wrapping, accents, punctuation and fonts remain readable
- Long interpolated values, newlines and help labels fit at the approved sizes and zoom
- Accessible names, focus order and supported assistive-technology output retain the instruction
- Navigation, refresh and language changes load the right resource without stale caching or unexpected fallback

If faithful meaning does not fit, choose approved shorter wording or adjust layout. Do not drop negation or an exception. Save visual evidence only after actually rendering; a text transcript cannot establish pixel layout or native behavior.

## Deliver a scoped result

State the source revision, saved target identity, locale/audience, exact parser/build used, consumer cases, branch coverage, fallback findings, meaning decisions, UI checks, unresolved issues and authorized destination.

Keep “JSON valid”, “framework compiled”, “consumer returned the expected text”, “meaning reviewed” and “screen inspected” separate. Deliver within existing authority: translating and testing do not themselves authorize new recipients, additional data transmission or public publication.
