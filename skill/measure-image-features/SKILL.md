---
name: measure-image-features
description: Measure counts, sizes, positions or intensity features from authorized images, with explicit regions, calibration and pixel-based verification. Use for quantitative image analysis and its masks or measurement overlays; artistic edits, OCR field extraction, geographic raster analysis and interpreting an already plotted chart have separate primary workflows.
---

# Measure Image Features

Return the requested measurements tied to the actual image features that produced them. A plausible count from a thumbnail, a polished overlay or an unexamined segmentation mask is insufficient. Define the measured feature before treating it as a physical object, semantic category or calibrated quantity.

Use `create-visual-asset` for artistic image creation or editing, and `extract-structured-information` for reading stated fields from documents or pictures. Use `analyze-geospatial-data` when geographic reference systems and spatial support determine the answer. This workflow measures pixels and derived features; it does not establish identity, diagnosis or a physical pass/fail standard from appearance.

## Establish the measurement and image representation

Inspect the actual original at a useful scale, along with the request and supplied calibration. Identify the target population, region of interest, requested measurements, output format and any reference values. A request to measure dark marks does not necessarily include every non-background tone. Ask only when a missing definition would materially change what is measured; continue useful pixel-level work when a physical calibration is unavailable.

Read image dimensions, mode, bit depth, channels, frames and relevant orientation or scale metadata using appropriate installed tools. Distinguish stored samples from a displayed rendering. A screenshot, compressed preview or rescaled copy may have different geometry or values from the source. Preserve the original and identify the exact frame, channel and working representation used.

Choose one coordinate convention and carry it through masks, tables and overlays. State the origin, axis directions and whether positions denote pixel centres, corners or integer index labels. Record crop offsets, rotations, registration and resampling so results can be located in the original. Do not silently apply orientation twice or attach displayed coordinates to stored pixels; the [Pillow orientation helper documentation](https://pillow.readthedocs.io/en/stable/reference/ImageOps.html#PIL.ImageOps.exif_transpose) illustrates an operation that changes the working representation.

Use the supplied region of interest faithfully. Keep excluded area distinct from measured background, and retain a way to reproduce a manual selection. If several regions or frames are compared, ensure their inclusion rules and acquisition conditions are comparable or state the difference. Selecting a favorable crop can change a summary even when every calculation inside it is correct.

## Separate pixels from calibrated quantities

Establish the calibration's source, units and scope. Image DPI, display size and a magnification label alone may not establish specimen spacing. A visible reference can support scale only for an appropriate geometry and plane; perspective, lens distortion or a different depth can make one global factor inappropriate. With insufficient calibration, report supported pixel quantities and the specific missing information instead of inventing physical dimensions.

Keep horizontal and vertical spacing separate when they differ. Pixel count converts to area using both spacings; a horizontal width uses the horizontal spacing. A diagonal or oblique measurement needs the appropriate coordinate transformation, not an arbitrary average scale. Preserve the relation between calibration and any resize or rotation.

Define the measurement's endpoints or support. Bounding-box width, a threshold-crossing width, maximum extent, fitted diameter and contour perimeter answer different questions. Pixel area counts selected pixels; it is not bounding-box area. A perimeter estimator or subpixel interpolation carries its own sampling assumptions. Report those definitions rather than giving unlike measurements the same name.

For intensity measurements, establish the relevant channel and value representation, including any declared scale or offset. Encoded RGB or grayscale values are not automatically linear light, reflectance or another physical quantity. Exposure, illumination, background, alpha and preprocessing can affect comparisons. Apply a supported correction when required and authorized, retaining the uncorrected basis; do not normalize away the difference being investigated or claim calibrated units from an arbitrary image range.

## Choose a reproducible feature rule

Use the simplest method that can express the task's target: an explicit mask, intensity or color rule, edge/profile definition, connected regions, or another justified measurement method. Choose parameters from the source and question, not by tuning until the requested count appears. Keep any manual decisions or development examples visible. Do not impose a learned detector when a transparent local calculation suffices.

For segmentation, specify which pixels are foreground and how unknown or excluded pixels are handled. State connectivity when connected regions are counted; edge-only versus edge-and-corner connections can change the result. The [SciPy connected-component reference](https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.ndimage.label.html) makes that neighborhood choice explicit. A connected region may contain touching objects, and one object may appear in disconnected parts. Do not convert a component count into a real-object count without an additional supported identification or separation method.

Treat cleanup as a measurement change. Smoothing, morphological operations, hole filling, separating touching shapes and removing small regions alter areas, topology or counts. Apply only justified operations, retain their parameters and explain the effect. If small regions are excluded from a summary, preserve their count and measured contribution when relevant. A region-size filter is not evidence that excluded marks were noise.

Keep selection and measurement definitions consistent. If the delivered mask includes small excluded regions while the main table omits them, say so and reconcile both totals. Preserve holes according to the intended foreground definition. Associate every measurement row with a stable label or locator in the selected mask or profile; annotations must not become part of the measured pixels.

## Preserve partial and ambiguous observations

Identify features clipped by the image or analysis boundary, occluded parts and unresolved overlaps. Report observed area or available endpoints as such. Do not infer a missing edge, complete a shape or call visible width the full width merely to fill a table. Exclude partial features from a complete-feature size summary when that is the relevant population, while retaining the observed measurements separately.

Continue quantities that remain supported. A missing outer edge may prevent a full band width while leaving an observed gap to its neighbor measurable. A profile with no detected band is different from a measured zero-width band. Distinguish missing, absent, below detection, clipped and unresolved states where they change interpretation.

For profile or contour measurements, verify the actual samples around each reported crossing or boundary. State interpolation and ambiguity rules, including plateaus or multiple plausible edges when present. Extra decimal places from interpolation do not establish optical resolution or accuracy. Keep rounding out of threshold and inclusion decisions.

Check sensitivity when a reasonable parameter choice could change the answer. A small justified threshold, boundary or background comparison can show whether counts, areas, rankings or clipping status are stable. Keep the chosen result distinct from alternatives, and retain meaningful failures or merges. Agreement among nearby settings is local robustness, not proof of correct segmentation or physical truth.

## Verify saved measurements against the image

Save and reopen the actual table, mask or other requested measurement representation. Check dimensions, orientation, label IDs, value types, units and missing-state encoding. Recompute key values directly from the saved mask or original samples, preferably with an independent calculation for a consequential boundary. Reconcile selected, excluded and partial populations instead of checking only the headline total.

Inspect a source-linked review image or profile plot at a readable size. Confirm that labels match table rows, measured boundaries follow the intended features, holes and clipped portions remain visible, and the overlay has not obscured the evidence. A colorized mask alone may hide a wrong source selection; show enough original context to judge it. An analysis overlay is a scientific annotation, not permission to cosmetically edit protected source content.

Use verification proportional to the request. A few direct pixel/profile checks may be sufficient for a small exact measurement; a broad automated method needs representative cases and explicit limits. A saved-file replay, visual inspection and external physical calibration support different claims. Do not imply an application, instrument or population was validated when only a synthetic or local image was exercised.

Deliver the requested measurements, their definitions and material limitations first. Include masks, overlays and a compact rerunnable method when requested or useful for revision, without requiring a large evidence package for every image. Preserve the source and distinguish a useful pixel-based result from any physical or semantic conclusion still unsupported. Sharing images, using a hosted service or changing source files remains separate unless authorized.
