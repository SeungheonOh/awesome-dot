---
name: create-3d-asset
description: Create or edit a reusable three-dimensional model or scene asset, preserving the requested editable source and checking its saved geometry, materials, transforms and export. Use for digital props, scene objects and their requested rigging or animation; a flat illustration, edited video or physical room-fit assessment has a different primary workflow.
---

# Create a 3D Asset

Deliver the actual model or scene asset the user can open, edit or place in its intended consumer. A rendered image can help judge appearance, but it does not substitute for requested geometry, editable source or an interchange file.

Use `create-visual-asset` when the final result is a flat illustration or image, even if a 3D technique helps make it. Use `create-edited-video` for a finished sequence of shots, and `room-layout-fit-check` for checking a proposed physical arrangement. A reusable model belongs here; building the application that displays it remains a software task. Do not infer fabrication, structural strength, watertight printing or physical safety from a successful digital model.

## Establish what the asset must support

Identify the requested object or scene, its visual treatment and the actual deliverables. Distinguish an editable source, a reusable exchange asset, a rendered preview and a finished animation. Supply the subset requested, using a sensible supported format when none is specified.

Resolve the constraints that change construction: intended consumer, dimensions and units, up and forward directions, placement origin, separate parts, material or texture needs, motion, and any geometry or file-size budget. Use the supplied brief and references before asking questions. A simple static object does not need a rig, UV atlas, multiple levels of detail or a design interview.

For supplied models, inspect the actual source before editing. Check its object hierarchy, transforms, construction features, materials, linked resources and animation as relevant. Separate appearance references from files that must be preserved. Determine which properties may change and which must survive; retain the original unless replacement is explicitly requested.

## Choose a representation that stays useful

Check the available authoring, inspection, rendering and export tools and their installed versions. Choose a representation for the intended use: an editable mesh, curves or procedural construction may suit an illustration or scene prop; a dimension-driven solid may suit a different native modeling task. Do not claim parametric editability merely because a tessellated mesh opens in a native file.

Keep useful source structure where the user needs later changes. Named parts and a clear hierarchy are often more useful than one joined object; unnecessary object fragmentation can make a simple model harder to use. A generation script can accompany a model when helpful, but does not replace a requested native file. Save dependencies within the deliverable or use a supported relative arrangement rather than relying on the author's machine.

Decide early which features the exchange format and target consumer can represent. Construction modifiers, procedural shaders, constraints, rigs and instances may need evaluated geometry, baked textures or sampled animation on an export copy. Preserve the editable source and explain a material loss of editability; do not silently flatten the only source to make export succeed.

## Build or apply the requested edit

Establish units, placement origin and part relationships before adding detail. Check dimensions in the relevant evaluated or world space: local mesh coordinates, object scale and parent transforms can describe different sizes. Applying every transform indiscriminately can change pivots, parenting or animation. Make any conversion deliberately and check its effect.

For articulated parts, place the pivot where the movement belongs and attach dependent details to the correct parent. For a bounded edit, change the relevant geometry, material, transform or animation channel while preserving unrelated parts. Compare the saved result to the original at the level the request protects; a similar preview does not establish unchanged geometry or timing.

Match topology and detail to use. Check for unintended holes, duplicate or degenerate faces, reversed normals, shading seams and intersections that affect the requested views or motion. Open surfaces can be intentional; closed manifold geometry is not a universal requirement for a digital asset. If a triangle budget matters, count the evaluated exported geometry, including subdivision or other generated detail, rather than only the editable base mesh.

Use material features supported by the intended export and consumer. Check transparency mode, sidedness, texture paths and color handling where they matter. A studio light can make a dull material appear bright, and a preview renderer can support nodes the exchange format drops. Judge the actual material and the exported appearance separately from the lighting setup. Do not add an external texture dependency when a simple portable material satisfies the brief.

## Include motion only when requested

Keep the requested motion, duration, clip identity and starting state explicit. Relate frame numbers to seconds using the scene's frame rate and actual clip start; a last frame number alone does not establish duration. Confirm which actions or animation tracks the exporter includes and whether constraints or other controls need baking.

Check the motion between endpoints as well as at them. Look for pivot drift, unexpected scale, penetration, detached details and loop discontinuities. Use playback, sampled poses or geometry checks as supported, and distinguish what each establishes. Two attractive endpoint images do not prove clear motion throughout an interval.

Verify exported animation against the requested time and pose behavior. An exported controller name does not establish that the right channels or range were saved. If the target cannot preserve the requested rig or motion, explain that specific limitation before substituting a static asset or a materially different animation.

## Inspect the saved source and exchange asset

Reopen the final native source. Check the relevant objects, editable structure and dependencies, then inspect rendered views that expose the important features. Choose views from the task: a hollow object's interior, an underside attachment or an articulated joint may need a view that the attractive cover image hides. When later editing is central, make a small representative change in a separate copy and confirm it behaves as intended without altering the deliverable.

Export only the intended asset content. Keep preview cameras, lights, floors and helper geometry out of a prop export unless requested. Check export selection, visibility and collection rules explicitly; an object hidden in one preview may still be exported.

Import the exact saved exchange file into a clean scene or open it in the intended supported consumer. Check the properties material to the brief: overall scale and bounds, ground placement, axes, hierarchy and pivots, geometry count, materials and embedded or linked resources, and any requested animation. Inspect an actual rendered view of the imported asset as well as its structural data. Reusing the still-open authoring scene is not an export readback.

Compare source and imported versions under reasonably comparable viewing conditions. Diagnose whether a discrepancy comes from geometry, transforms, export support, material interpretation or lighting before changing the model. A successful reimport in the authoring application supports that route; it does not certify every engine or viewer. If the requested consumer is unavailable, retain the usable files and state the narrower checks performed.

Format conventions can differ from the native scene. For example, glTF defines meter-based distances, a right-handed coordinate system with Y up, and animation timestamps in seconds. Treat those as glTF rules rather than universal modeling defaults, and verify any axis or time conversion in the exported file. The [Khronos glTF specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html) is the authoritative reference for that format; use the relevant current documentation for other formats and exporters.

## Hand over the usable files

Deliver the requested native source, exchange file and necessary dependencies, with concise previews when useful. Keep filenames and the handoff clear about which file is editable and which is an export. State the units, orientation or pivot convention the recipient needs, the software or consumer actually checked, and any consequential limitation.

Keep the handoff proportional. A small prop usually needs its files and a short usage note, not a modeling diary or a test ledger. Do not add asset-store publication, hosting or uploads to unrelated services merely to deliver it.
