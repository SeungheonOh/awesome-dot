---
name: photo-selection-caption-review
description: "Select authorized photos for a stated audience and purpose, check factual captions against their sources, and return a selection with privacy and publishing holds."
---

# Select Photos and Review Captions

Produce a small, useful photo selection with grounded captions and an explicit list of anything that prevents sharing. This workflow reviews existing pictures; it does not identify faces, edit pixels, remove metadata, or publish merely because a shortlist is ready.

## Inputs and boundaries

Establish the following from the request and available evidence:

- Purpose, audience, destination and desired number or range of pictures: a private project recap and a public newsletter have different exposure
- The exact authorized album, files or asset IDs, including any exclusions; access to a larger library is not a request to inspect all of it
- Desired coverage, order, aspect ratio and practical constraints such as an existing newsletter layout
- User-supplied context, factual claims and any proposed captions, with a source reference for each
- Evidence about ownership or permitted use, audience clearance, and any restrictions on depicting people, third-party work or private spaces
- Whether the request is to prepare a private review or actually share named files and captions to a specific audience or destination

Ask for missing information only when it changes a decision. If the audience is unknown, prepare a private inventory and ask who will see the result before judging audience eligibility. If the actual photos are unavailable, provide a clearly labeled metadata-only eligibility shortlist; do not call it a visual selection or claim to have inspected it.

Keep these decisions separate:

1. **Authorized access:** may this particular source be read for this task?
2. **Rights and audience clearance:** does supplied evidence support this use and audience? File ownership, upload permission, copyright permission and consent to public exposure are not interchangeable
3. **Authority to publish:** has the user authorized sharing these files, captions and destination? A cleared asset still needs the applicable sharing authority

No one of these establishes the others. Do not infer consent from a smile, attendance, the fact that someone posed, a prior post, or the existence of a file. Treat unknown rights or clearance as a hold; do not present an informal review as legal verification.

## Workflow

### 1. Build the source inventory without changing it

Assign a stable ID to every in-scope original. Record its source link or path, filename, version when available, and whether the original, only a thumbnail, or no pixels can be accessed. Distinguish exact duplicates from similar shots; do not delete either. Preserve originals, source dates, filenames and metadata. If an output manifest needs short labels, store them in the manifest rather than renaming source files.

Match captions, permissions and notes to the exact asset they describe. An album-level statement applies only if its scope is explicit. Similar filenames, adjacent sequence numbers and upload order do not establish a match. When two versions conflict, keep both source references and resolve the conflict before carrying a claim or clearance forward.

### 2. Inspect actual pixels when available

Open the authorized images with an image-capable tool. Use contact sheets to find candidates if helpful, then inspect the actual candidates at a size that supports the decision. A filename, embedding, OCR extract or user description is not pixel inspection. A small thumbnail is partial evidence: it may support composition, but not that tiny text or distant faces are absent.

Assess task-relevant qualities: subject coverage, framing, legibility, blur, exposure, distracting details, repeated views and whether the requested layout would hide essential content. Prefer complementary coverage over near-identical pictures. State a layout concern instead of silently cropping or altering the file.

Record observable privacy concerns such as readable badges, addresses, contact details, screens, vehicle identifiers, reflections or access information. Do not transcribe sensitive identifiers into the deliverable when a concise flag suffices. Inspect location-bearing metadata only through available authorized tools and record what was actually checked. No access to metadata means **unknown**, not absent. Metadata can be stale or copied and is not independent proof of the scene's date or location.

Do not recognize or name people from their faces. Do not infer sensitive traits, personal relationships, intent, emotions or permission from appearance. A supplied identity mapping can support a caption only for its explicitly identified asset and authorized audience; it does not establish consent or justify revealing unrelated details.

### 3. Ground each caption

Separate caption evidence into:

- **Observed:** a plain description supported by inspected pixels, at the available resolution
- **Explicitly supplied:** context provided by the user or an authorized source and matched to this exact photo; retain that attribution in the review record
- **Unverified:** plausible details without adequate support; omit them from the caption or ask a focused question

