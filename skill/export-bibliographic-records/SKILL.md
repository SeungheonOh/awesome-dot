---
name: export-bibliographic-records
description: Convert a bounded, authorized metadata review into citation-manager records while preserving identifier and date semantics, disclosing lossy mappings and excluding private reading notes unless requested.
---

# Export bibliographic records

## When to use

A user or agent has a reviewed bibliography and needs a portable reference file for a citation processor. Use when converting provider metadata, a saved research list or an approved catalog. This process does not verify scholarly claims, retrieve full text or publish the user's reading activity.

## Required inputs

- Bounded source records with durable identifiers and explicit lookup outcomes
- Target citation format and, when known, the intended manager or processor
- Provenance and observation time for the original metadata
- Whether annotations, private notes and unresolved rows belong in the output
- Required precision for author names, dates and publication fields

If the destination has not been chosen, a documented intermediate format such as CSL-JSON can be useful. Do not promise compatibility with a specific manager without testing its actual import path.

## Workflow

### 1. Freeze and validate the source

Work from an immutable snapshot. Validate identifier-to-record agreement, field types, record count, text lengths and dates before conversion. Treat imported snapshots as unverified until refreshed from an authorized source; a format conversion must not silently upgrade their trust or freshness.

Distinguish a missing registry result from a globally invalid identifier. Keep unsuccessful rows in the source review even if the target format cannot represent them. Refreshing metadata is a separate network action from exporting what is already present.

### 2. Define an explicit mapping

List supported source-to-target publication types. Use a disclosed generic fallback for an unknown source type, or hold that record when the target lacks an honest representation. Never label an unknown work as a journal article just because that type is common.

Map only supplied fields. Missing volume, issue, pages, publisher or title should remain missing rather than being inferred from an identifier or fabricated for a complete-looking citation. Keep the source review available for provenance and fields outside the mapping.

### 3. Preserve names and date precision

Use structured family/given name fields only when the source actually supplies and retains that structure. Do not split a display string on its last space: particles, institutional authors, mononyms and multi-part names break that shortcut. If only a display string survives, use the target's literal-name representation and disclose sorting/abbreviation limitations.

Represent a year-only date as a year, and a year/month date without an invented day. Validate real calendar dates. Do not substitute the metadata observation time for the publication date or access date without an explicit policy.

### 4. Handle text and identifiers predictably

Use the target format's encoder, preserving Unicode and punctuation. Decide explicitly whether supported inline formatting should be interpreted or kept literal. Do not apply HTML-entity escaping merely because a JSON string contains ampersands or angle brackets: some citation processors print those entities verbatim. Test the intended processor's documented behavior. If exact literal rendering is unavailable, disclose that limitation rather than inventing an escaping convention.

Use stable unique record IDs and reconstruct trusted resolver links from validated identifiers rather than copying arbitrary imported URLs. Deduplicate only under the agreed identifier normalization policy. Do not merge distinct works based on a matching title alone.

### 5. Minimize exported private data

Exclude private reading notes, reading states and unrelated source fields by default. An export intended for citation management does not automatically authorize sharing annotations with that tool. Disclose what is excluded and retain it in the user's separate review artifact where authorized.

A local download does not transmit records to the manager. Uploading, importing into a connected account or publishing the bibliography is a separate action with its own destination and permission requirements.

### 6. Reconcile and verify

Account for every input row: exported unique record, duplicate, unresolved or rejected. Show omitted counts and mapping warnings alongside the download. Validate the target structure against its documented schema when available, then import a small representative fixture into the intended processor if that interaction is authorized.

Test partial dates, literal names, unknown types, missing fields, duplicate identifiers, escaped markup, malicious imported URLs and private-note exclusion. Round-trip comparison should focus on fields the target can preserve; a successful JSON parse alone is not a citation-manager compatibility test.

Invalidate generated output when its inputs change. Keep the download tied to the frozen snapshot, without hidden refreshes or background requests.

## Worked example

A four-row review contains:
- A found DOI record with type journal-article, publication date [2026, 10], author display string "María de la Cruz" and a private reading note
- The same normalized DOI a second time
- A registry miss for another DOI
- An invalid input line

A CSL-JSON export contains one item. Its type maps to article-journal, its issued date-parts are [[2026, 10]], and its author is represented as a literal name because no reliable family/given split was retained. The private note is absent.

The download status says one reference exported and three other input rows omitted. The review artifact still records the duplicate, miss, invalid line, observation time and note. The exporter does not add a publication day, pretend the missing DOI is globally invalid or claim that the reference was imported into a manager.

## Output and limits

Deliver the reference file, a mapping/omission summary and the checks actually performed. State whether manager import and formatted-style rendering were tested. Imported source data remains unverified, and a bibliography export is not evidence that a work is accurate, peer-reviewed or unretracted.

## Reference

[CSL-JSON field and markup documentation](https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html). Consult the intended processor's current schema and import documentation before claiming compatibility.

## Interoperability check: source strings and richer snapshots

A synthetic source title is "A <i>literal</i> & B" and an institutional author is "A & B Research". In citeproc-js 2.4.63 text output, supplying the original title string renders "A literal & B": the supported italic tag affects formatting and its markup disappears. Pre-escaping it as "A &lt;i&gt;literal&lt;/i&gt; &amp; B" instead prints entity syntax in that text output. This observed result is specific to the tested processor and minimal style, not a promise about every manager.

Keep source strings in the review and document the export's formatting policy. Test both personal given/family names and institutional literal names through the actual consumer. Preserve source name components when collecting metadata; when upgrading saved-review formats, accept older display-only names as literal fallback and flag their loss of structure. Reconcile optional structured names with their display representation instead of silently accepting contradictory fields.

The implementation check used a minimal custom CSL style with synthetic records in Node. It did not import into a reference-manager account, exercise all citation styles or establish cross-processor equivalence.
