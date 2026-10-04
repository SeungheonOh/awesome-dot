---
name: unslop
description: "Edit requested prose for concrete meaning, natural language, and economy while preserving voice, factual qualifiers, and the required format."
---


# Unslop

Remove formulaic or padded wording from the text being edited. This is a scoped editing aid, not an always-on mode or a replacement for the user's voice and format. Do not alter code, quotations, technical identifiers, legal text, or formal requirements merely to satisfy a stylistic preference.

## Work from meaning

Identify the audience, purpose, claims, uncertainty, and requested tone. Rewrite only what improves comprehension. Compare the result with the original for lost conditions, added promises, altered facts, and erased empathy. A shorter sentence that says something different is not an improvement.

## Patterns worth checking

The numbers are stable reference IDs. They are diagnostic prompts, not forbidden-word rules.

3. Empty “-ing” tails: “highlighting,” “ensuring,” or “showcasing” often add no fact. State the mechanism or remove the tail
5. Vague attribution: replace “experts say” with a supported source, or remove the unsupported claim
7. Inflated vocabulary: prefer a precise ordinary word over decorative “pivotal,” “landscape,” or “delve”
8. Elaborate copulas: “serves as” often means “is”; keep the longer form only when it adds a real distinction
9. Artificial contrasts: state the point rather than “not just X, but Y” when no comparison is needed
10. Forced groups: use the natural number of ideas instead of manufacturing a trio
11. Synonym cycling: keep one name for one concept
12. False ranges: “from X to Y” should describe a real scale or progression, not disguise an arbitrary list
13. Dash-heavy prose: simplify stacked asides; preserve punctuation that genuinely helps the reader or matches the requested style
14. Unnecessary colons: use a normal sentence when the colon adds no structure
15. Excessive emphasis: do not bold every term or heading-like phrase
16. Repetitive labeled bullets: a label should add navigation, not repeat the first words of the sentence
17. Headings: prefer sentence case unless the format or house style requires otherwise
18. Decoration: remove gratuitous emoji or symbols while preserving the intended channel tone
19. Typography: keep quotation style consistent with the destination; do not “normalize” exact source quotations
20. Chatbot filler: remove generic openings and closers that do not answer the user
22. Sycophancy: answer or disagree directly without inflated praise or automatic agreement
23. Filler phrases: “to,” “because,” and a direct claim often replace a long preamble
24. Stacked hedges: reduce redundant uncertainty words, but retain the actual confidence level
25. Generic conclusions: end with a real implication, result, or needed decision
26. Abstract metaphors: replace invented labels with the actual component or mechanism; keep established domain terminology when accurate
27. Mechanism over mood: “the tool returns the executed query” says more than “the query stays close at hand”
28. Dense sentences: split when the reader must backtrack; do not impose a fixed length on every thought
29. Actor clarity: use active voice when the actor matters; passive voice is valid when it does not
30. Unsupported intensifiers: replace “significantly faster” with measured evidence or an appropriately qualified claim
31. Plain words: choose “use,” “help,” and “many” when equally precise
32. Mannered prose: remove rhetorical fragments and personified code when a literal statement is clearer
33. Over-compression: restore articles and verbs; do not turn explanation into cryptic arrows and abbreviations

## Accuracy pass

Check that the revision still names prerequisites, exceptions, risks, and decisions. Preserve epistemic qualifiers such as “the evidence suggests.” Keep sensitive details out of a newly public-facing version. Do not add sources, measurements, or promises to make prose more vivid.

Example: “The migration could potentially improve reliability” becomes “The migration may reduce duplicate writes; that behavior has not been tested.” This rewrite is valid only if duplicate writes and the testing limit were already supported by the supplied context. Otherwise shorten to “The migration may improve reliability” or flag the unsupported claim.

Return the edited text in the requested format. Explain a consequential ambiguity only when the user needs to resolve it. Do not append a performance about how much filler was removed.