Use short factual wording suited to the stated audience. Dates, venues, names, causation, awards and completion claims need their own evidence. A source filename or geotag alone does not establish such a claim. Resolve contradictory notes rather than choosing the more vivid story. Drafting engaging text must not introduce a new fact.

For metadata-only work, label captions as provisional text based on supplied notes. Keep **pixels uninspected** alongside each row; do not turn a supplied description into a claim about what you saw. Alternative text, if requested, likewise needs actual visual review before it is finalized as a visual description.

### 4. Make the selection and hold decisions explicit

Apply hard eligibility gates before aesthetic preferences. Exclude an out-of-scope asset or a known audience restriction; hold an unresolved source match, missing clearance or incomplete inspection. Among eligible, inspected assets, choose for the user's purpose. Explain a near-duplicate tradeoff briefly. Do not force the requested count by including unsafe, mismatched or unsupported material.

When pixels are unavailable, shortlist only by supplied coverage notes and known eligibility. This is a provisional work queue, not approval of composition, quality or safety. If none can pass review, return that useful result instead of fabricating a final selection.

Use independent hold reasons so one resolution does not erase another. For example, confirmed public-use permission does not clear an uninspected address label, and a reviewed caption does not authorize publication. A known restriction should remain an exclusion unless new applicable evidence changes it.

### 5. Deliver the review; share only if authorized and ready

Return the selection, proposed order, captions and a hold manifest in the requested private destination. Keep this review useful even if publication is blocked. Do not upload photos to another service merely to make the review easier; follow applicable privacy and file-sharing approvals.

If sharing was explicitly requested, confirm the exact assets or approved export versions, captions, destination, audience and applicable permissions against the final reviewed set. Inspect the actual version to be shared; an original's review does not prove a different export is suitable. Recheck outstanding rights, identifiers and metadata concerns. Share only when required review and approval gates are satisfied, then verify the resulting post or delivery and report the actual status. Preparation alone does not authorize a scheduled post, tag, additional recipient or new public link.

This skill makes no pixel-editing or metadata-removal guarantee. If a candidate needs redaction or another edit, describe the concern and hold that version. Obtain an appropriately prepared version through an authorized workflow, and inspect its actual output before reconsidering release. Do not promise that cropping, screenshots, conversion or a platform upload strips hidden information.

## Output contract

Use one row per in-scope asset with these fields, omitting irrelevant optional fields rather than inventing data:

| Field | What belongs in it |
|---|---|
| Asset and source | Stable ID, exact original/version reference and note references |
| Inspection | Inspected / partially inspected / uninspected, with resolution or access limit |
| Selection | Selected / provisional shortlist / not selected / excluded, plus purpose-specific reason |
| Caption | Draft or final text; each factual claim's matched evidence |
| Clearance | Rights and stated audience status, source and limitations |
| Privacy review | Observed identifiers and metadata status; distinguish reported concerns from observations |
| Holds | Specific unresolved issue and smallest action that would resolve it |
| Release | Authorized destination if any, ready/held status, and actual sharing result only if performed |

Add a short selection rationale and explicit count of final-ready versus provisional assets. “Not selected” describes an editorial choice; “excluded” or “held” describes an eligibility or review problem. Keep these meanings visible.

## Checks and stop conditions

- Every input asset appears exactly once in the manifest, including exclusions
- Every caption claim and clearance record matches the intended asset and version
- No uninspected asset is labeled visually approved, and no absent metadata inspection is labeled clean
- Requested count, factual caption support, audience fit, rights and publication authority are checked independently
- All issues remain attached to the exact file or version that caused them
- Originals remain unchanged; no publishing, editing or metadata-removal claim exceeds actual tool evidence

Stop the dependent sharing step on unresolved identity of an asset, clearance, privacy exposure, unsupported caption facts, destination or authority. Continue the private review of unaffected assets. If access fails, report the precise missing file or inspection capability and ask for the smallest usable input; do not switch to unauthorized sources.

The [metadata-only worked example](example.md) checks exact note matching, a public-audience restriction and independent sharing holds without pretending to inspect real photos.
