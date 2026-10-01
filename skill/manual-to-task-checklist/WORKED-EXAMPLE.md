# Worked example: replace an empty label roll

This is a completed source-to-checklist exercise using the [fictional supplied packet](example-source.md). It does not describe an executed physical task or a real printer's instructions.

## Delivered checklist

**Task:** Replace the empty roll with 40 × 25 mm die-cut paper labels

**Applies to:** PebbleTag L20, firmware 2.2, based on the user's supplied device-label and settings observations. This matches D1, *User Guide* revision C, printed page 2. The supplied material covers printed pages 2, 8 and 9; page 12 was not read because it is absent. [M01](example-source.md#m01)

**Readiness:** Ready for the normal replacement path described below. Alignment recovery is unavailable. If either output check fails, stop at that point; the missing page prevents further attempts. All steps remain unchecked. The user has not reported performing them.

### Before starting

- [ ] **P1 — Confirm the roll.** Have the 40 × 25 mm die-cut paper label roll. This procedure excludes continuous rolls and film labels. The supplied package observation meets this requirement. [M02](example-source.md#m02)
- [ ] **P2 — Recheck the starting state.** The display must read Ready and the print queue must contain no jobs. Both were reported in the supplied observations; if either is now false, do not start. [M03](example-source.md#m03)

### Replace and check

- [ ] **C1 — Read the opening warning.** Do not press Feed while the media lid is open. Use fingers only on the green release latch. If the latch or holder is stuck, stop; do not force it or use tools. [M04](example-source.md#m04)
- [ ] **C2 — Remove the empty core.** Lift the media lid, press the green release latch, lift the holder and slide off the empty core. The C1 stop applies if the latch or holder is stuck. [M05](example-source.md#m05)
- [ ] **C3 — Load the roll.** Slide the new roll onto the holder so labels unroll from the bottom toward the front slot, label face upward. [M06](example-source.md#m06)
- [ ] **C4 — Seat and thread.** Seat the holder until it clicks; pass the leading label through the front slot. [M06](example-source.md#m06)
- [ ] **C5 — Guide and close.** Slide the guides against the label edges without curling them. Close the media lid until it clicks. [M07](example-source.md#m07)
- [ ] **C6 — Match the size.** Compare Settings → Media → Size with the roll package. The supplied current setting is 50 × 30 mm, so select **40 × 25 mm**. If the screen already shows 40 × 25 mm when you reach this step, leave it unchanged. Both routes rejoin here: confirm the displayed size equals the package size before C7. [M08](example-source.md#m08)
- [ ] **C7 — Feed once and inspect.** With the lid closed, tap Feed **once**. Continue to C8 only if one blank label reaches the tear line and the display returns to Ready. Otherwise stop: do not press Feed again or change alignment settings. D1 page 12 is required for recovery and is missing. [M09](example-source.md#m09), [M11](example-source.md#m11)
- [ ] **C8 — Print and inspect the sample.** Choose Tools → Print Sample. Check that the entire border fits on one label with no part missing and the display returns to Ready. Otherwise stop: do not press Feed again or change alignment settings; recovery requires the missing page 12. [M10](example-source.md#m10), [M11](example-source.md#m11)

**Done when:** C7 passed and C8 produced a complete border on one label with the display back at Ready. These are expected results, not observations from this exercise. Record the user's actual result before marking the task completed. [M09](example-source.md#m09), [M10](example-source.md#m10)

**Gap:** D1 printed page 12, “Align media.” It is needed only if a Feed or sample check fails. If that happens, obtain that page for the same model and applicable revision before suggesting any recovery action. The normal path has an explicit source-backed stopping point and does not require invented recovery steps.

## Source-to-step coverage review

The denominator is every clause of D1's supplied procedure, including warnings and the failure instruction. D2 is a separate scenario and is not silently discarded from a source set where it is present.

| Source clause | Checklist location | Reviewed requirement |
| --- | --- | --- |
| M01 | Applicability | Exact L20, firmware 2.2 within 2.1–2.3; L20 Plus excluded |
| M02 | P1 | Die-cut paper, allowed size, continuous/film exclusions |
| M03 | P2 | Ready **and** empty queue before starting; otherwise stop |
| M04 | C1, C2 | Warning before lid opening; no Feed with lid open; fingers only; stuck latch/holder stop |
| M05 | C2 | Open lid → latch → lift holder → remove empty core |
| M06 | C3, C4 | Bottom-to-front, face-up orientation → seat until click → thread slot |
| M07 | C5 | Guides touch without curling → lid closes until click |
| M08 | C6 | Different/equal branch; exact package size; confirm before Feed |
| M09 | C7, Done when | Closed lid; one Feed press; label at tear line **and** Ready before sample |
| M10 | C8, Done when | Print Sample; complete border on one label **and** Ready |
| M11 | C7, C8, Gap | Stop at either failed check; no extra Feed/alignment changes; page 12 dependency |

Checklist-to-source review separately checked P1–C8, including each number, menu label, orientation and stop. The source's five actions in M06/M07 were split for readability without changing their relative order. P2 is a recheck of the stated prerequisite, not a claim that the device was inspected.

## Boundary cases

| Input/result | Checklist decision | What resolves it |
| --- | --- | --- |
| Device label says L20 Plus | **Blocked before starting.** D1 explicitly excludes that model; no roll-changing procedure is released as applicable | An L20 Plus procedure matched to the actual firmware |
| L20 firmware reported as “2.x” | **Blocked before starting.** This could include an unsupported release; matching the model alone is insufficient | Exact firmware from Settings → About or another reliable observation |
| Size already 40 × 25 mm at C6 | Leave it unchanged, confirm package match, then rejoin C7 | No question or extra approval needed; M08 defines the branch |
| Label does not reach tear line at C7 | Stop before C8. Do not repeat Feed or invent calibration | Missing D1 page 12; retain this observed failure when obtaining recovery guidance |
| Sample border is clipped at C8 | Task remains incomplete. Stop with no extra Feed or alignment changes | Missing D1 page 12 |
| D2 is added to the source set | **Blocked before starting.** C7 and C8 are held; the normal checklist above becomes a non-executable draft | Applicable authoritative correction or evidence establishing which instruction governs |

For the D2 case, the unresolved conflict is precise: [D1 M09](example-source.md#m09) requires one Feed press and [D2 Q01](example-source.md#q01) requires two, for the same model and firmware range. D2's later date supplies no explicit supersession. Do not average the instructions, choose the newer date automatically, or show C7 as ready while waiting for clarification. Preserve the other source mappings as draft work; no physical steps have been performed.

## Verification record

Run from this skill folder with Python 3 using only the standard library:

```bash
python3 verify_example.py
```

The check reads this folder only and makes no changes. It verifies local file/heading targets, the D1 coverage denominator and reviewed location mapping, all checklist labels, per-step source links, warning/action and prerequisite ordering, unchecked status and the presence of each boundary case. The observed output was:

```text
PASS local links and anchors
PASS D1 coverage and checklist source links
PASS checklist order and unchecked status
PASS boundary-case coverage
```

Observed run: 2026-10-01, Python 3.12.14 on Linux; all four checks passed. Temporary-copy mutations of a coverage location and an added X1 instruction were also rejected. Structural checks cannot decide whether an instruction is semantically supported or whether a real manual is authentic. The clause-by-clause review above supplies the separate content check for this synthetic packet. No hardware, live source retrieval, connected application or physical completion was tested.
