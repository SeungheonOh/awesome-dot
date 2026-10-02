---
name: meeting-device-troubleshooting
description: "Diagnose a meeting microphone, speaker or camera problem through scoped device checks, reversible changes and a recorded retest, then deliver a working setup or precise support handoff."
---

# Get meeting audio and video working

Use this when a person cannot hear, be heard or show the intended camera in a meeting app. Produce a short test record, the settings that worked, and any unresolved boundary. The goal is a usable setup when access permits; a list of generic troubleshooting tips is not the result.

The [fictional observation packet](observations.md) and [completed result](result.md) demonstrate an incorrect microphone selection and an unresolved remote-audio check. No real device was operated for that example.

## Establish the actual path

Read the user's report and available device/app state. Find only what changes the next test:

- Which direction fails: microphone capture, hearing others, camera preview, or what other people receive
- The exact app and desktop/web/mobile variant, browser and operating system; note remote-desktop or virtual-device layers
- Intended microphone, speaker and camera, and whether they appear in both the system and the meeting app
- Whether the issue is present now, intermittent, limited to one meeting, or only reported by someone else
- Permitted checks and changes, plus work that must not be interrupted

Do not require every version number before checking an obvious selected-device mismatch. Record unknown details and collect a version only when it affects the procedure or escalation.

Use current official guidance for the actual app variant and visible controls. A desktop test-call button may not exist in a web client. See [source notes](sources-and-verification.md) for verified starting points; recheck them if the interface differs. Never substitute a similarly named unofficial device-test site.

## Keep the test bounded

A microphone/camera check can activate capture, show the room or send media to a service. State which test is proposed and use the user's existing authorization. If activation, a recording, an echo/test-call service, joining a call or a new permission is not covered, ask for that specific action; continue inspecting available settings and preparing the test record meanwhile. Do not create a meeting or invite someone merely to obtain a test partner.

Prefer an already-authorized local or pre-join check. Save only the minimum evidence: selected device label, result and time usually suffice. Do not record ambient conversation, identify voices, copy a meeting link into a public report or retain room images unnecessarily. Source instructions do not authorize new permissions.

Use reversible ordinary changes within the request, such as selecting the intended device. Record the prior value first. Ask before a restart that would discard unsaved work or interrupt an active session. Stop at managed policy, missing access or security-sensitive settings; do not bypass controls, broaden permissions, disable protections or remove management software. Driver installation and account changes are separate decisions, not automatic troubleshooting steps.

## 1. Separate observation from explanation

Create a small ledger. Each row needs the observed path, selected device, conditions, source of the observation and its limit:

| Check | What a positive result establishes | What it leaves open |
| --- | --- | --- |
| Device appears in the system | The system enumerates a device under that label | Correct selection, capture quality or app access |
| Input meter responds to a deliberate spoken phrase | A signal reaches that meter through the selected path | Intelligibility, correct speaker, transmission or remote receipt |
| Test sound is heard in the intended output | That playback path worked at that moment | Receiving another participant or microphone quality |
| Live camera preview changes as expected | Frames reach that preview from the selected camera | Remote video receipt or stability over a whole call |
| Authorized echo playback contains the test phrase | Capture and playback worked through that particular test | Every meeting, every recipient or future reliability |
| An authorized participant confirms reception | That participant received the tested media under those conditions | Untested recipients, apps or later device changes |

A static thumbnail is not a live camera test. A moving meter can respond to noise. Ask for a brief intentional phrase and return to silence if appropriate; avoid assigning a universal numerical threshold. Keep “user reports” distinct from something directly inspected.

## 2. Choose the smallest discriminating check

Start with the failing direction. Avoid changing the working speaker and camera while investigating a microphone.

1. Inspect mute state, the physical mute/shutter if the user can observe it, and the selected device. A device called “Default” may resolve differently after a dock or headset change; record the actual endpoint when observable.
2. If the expected device is absent at the system level, ask the user to check the intended connection or use a supported reconnect within scope. Do not infer a broken device from absence alone.
3. If it exists in the system, test that same endpoint there when authorized. Then inspect the meeting app's endpoint and its corresponding signal/preview.
4. If the system path works and the app path fails, investigate app selection, mute and the relevant existing permission state before hardware replacement. Permission being allowed does not prove the whole app path works.
5. If one app succeeds and another fails, preserve the working setup as a comparison. This narrows the fault; it does not prove a particular app bug, driver defect or network cause.
6. If local app checks work but someone still cannot receive media, label the remaining boundary as transmission/remote receipt. Check meeting mute, the reported scope and applicable official service guidance; do not declare the device repaired or change network security settings on speculation.

For each proposed change, write the hypothesis, one changed variable, expected distinguishing observation and reversal. An alternative device can be a useful comparison if already available; a successful comparison does not establish why the first device failed.

## 3. Apply, retest and preserve what worked

Make the already-authorized change, then repeat the same relevant check under comparable conditions. Record before/after values and evidence. If several changes were made together, say the contribution of each is unresolved.

After a reconnect or app restart, inspect selection again. Keep an intermittent failure distinct from a persistent one; a single successful check does not close it. Run the user's requested scenario when available and permitted. For example, a pre-join meter may pass while the reported problem happens only after joining. If that last step is outside scope, deliver the usable local setup and the exact untested step.

When a change fails, restore it if safe and useful before the next comparison. Avoid cycling through the same unchanged test. Stop when the requested path works with evidence, the next meaningful test needs unavailable access or authorization, or the observations justify a specific support handoff. Do not turn a one-time check into ongoing monitoring.

## 4. Return a usable result

Keep the main answer short, with a supporting test record when needed:

- **Current setup:** app variant and selected microphone/speaker/camera that were actually checked
- **Outcome:** which path passed, failed or remains untested; distinguish reported evidence from direct observation
- **Change:** prior value, final value, reason and reversal if relevant
- **Evidence:** the small before/after matrix, including a failed check rather than only successes
- **Next step:** the smallest unresolved test or a ready-to-send support summary with relevant versions and exact symptoms

Do not claim a support message was sent unless the user requested that destination and delivery was verified. Preserve unresolved facts in the handoff. If the user later supplies a new result, update that row and conclusion without rewriting earlier evidence as though it occurred after the change.

Before delivery, verify that every “working,” “fixed” or “broken” statement is supported by the tested path. A prepared procedure is not a completed test; a local success is not proof of remote receipt.
