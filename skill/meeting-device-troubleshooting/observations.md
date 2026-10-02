# Fictional device-check packet

This is original fictional evidence for practicing the workflow. The observations below are supplied reports, not measurements taken on a real computer for this example.

## Request

“People said they couldn't hear me in my last browser meeting. Help me get the headset mic selected correctly and check what we can before the next meeting. You may guide a private pre-join mic meter, speaker test and camera preview, and change the selected devices. Existing permissions are already enabled. Do not record, join, invite anyone or change permissions.”

## Context

- Computer: a personal Windows laptop with a USB dock
- Meeting app: Google Meet in Chrome on the laptop, not a remote desktop; precise versions were not supplied
- Intended microphone and speaker: `USB Headset A`
- Intended camera: `Integrated Camera`
- Another input device is enumerated as `Display Audio Input`
- The last-meeting report does not include a recording or remote participant test from the current session
- No test media, screenshots or personal meeting URL is needed in the handoff

## Supplied observation sequence

The order is explicit; these are separate checks in one session. “User reports” is the basis for every row.

| ID | State and action | Result |
| --- | --- | --- |
| O1 | Inspect system input selection and device list | `USB Headset A` is present and selected for the system input |
| O2 | With the headset unmuted, speak “one two three” and then stop; observe the system input meter | Meter moves during the phrase and falls after speech stops |
| O3 | Inspect Meet's pre-join microphone selection | `Display Audio Input` is selected; microphone control shows unmuted |
| O4 | Speak the same phrase while observing the Meet mic indicator | Indicator does not visibly respond |
| O5 | Inspect the browser's existing permission indicator | Microphone and camera are allowed for this site; no permission was changed |
| O6 | Change only Meet's selected microphone from `Display Audio Input` to `USB Headset A` | The new selected label is visible |
| O7 | Repeat the same phrase, then stop, while observing the Meet indicator | Indicator responds to the phrase and falls afterward |
| O8 | Test Meet's selected speaker, already `USB Headset A` | User hears the test sound through the headset |
| O9 | Inspect the already-authorized preview from `Integrated Camera` and move a hand in view | User reports the preview changes with the movement; no image retained |
| O10 | Close and reopen this pre-join page once, then inspect the microphone and repeat the phrase | `USB Headset A` remains selected and the indicator again responds |

No call was joined, no phrase was recorded or played back, and no remote participant received a test. The packet contains no evidence of speech intelligibility, live-call transmission or long-term stability.

## Later alternative report for a review exercise

This is a separate branch, not a continuation of O10: “After undocking on another day, the headset is not listed in either Windows input devices or Meet. The built-in microphone appears, but I haven't tried it. I want the headset, not a replacement.”

Decide which earlier conclusion still applies and what observation is needed next. Do not reuse O10 as proof about this new device state or silently switch to the built-in microphone.
