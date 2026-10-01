---
name: paper-reading-companion
description: "Build a source-grounded reading guide that separates a paper’s question, method, evidence, limitations, and claims that need external verification."
---

# Paper Reading Companion

Build a source-grounded reading guide that separates a paper’s question, method, evidence, limitations, and claims that need external verification.

## When to use

An engineer wants to understand a technical paper before proposing its method at work. The abstract sounds decisive, but the practical relevance depends on assumptions, evaluation conditions, and the gap between the reported experiment and the team’s setting.

## Required inputs

- An authorized paper file or an exact public paper reference
- The learner’s background and the decision or question motivating the reading
- A target depth and the specific sections or claims that need attention
- Optional supplied supplementary material and a description of the intended application

## Workflow

1. **Verify the paper and readable coverage.** Record title, authors, version or date, page count if available, supplied supplements, and the learner's practical question. Check that the actual text is accessible and identify missing figures, tables, appendices, or damaged extraction. A title or abstract alone supports only a limited abstract review. Ask for missing pages when they contain the evidence needed for the central claim rather than reconstructing their contents.

2. **Plan a question-led reading route.** Match the depth to the learner's background and named question; choose a bounded set of sections rather than claiming comprehensive coverage. Start with the research question and claimed contribution, then route to the method, decisive evidence, and limitations. Introduce only prerequisites needed for those sections. Give each reading stop a question to answer, such as what changed between comparison groups or which assumption makes the argument work. This keeps the guide from becoming a passive section-by-section summary.

3. **Construct a claim-to-evidence record.** For each important claim capture a concise paraphrase, exact locator, supporting experiment or argument, baseline, population or dataset, units, and qualifiers. Separate author interpretation from measurements and your own deductions. Inspect an abstract claim against later qualifications. For reported improvements, preserve the denominator and distinguish absolute from relative changes. Missing uncertainty information remains missing; do not manufacture confidence intervals or significance claims.

4. **Work through one conceptual example.** Use small fictional inputs to explain the mechanism without implying reproduction of the study. Ask the learner to predict a step before revealing its explanation. Include three comprehension questions covering the question being studied, interpretation of evidence, and a boundary on application. Place answers separately and accept justified alternative interpretations when the paper permits them.

5. **Audit practical relevance.** Compare the supplied application context with the study's assumptions, scale, data, and evaluation conditions. List what must be true for the result to matter locally and what evidence is still needed. If a current-literature statement is requested, retrieve appropriate sources during the actual run and record dates; otherwise mark it pending. Do not infer that an uninspected supplement, unavailable codebase, or familiar method validates the paper.

6. **Deliver and verify the companion.** Return the staged route, glossary, evidence map, conceptual exercise, separate answer guide, and uncertainty list. Recheck all central locators against the inspected version and label inaccessible visuals. If the learner answers, tie feedback to their reasoning and request one revised interpretation where useful. Stop before replication, deployment endorsement, or uploading restricted material to another service.

## Deliverables

- A staged reading route appropriate to the supplied background
- A claim-to-evidence map with precise source locators
- A glossary, conceptual example, and three comprehension questions
- A limitations and application-assumptions list with unverified checks marked

## Verification

- The guide identifies the paper version actually inspected
- Each central claim has a locator in available source material
- Abstract claims are checked against later qualifications
- Comparisons preserve denominators, baselines, and evaluation conditions
- Unavailable figures or supplements remain explicit gaps
- A conceptual explanation is not labeled as an executed replication

## Stop and ask

- Supply only papers and supplementary material you are authorized to provide
- Do not upload restricted publications or internal application details to new services
- Current literature claims require actual source retrieval during the run; supplied-paper review alone is not a literature survey

## Response and evidence branches

- **Abstract only:** Produce an abstract-limited question and claim list; ask for methods and results before evaluating evidence strength
- **Inconsistent numbers:** Recalculate from the reported counts, preserve the discrepancy, and ask which source version governs; do not silently repair the paper
- **Wrong learner answer:** Point to the relevant locator and ask for a narrower revision before revealing the full explanation, unless requested
- **Missing learner answer:** Leave comprehension unevaluated and provide a smaller question or the separate key on request
- **Unavailable figure or supplement:** Mark the affected claim unverified; continue with inspectable text without guessing visual details
- **Evidence cannot support the application:** Explain the mismatch in population, task, scale, or outcome; return evidence-needed questions instead of a deployment endorsement

## Worked example

[Read a fictional row-preview study](EXAMPLE.md) provides complete invented source excerpts, checkable denominators, an abstract-to-limitations comparison, and branches for learner errors or missing source material. Its arithmetic checks do not establish real research findings or learner understanding.

## Example request

```text
dot, build a reading companion for [PAPER] for someone with [BACKGROUND] who wants to answer [PRACTICAL QUESTION]. Use the paper and [AUTHORIZED SUPPLEMENTARY MATERIAL]. First confirm which version and sections you can inspect. If the text is unavailable, ask for it or an accessible source; do not reconstruct the paper from its title.

Create a reading route through the research question, central claim, method, evaluation, and limitations. Explain required terms in plain language while preserving their technical meaning. For each important claim, give a section, page, figure, or table locator and separate what the authors report from what the evidence supports in the described setting. Identify assumptions needed to apply the result to [APPLICATION CONTEXT].

Include three comprehension questions, a small conceptual example, and a claim-to-evidence map. Check a claim mentioned in the abstract, a qualification found later in the paper, and a result whose denominator or comparison baseline matters. If a figure or supplement cannot be inspected, say so.

Use concise paraphrases rather than reproducing long passages. Mark any outside-source checks as pending unless actually retrieved and dated. Return the companion and an uncertainty list; do not claim replication, endorse deployment, or upload restricted material elsewhere.
```

## Focused follow-ups

### 1. Read one figure critically

```text
Explain [FIGURE OR TABLE] using its actual labels, comparison groups, units, and uncertainty information. Separate what is visible from interpretation and identify one conclusion it cannot establish.
```

### 2. Trace the strongest claim

```text
Follow the paper’s strongest practical claim back to its experiment or argument. List the assumptions and show how the wording should change if one assumption fails.
```

### 3. Translate to a local question

```text
Compare the paper’s setting with [SANITIZED APPLICATION CONTEXT]. Produce a small list of questions a team would need to answer before testing relevance; do not invent a successful replication.
```

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
