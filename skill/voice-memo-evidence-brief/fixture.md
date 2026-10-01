# Fictional clipped transcript

This fixture is invented. No audio file, recording service or real participant was accessed. The timestamps, offset and speaker labels below are supplied scenario data, not acoustically verified measurements. The original recording and recording date are unavailable.

## Source manifest

```json
{
  "source_id": "memo-clip-01",
  "title": "Release memo excerpt, fictional transcript revision 1",
  "input_type": "supplied_transcript",
  "evidence_mode": "transcript_only",
  "audio_available": false,
  "recorded_at": null,
  "recording_timezone": null,
  "original_source_id": "memo-original-01",
  "original_accessible": false,
  "original_duration_ms": null,
  "clip_duration_ms": 84000,
  "timebase": "clip_elapsed_ms",
  "source_offset_ms": 185500,
  "mapping": "single_contiguous_normal_speed",
  "mapping_basis": "supplied_fixture_metadata",
  "speaker_labels": ["Speaker A", "Speaker B"],
  "speaker_identity_verified": false,
  "coverage": "Supplied segments only; gaps and final 3 seconds are unrepresented"
}
```

The original-source span corresponding to this clip is `[03:05.500, 04:29.500)`. This is an offset calculation, not evidence that the original was opened. Segment endpoints are exclusive. The clip is only an excerpt; earlier or later discussion may alter the context.

## Transcript

### S01

```text
00:00.000 --> 00:08.000 | Speaker A
Release memo. I’ll send the customer note tomorrow after the test.
```

### S02

```text
00:08.000 --> 00:17.000 | Speaker A
Correction: I will not send it tomorrow. I’ll prepare a draft for internal review; no customer send is authorized.
```

### S03

```text
00:18.000 --> 00:25.000 | Speaker A
We’ve agreed to keep the rollback switch disabled until the review says otherwise.
```

### S04

```text
00:25.000 --> 00:34.000 | Speaker B
Maybe [Lee/Leigh?] could check the [cache/cash?] figures next Friday.
```

### S05

```text
00:35.000 --> 00:43.000 | Speaker A
Yes to checking those figures. I don’t know who will do it yet.
```

### S06

```text
00:44.000 --> 00:53.000 | Speaker B
I think the launch is approved.
```

### S07

```text
00:54.000 --> 01:02.000 | Speaker A
I have not approved the launch. We still need a review.
```

### S08

```text
01:03.000 --> 01:13.000 | Speaker A
I’ll post the internal draft by next Friday. I mean the draft, not the customer note.
```

### S09

```text
01:14.000 --> 01:21.000 | Speaker B
We could also write a public recap, if that would help.
```
