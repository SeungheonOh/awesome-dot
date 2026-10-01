# Local example checks

## Scope

This is an executed transcript-only fixture check using Python's standard library on Linux. The fixture and expected brief are fictional. No audio capability, speech-recognition system, recording account, network access, package installation or external action was used.

Run from this folder:

```sh
python3 --version
python3 check_example.py
```

## What the check establishes

- The example's nine segment IDs, supplied labels, exact text and clip timestamps match the fixture
- Each original-source interval equals its clip interval plus 185,500 ms; the 84-second clip ends at original time 04:29.500
- Clip bounds, segment order, source revision, claim references, local links and the brief's displayed source ranges are consistent
- The fixture's retracted customer-send action stays out of current work; ambiguous wording and unresolved owner/date fields remain visible
- The modeled gaps total 9,000 ms, including the final 3,000 ms; they are not called silence
- Six corrupted copies are rejected: wrong offset, dropped negation, wrong source, revived retracted action, invented deadline and unsupported audio-review claim

The checks compare authored records and specific expected fixture states. They do not infer meaning from arbitrary speech, validate the supplied transcript against audio, establish a speaker's identity/authority, test an edited or retimed source, or establish access to a real recording. The clip offset itself is supplied fictional metadata, not independently verified.

## Observed result

Recorded after running the commands against the final example; the output below is a local consistency result only.

```text
Python 3.12.14
PASS: 9 segments, 9 claims, 2 current actions
PASS: source/quote/time checks, 15 local links, brief citation ranges
PASS: 9000 ms unrepresented; expected unresolved-date fields preserved
PASS: 6 intentionally corrupted copies rejected
LIMIT: no audio, transcription, speaker identification or external action tested
```
