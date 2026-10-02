---
name: pdf-packet-assembly
description: "Combine explicitly selected pages from several authorized PDFs into a new packet, preserving page content, order, geometry and supported navigation, with source-page lineage and saved-file checks."
---

# Assemble a selected-page PDF packet

Produce the actual new PDF in the requested order, plus a concise page map. Use for meeting packets, application exhibits, instruction bundles and selected appendices. The unit of work is an existing PDF page: this workflow does not add OCR, export an editable document or fill a form. A merge command completing is only the start of verification.

## Make the page instructions unambiguous

Identify the exact source files/revisions, selection, order, intentional repeats or blanks, permitted orientation changes and output destination. Record each original's byte size and SHA-256. Preserve its bytes and use a new output name; refuse an existing destination unless replacement of that exact file is authorized. An authorized local assembly does not need a second approval merely to create its working copy. A new upload, audience or service needs its own authority.

Use one-based physical source page numbers in the page map, alongside printed labels when useful. The PDF's third physical page might display “1,” “iii” or nothing. Expand ranges into individual rows before copying:

| Output page | Source identity | Physical source page | Visible label or purpose | Intended change |
| --- | --- | --- | --- | --- |
| 1 | Notes A, recorded hash | 1 | Setup summary | None |
| 2 | Layout B, recorded hash | 2 | Landscape diagram | None |
| 3 | Notes A, recorded hash | 2 | Intentional blank | None |
| 4 | Notes A, recorded hash | 3 | Equipment appendix | None |

Resolve only gaps that affect the result. “Add pages 2-4” is incomplete when printed and physical numbering disagree; show the matching headings and ask which numbering was intended. “Use the appendix” needs a choice if two source revisions contain one. “Skip the draft” does not establish which similarly named file is final. “Rotate the diagram” needs the desired reading direction if it is not evident. Inspect thumbnails and existing instructions first; do not ask the user to restate information already supplied. Keep ambiguous pages pending and do not present a partial packet as the complete request.

An empty text extract does not authorize dropping a page. A blank may separate sections or control duplex printing. Repeating a page can make internal links ambiguous: record which output occurrence each destination should reach.

## Preflight preservation and navigation

Inspect the catalog and every relevant page before choosing a copying tool. Inventory page count; effective MediaBox, CropBox, BleedBox, TrimBox and ArtBox; rotation and UserUnit; encryption; form-field trees and widgets; signature indicators; embedded files; outlines, named destinations and annotations. Also check for actions, JavaScript, external-file links, page labels, tags, layers and other features the available route may not preserve. Inventory is not signature validation or a complete security audit.

| Finding | Decision before assembly |
| --- | --- |
| Signed or encrypted source | Preserve the original. Establish whether an authorized unsigned derivative is appropriate and how access is permitted. Do not remove signatures, bypass restrictions or imply a copied page retains signature validity |
| Forms, widgets or repeated field names | Establish required interactivity and a tool that preserves the field tree, values and appearances. Page copying can lose fields or combine unrelated names. Do not flatten, rename fields or discard controls merely to merge |
| Links/bookmarks target included pages | Resolve each original target to its output occurrence, including its view/position. Preserve link rectangles and bookmark hierarchy, labels and supported styling |
| A selected page links to an omitted page | Hold that link decision. Ask whether to include the target or explicitly change/remove the link. Do not silently add unrequested pages or leave a stale destination |
| An outline points to an omitted page | Agree which entries to omit or revise; record the disposition. Do not imply the complete original outline survives |
| Attachments, tags, layers, media, actions, unusual destinations or unsupported features | Use a supported preservation route or get a bounded decision about the derivative. Do not silently discard them or launch content to inspect it |

Inspect literal external URI targets without opening them. A URL click is not needed to verify that its annotation survived. Remote-file links may stop working in a new folder; do not reinterpret them as internal links without checking the user's intent. Keep original printed page numbers unless editing them is part of the request; PDF page labels and visible ink are different things.

## Copy pages and remap supported destinations

Use installed, format-aware tooling whose support matches the inventory. Read that version's API documentation. Copy the selected page objects in the explicit order; keep their resources and content streams. Do not rasterize, crop, rescale, optimize or normalize orientation as an incidental merge step. A landscape MediaBox and a portrait page with rotation are different structures even when they look similar.

Build the source-page-to-output-page map before rebuilding navigation. Remap only destinations whose meaning is established. Preserve the target view and clickable area when supported. A tool importing links automatically still requires readback: excluded targets, named destinations, duplicate pages and multiple documents can defeat simple offset arithmetic. If a required feature cannot be preserved, stop the dependent step and identify the exact unsupported item.

Write an isolated candidate and capture the actual tool versions, options and warnings. Keep source identities stable throughout; if a source changes, reconcile the selection against the new revision before proceeding.

## Check the saved packet

Reopen the exact output bytes and reconcile every row of the page map:

1. Confirm exact count, membership, order and intentional repetitions/blanks. Compare source-page text and native content where available; identical text alone cannot establish page identity
2. Compare effective boxes, rotation, UserUnit and orientation. Check any explicitly requested transformation separately
3. Read each retained annotation's target and rectangle and each bookmark destination. Resolve destinations to the expected saved output page and heading. Check form structures and other retained features through their appropriate tools, not screenshots alone
4. Render each selected source page and each saved output page with the same renderer/settings. Compare them and visually inspect every output page at readable size for clipping, missing content, unexpected blank pages and orientation changes. Inspect a deliberate blank as a page, not as an extraction failure
5. Recheck original hashes and record the saved output's size/hash. If the reviewed candidate is copied to a final location, read that saved file back and compare it with the reviewed bytes

Pixel equality in one renderer at one resolution supports that specific comparison. It does not prove all PDF features, accessibility, archival conformance or every viewer's behavior. Test navigation in the intended viewer when available; distinguish an actual click test from structural destination checks. Repair discrepancies within the approved scope and repeat affected checks before calling the packet ready.

Deliver the new PDF, ordered source-page map, checks performed and specific remaining limits. Keep originals available. If assembly or a required check remains blocked, identify the candidate as incomplete and state the smallest decision or capability needed.

## Worked example

The [Pine Room example](example.md) includes original fictional sources, the actual four-page [packet](examples/packet.pdf), a [preview](examples/preview.png), the [page map](examples/page-map.json) and [verification record](examples/verification.md). Its narrow script preserves a true blank and landscape page, remaps one internal link and three flat bookmarks, and catches omitted targets and several deliberately damaged copies. It is an inspectable example, not a general PDF preservation library.
