# Fictional archive workshop: caption delivery

**Status: transcript-only caption draft.** The native [SRT](captions.srt) and [WebVTT](captions.vtt) files are ready to try against the matching clip, but there is no media in this example and no synchronization or audio review has occurred. The uncertain date in C03 remains unresolved. This is original fictional source material, not a transcription of a real recording.

## Request and supplied material

> Create SRT and WebVTT for the supplied clip transcript. Use the clip's clock and keep the supplied speaker labels. Use at most two lines, each at most 34 Unicode code points, counting labels, spaces and punctuation. Flag reading speed above 18 code points per second, excluding line breaks. Keep unclear wording and French intact. Return files and a review sheet privately.

The [unchanged source fixture](source-transcript.json) identifies `fictional-sign-photography-clip-r1`, a supplied 36-second excerpt from `fictional-archive-workshop-r1`. Its fictional supplier says the excerpt is contiguous, unedited and at normal speed, beginning at original elapsed time `00:02:17.250`. The original recording and clip are both unavailable. This is a supplied mapping, not an observed edit decision list.

S04 is supplied with separate boundaries for its two sentences, S04.a and S04.b. Those boundaries support C04 and C05; they were not computed from text length. All other cue boundaries are copied from the supplied segment boundaries. Uncaptioned gaps carry no claim about silence. The source describes dialogue only, so sound-caption completeness is unknown.

## Cue-review sheet

The SRT ordinal and the number in each stable `C` identifier correspond in this revision. Times below are elapsed media times, with start inclusive and end exclusive. The caption files contain only the clip-relative intervals.

| Cue | Source span | Clip start–end | Original start–end | Review status |
| --- | --- | --- | --- | --- |
| C01 | S01 | 00:00:00.600–00:00:04.700 | 00:02:17.850–00:02:21.950 | Layout only; accents preserved |
| C02 | S02 | 00:00:05.000–00:00:09.400 | 00:02:22.250–00:02:26.650 | Dropped negation restored from supplied text |
| C03 | S03 | 00:00:09.800–00:00:14.300 | 00:02:27.050–00:02:31.550 | Date reading unresolved; qualification retained |
| C04 | S04.a | 00:00:15.000–00:00:18.500 | 00:02:32.250–00:02:35.750 | Uses supplied first-sentence interval |
| C05 | S04.b | 00:00:18.800–00:00:23.200 | 00:02:36.050–00:02:40.450 | Uses supplied second-sentence interval |
| C06 | S05 | 00:00:23.900–00:00:28.600 | 00:02:41.150–00:02:45.850 | José’s spelling and apostrophe preserved |
| C07 | S06 | 00:00:29.000–00:00:33.800 | 00:02:46.250–00:02:51.050 | French retained without translation |

The clip's full origin/end maps to `00:02:17.250–00:02:53.250`. For example, C02 starts at `5,000 + 137,250 = 142,250 ms`, or `00:02:22.250` in the original. Putting that original time in the clip's caption file would delay the cue incorrectly.

### Review update: C02

An intentionally faulty working draft dropped “not”:

```text
Speaker A: Do crop the date
off the photograph.
```

Comparing it with S02 reveals a reversal of meaning even though the text would fit the layout. The delivered files restore the supplied wording:

```text
Speaker A: Do not crop the date
off the photograph.
```

**Resolved against supplied text.** This is a caption-draft correction, not a correction to the transcript and not an audio-verified finding. No times changed. All other changes are line wrapping and prefixing each cue with its supplied speaker label. The source dialogue is unchanged.

### Open issue: C03

```text
Speaker B: The date reads
[1908/1909?], I think.
```

The bracketed alternatives and “I think” both remain. Neither a format check nor contextual plausibility can choose the year. Next step: request a source-owner wording clarification or inspect the authorized media at clip `00:00:09.800–00:00:14.300`, with surrounding speech as needed, if a suitable audio capability becomes available. A supplied correction must be attributed; it still would not establish that audio was heard.

### Handoff

- Local files: [captions.srt](captions.srt), [captions.vtt](captions.vtt)
- Verified mechanically: source text/order, clip intervals, source-clock arithmetic, equivalent content and this fixture's supplied layout limits; see [the observed check](verification.md)
- Awaiting: resolution of C03 if required for release, synchronization and rendering review against the exact clip and intended player, and any review of sound events needed for the user's captioning purpose

No upload, publication, contact with speakers, recording, playback or audio review was performed. The supplied constraints are an example request, not an accessibility standard.
