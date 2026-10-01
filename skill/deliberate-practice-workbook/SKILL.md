---
name: deliberate-practice-workbook
description: "Create a compact workbook that isolates a practical skill, varies the right difficulty, and makes feedback and transfer measurable."
---

# Deliberate Practice Workbook

Create a compact workbook that isolates a practical skill, varies the right difficulty, and makes feedback and transfer measurable.

## When to use

A new engineer wants to improve writing acceptance criteria but keeps doing large tasks without focused feedback. A small workbook can isolate observable behavior, provide increasingly difficult cases, and make it clear what improved after a revision.

## Required inputs

- One practical skill and a concrete work situation where it matters
- Two sanitized examples of current work or a fictional baseline exercise
- A trusted reference or explicit quality criteria
- The output format, desired number of exercises, and whether answers should be hidden until an attempt

## Workflow

1. **Turn the skill into an observable output.** Confirm the work situation, supplied quality criteria, sanitized examples, exercise count, format, and answer-reveal preference. Replace a broad goal such as clearer writing with one inspectable behavior, such as specifying a boundary condition. Ask when the intended standard is genuinely unclear. If examples are missing, create a fictional baseline and identify it as such; do not infer a personal weakness from the absence of work samples.

2. **Select one bottleneck and establish a baseline.** Decompose the skill into a few components and explain which component the first workbook targets. Create a short attempt that can be scored without prior coaching. Specify the input, exact deliverable, permitted aids, and completion boundary. Preserve the learner's original attempt if provided. A baseline measures this attempt under these conditions, not the learner's general ability.

3. **Sequence focused drills.** Design successive exercises that change one named difficulty variable, such as ambiguity, number of constraints, or competing priorities. Keep the remaining conditions stable enough for meaningful comparison. Give every drill a stable identifier, purpose, output shape, and common error pattern. Keep the sequence within the requested exercise count; if prerequisites require more work, propose a smaller first workbook instead of silently expanding it. Put hints and worked responses after the attempt section.

4. **Define feedback before answers.** Build a small rubric with observable anchors for full, partial, and missing success. Cover every required part of the response, including a specified action or requested explanation; an otherwise correct result must not hide a wrong trigger or an omitted transfer explanation. Include acceptable alternative solutions and distinguish harmful omissions from stylistic choices. For each worked response, show where it satisfies the rubric. Create an error log with exercise identifier, evidence from the attempt, error category, revision, and next practice choice. Do not prefill entries with invented learner performance.

5. **Add and inspect a transfer task.** Change the surface context while preserving the skill and comparable complexity. Ensure the learner must apply a principle rather than copy a phrase from the example. Solve the exercises privately enough to detect contradictions, impossible constraints, and ambiguous scoring, then revise the task or explain alternatives. Test the rubric on a partially correct fictional response and an unusual valid approach.

6. **Deliver an attempt-first packet.** Return the workbook, separate hint and answer guide, rubric, and blank error log. State which exercises were checked for solvability and which learner responses remain absent or unevaluated. If actual attempts arrive, cite their evidence and recommend one next drill. Stop when the agreed workbook is complete; enrollment, external submission, recurring practice arrangements, and sharing evaluations require separate instructions.

## Deliverables

- A bounded workbook with baseline, focused drills, and transfer task
- A self-check rubric with partial-success criteria
- A separate hint and answer guide
- An error log template connecting mistakes to the next practice choice

## Verification

- Every exercise has an input, a specific output, and inspectable success criteria
- The drill sequence varies one stated difficulty at a time
- Hints and answers appear after a clear attempt-first boundary
- The transfer task requires applying the skill rather than copying an example
- The rubric handles a partially correct response fairly
- Unattempted exercises remain unevaluated; a wrong answer and a missing answer are handled differently

## Stop and ask

- Use synthetic or authorized examples without confidential work or personal evaluations
- This workbook supports self-practice and does not establish professional certification
- External submission, enrollment, sharing, or recurring reminders require separate instructions

## Response branches

- **Correct answer with sound reasoning:** Cite the demonstrated behavior and move to a changed-context task; do not infer broad mastery
- **Wrong or partly correct answer:** Identify the first mismatch with the stated rule, give one targeted hint, and request a revision before revealing the full worked answer unless the learner asks
- **No answer:** Keep the response and score blank, offer a smaller starting prompt, and retain the exercise as unattempted
- **Several valid approaches:** Score the observable result against the rubric, not similarity to the sample wording
- **Unclear or conflicting source rule:** Pause the dependent exercise and ask for the governing rule; do not grade a guess as the only correct answer

## Worked example

[Quantity-validation practice](EXAMPLE.md) includes fictional inputs, an attempt-first packet, illustrative feedback, and repeatable checks. It demonstrates a narrow artifact-level assessment, not evidence that a learner completed the workbook.

## Example request

```text
dot, create a deliberate-practice workbook for [SKILL] used in [WORK CONTEXT]. Use [AUTHORIZED EXAMPLES OR FICTIONAL BASELINE] and [QUALITY CRITERIA]. I want [EXERCISE COUNT] exercises in [FORMAT]. Keep the first version focused on one observable bottleneck and ask before adding more exercises.

Break the skill into observable components and select the most useful bottleneck to practice first. Include a baseline exercise, focused drills with one changed difficulty at a time, and a transfer task with unfamiliar surface details. Give every exercise a clear input, a requested output, a self-check rubric, and a common failure pattern. Put hints and worked examples after a visible solution boundary so I can attempt the work first.

Use synthetic examples if real materials are incomplete. Check that instructions admit a fair answer, that the rubric can distinguish partial success, and that one edge case cannot be solved by copying the worked example. Do not fabricate my performance or promise proficiency after a fixed number of repetitions.

Return the workbook, a separate answer guide, and a simple error log template. Keep all work private. Do not enroll me in a course, submit work, schedule practice, or share an evaluation.
```

## Focused follow-ups

### 1. Grade one attempt against evidence

```text
Review my attempt, [ATTEMPT], using only the workbook’s stated rubric. Quote the relevant part of my work, identify one priority improvement, and leave unsupported judgments out.
```

### 2. Change one difficulty

```text
Create two new drills that target the same bottleneck while changing only [DIFFICULTY VARIABLE]. Explain what stays fixed so I can compare my attempts fairly.
```

### 3. Review the error pattern

```text
Use these completed error-log entries, [ENTRIES], to identify a recurring issue. Propose the smallest next exercise and distinguish observed patterns from guesses based on a small sample.
```

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
