---
name: build-2d-scene-component
description: Build or maintain a programmatic 2D scene component whose editable source, native geometry queries, accepted edits and saved rendering agree. Use for scene-component software, not ordinary artwork, diagrams, charts or export inspection alone.
---

# Build a 2D scene component

Make a caller able to identify, change and save the same drawing objects with consistent meaning. Start from the actual source format, public caller and requested outputs. For maintenance, trace the affected existing path before changing it. Keep the supported shapes and operations as small as the task allows.

Use a suitable scene, geometry and rendering facility already available in the project. Let its paths, transforms, shape queries and renderer own the mechanics they support. Check the actual library version and backend; documentation alone does not establish installed capability. A GUI, custom geometry engine, spatial index, history system or second renderer is not a prerequisite.

## Keep source meaning separate from native presentation

Identify the authoritative editable state and its ownership. Preserve the identities, parent relationships, logical order, local geometry, styles and other source fields that the contract retains. A source ID can differ from both a display name and a native object handle. Keep the mapping explicit so rebuilding artists does not change which source object a query or edit identifies.

Define how source order becomes native paint order, including group traversal and ties where relevant. Do not let per-class drawing defaults accidentally reorder a mixed collection. Keep derived artists, views and query results from becoming independently editable copies of the document. Protect accepted state from unintended mutation through caller-owned inputs or returned data using the project's existing ownership approach.

## Establish the coordinate and selection contract

Name the frames that actually cross the interface: object-local, parent/document, view/display and exported-image or page coordinates. State their units, origin, axis direction and the frame of returned bounds. Distinguish continuous image coordinates from integer pixel samples when the caller depends on that choice.

Trace the actual composition from local geometry through parent placement to document and output mapping. Include the relevant crop, viewport, aspect fitting, padding and resolution. Use native mapping and inverse transforms where supported; do not assume that similarly named coordinates coincide. Check composition order with a simple known placement. Matplotlib, for example, uses different display units for Agg and SVG/PDF, and changing a view can change its data-to-display mapping. These are library-specific facts, not a universal pixel convention. See its [transform documentation](https://matplotlib.org/3.10.8/users/explain/artists/transforms_tutorial.html). Qt provides its own [item, scene and view mappings](https://doc.qt.io/qt-6/graphicsview.html#the-graphics-view-coordinate-system).

Choose what a query means for this caller:

- Which objects are eligible, including the relevant effects of visibility, transparency, clipping, groups and non-filled objects
- Whether it tests a fill, stroke, bounding envelope or rendered pixels, and whether it returns one object or several in a declared order
- What bounds include, which frame they use, and how any tolerance or boundary ambiguity is handled

Use the native operation matching that meaning and map its result to source identity. A bounding envelope can include points outside a shape; painted strokes and antialiasing can extend beyond a fill. Clipping or a visual effect may change visible pixels without changing the underlying path. Do not substitute one of these results for another. Check the selected API's exact limits: Matplotlib's [path containment](https://matplotlib.org/3.10.8/api/path_api.html#matplotlib.path.Path.contains_point), for example, leaves exact-boundary results undefined. Add a boundary policy only when the application needs one.

## Carry changes through the complete path

Distinguish a source edit from a view-only change. Validate an edit at the established acceptance boundary, change the intended source object, and update or rebuild the native representation through supported APIs. Preserve unrelated source meaning and order. If native geometry changes require notifications, follow that facility's contract so later queries and rendering see the update. Keep rejection behavior consistent with the caller's promise.

For relevant zoom, viewport or export-size changes, update the affected coordinate mapping and derived state. Honor the accepted stroke and text semantics: document-scaled widths, fixed physical points and fixed display sizes can require different handling. Inspect how the chosen library applies transforms to geometry, outlines and text instead of multiplying every property by one scale. Keep view-only changes from rewriting source geometry unless the document contract calls for it.

Save genuine editable source when requested. Bind queries and exports to the accepted source state and the mapping for the requested output. If exporting temporarily changes native state, ensure subsequent queries still use the intended frame. Reopen saved source and exercise its public read/query/export path when persistence is part of the component's promise. A rendered SVG is not automatically a round-trip document format.

Choose explicit export extent and sizing rather than inheriting incidental preview layout. For SVG, verify how dimensions, viewBox and aspect handling produce the output mapping; the [SVG viewport rules](https://www.w3.org/TR/SVG2/coords.html#ComputingAViewportsTransform) define their relationship. Preserve the task's existing overwrite and failure policy, and report save/export failure truthfully. Do not impose a new file-refusal mechanism or transaction scheme on a task that does not need it.

## Verify shared meaning and the saved result

Select a few source-grounded cases that distinguish the requested behavior from a plausible wrong frame, order or stale revision. Derive expected positions, identities or dimensions independently of the helper being tested. Simple source geometry, a known placement or an established caller can supply useful checks without a second production geometry implementation.

Exercise the actual public path before and after the accepted edit, and after a relevant view change or reload when those behaviors are in scope. Check the changed object and a meaningful unaffected object. An overlap can distinguish stacking; a point inside an envelope but outside its fill can distinguish query semantics. Choose cases for the contract rather than requiring every shape, frame and boundary combination.

Inspect the actual saved visible artifact for the requested placement, scale, clipping, strokes and text. Check consequential source and file properties separately, such as retained identities, dimensions or vector content. A successful save or parse cannot establish appearance. Use an independent renderer when required for interoperability or export fidelity; identify that evidence separately from the native saved rendering.

Deliver the working component, requested source and outputs, useful invocation, and the material coordinate/query choices. State which public API, caller, save/reload and visual checks ran. Native artifact inspection does not prove GUI interaction, independent-render compatibility or physical output. Keep those claims tied to what was actually exercised.
