# Fictional venue copy

All names, addresses, event details and records in this folder are invented. The `.example` addresses are fixture data, not destinations to contact. No email, upload or cloud-document action is performed.

## Source and audience policy

The request is:

```text
Create a separate plain-text venue brief from source.md for Taylor Reed,
the venue coordinator at taylor@venue.example. Keep the title and the six
lines in Approved logistics exactly. Remove everything else, including
organizer contacts, internal planning, source properties and links.
Save it as venue-copy.txt here and keep a private removal/review record.
Preserve source.md. Do not send or upload anything.
```

This approves the intended audience and the copy/save steps. It does not authorize sending. In a real task, the address and identity would need the applicable recipient evidence before sending; these invented details are not such evidence.

The actual [source](source.md) contains frontmatter, six approved factual lines, contact details, an internal spending ceiling, an HTML comment and a link target with an internal reference. Raw-source inspection matters: a rendered Markdown view can hide the comment and display only the link label. The request uses an exact retained-content list, so a new note inserted under the heading is not automatically permitted.

## Actual output

The new [venue-copy.txt](venue-copy.txt) contains:

```text
Workshop venue brief

Event: Printmaking meetup
Date: 2026-11-07
Time: 10:00-12:00
Attendance: 12 adults
Room: Studio B
Constraint: Use a water-cleanup area.
```

The source was not edited. Removing the organizer section, frontmatter, internal budget, comment and link required building a separate output, not classifying the original as suitable or moving it to a different folder. The water-cleanup constraint remains because omitting it would change what the venue needs to know.

The [review record](review-record.json) binds the checks to the actual source and output bytes. It records removal categories rather than repeating their values. Its audience field is an intended-reader label, and its release state is `prepared_only`.

## Repeat the local check

From this folder, run:

```bash
python3 check_example.py
```

The checker reads the saved files without modifying them. It verifies the fixed approved content, source/output fingerprints, removal coverage, audience and prepared-only status. Its in-memory negative cases try a hidden-style comment, a private link, a missing constraint, a changed attendance number, a changed source, an incorrect output hash, an unknown surface and an unauthorized release claim. Deliberately changing the hash alongside a contaminated output still fails the content check.

This is a bounded text fixture. It does not parse PDF objects, DOCX packages, image metadata, remote permissions or histories. Do not apply its success message to those formats. See [verification.md](verification.md) for the actual observed run and limits.
