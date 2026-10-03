---
name: analyze-geospatial-data
description: Answer a spatial question from authorized vector or raster data, with suitable coordinate systems, explicit geometric or pixel-support rules, and checked saved results. Use when location, spatial relationships, distance, area or raster alignment determine the answer; ordinary tabular analysis and styling an already established map have separate primary workflows.
---

# Analyze Geospatial Data

Produce the requested spatial answer and usable data or map, preserving the meaning of the source coordinates and measurements. A plausible map, matching layer names or a successful file conversion does not establish a correct spatial analysis.

Use `analyze-data-question` when the question is primarily about tabular populations or trends and geometry does not change the calculation. Use `visualize-information` to communicate already established spatial findings. A map can support this analysis without becoming a separate project. Keep navigation, physical access, survey accuracy and eligibility decisions distinct from geometric results.

## Establish the spatial question and source support

Inspect the actual authorized sources before choosing a method. Identify what the requested result represents: features, spatial relationships, a distance or area, values sampled at locations, a zone summary, or a comparison between raster surfaces. Clarify a consequential ambiguity such as distance to a centroid versus the nearest boundary; do not require a general GIS intake when the task is clear.

Read native metadata and representative contents with available format-aware tools. Check layer or band names, feature counts, geometry types, extents, coordinate reference systems, units, dimensionality and relevant dates or versions. For rasters, inspect dimensions, affine transform, pixel support, band meanings, scale/offset and validity masks or NoData values. A filename, a display legend or the presence of a CRS label is insufficient.

Preserve original sources and exact feature identities. Keep a source row, a geometry component and a real-world entity separate: a multipart feature may still be one record, while repeated IDs may represent several occurrences. Retain missing, empty and invalid geometries distinctly from valid features outside the selected area. Missing coordinates are not an origin, and an empty match is not proof that an unlocated feature lies outside every zone.

Establish the source's coverage and measurement limits. A clipped layer, incomplete tile set or partial service response may omit relevant features. Precision in a coordinate file does not establish positional accuracy. Record supplied uncertainty or resolution where it affects the conclusion; do not invent a survey tolerance from the number of decimals.

## Put coordinates and measures on a defensible basis

Determine the actual CRS and data axis order for each source. Longitude/latitude, latitude/longitude and easting/northing conventions are not interchangeable. Check plausible coordinate ranges and a known reference when available. The [GDAL coordinate transformation tutorial](https://gdal.org/en/stable/tutorials/osr_api_tut.html) explains why authority axis order and a library's data-axis mapping can differ.

Assigning a CRS describes existing coordinates; transforming changes their representation. Do not relabel coordinates to make layers appear aligned. If the source CRS or units are genuinely unknown, keep affected distances, areas or overlays unresolved while completing independent inspection. Resolve the missing reference from source evidence rather than guessing from a map's appearance.

Choose a calculation method suitable for the extent and quantity. A projected metric CRS can support local planar distances; area comparisons may need a suitable equal-area or geodesic method. Geographic degrees and display-projection units must not be silently interpreted as metres or square metres. Account for datum, axis, epoch or vertical-reference differences when they are material, without imposing global-geodesy machinery on a simple local task.

Name the measure actually calculated: planar, geodesic, along-line or network distance; polygon area, bounding-box area or covered raster area. Straight-line proximity does not establish travel time, a traversable path or access. A centroid-based result is not automatically a result for every part of an irregular feature.

## For vector data: preserve geometric relationships

Choose the predicate that answers the question. Interior containment, boundary-inclusive membership, intersection, positive-area overlap and nearest feature are different relationships. State how boundaries, holes, touching features and ties are treated when they can change the result. Do not use a bounding box as a substitute for the actual geometry unless its limited purpose is explicit.

Validate the geometry needed for the operation. Retain multipart components and holes. If repair is necessary, work on a derivative and check the changed geometry, feature identity, type and area; a successful repair function does not prove that its interpretation matches the source's intent. Do not silently drop failed features or convert them into successful nonmatches.

Keep spatial-join multiplicity visible. A point can belong to several overlapping zones, and an intersecting feature can contribute to several output pieces. Preserve the relevant source IDs and all intended relationships. Distinguish membership counts from distinct-feature counts. Resolve a requested single assignment using an explicit rule, not the engine's first match or arbitrary row order.

For area or coverage, decide whether the requested whole is a sum of contributions or a geometric union. Overlapping polygon areas generally cannot be summed to obtain union area. For clipping or allocation, state whether a value describes the whole feature, is an intensive rate, or can defensibly be apportioned by area. Geometric fractions alone do not prove that people, assets or quantities are uniformly distributed.

Use full calculation precision for thresholds and round only presentation. Keep computational tolerance separate from source uncertainty. A chosen tolerance must not become permission to move features or round a failed constraint into a pass. If a buffered or simplified shape is an approximation, ensure its error is appropriate for its purpose; a display outline need not be the authority for an exact distance classification.

## For rasters: compare the same spatial support

Treat the grid as georeferenced data, not merely an image array. Equal dimensions or matching CRS names do not establish matching pixels. Compare origin, resolution, rotation, extent and pixel alignment before combining arrays. A pixel centre, its footprint and a point sample answer different questions; the [GDAL raster data model](https://gdal.org/en/stable/user/raster_data_model.html) describes these distinctions and affine georeferencing.

Interpret band values using their declared scale, offset and units. Keep validity separate from numeric values so a NoData sentinel or masked sample does not enter arithmetic, and valid zero is not discarded. When comparing periods or sources, retain the common valid support and report excluded coverage. A mean over the observed part of a footprint is not automatically its full-footprint value.

Choose resampling or aggregation from the quantity's meaning. Category labels should not become invented intermediate classes. An intensive value may call for a weighted mean; a total may require a conservation-aware operation. Merely increasing resolution does not add information. Document the target grid and the treatment of edge pixels, partial overlap and invalid contributing areas. Check the engine's actual behavior; for example, [GDAL's resampling documentation](https://gdal.org/en/stable/programs/gdalwarp.html#cmdoption-gdalwarp-r) distinguishes averaging valid contributors from other kernels.

For zonal summaries, define which pixel support counts: centres inside a zone, every touched pixel, or fractional footprint overlap. Carry the relevant denominator or coverage area. If full coverage is required, a normalized average of valid contributors alone cannot demonstrate it. Preserve an explicit coverage result when missing support changes which cells or zones can be compared.

Avoid claiming that raster alignment removes uncertainty in the inputs. Reprojection, interpolation, aggregation and thresholding can alter a result. Use a proportionate sensitivity check when a reasonable alternative resolution or inclusion rule changes the substantive answer; do not manufacture scenarios when the contract is settled and the effect immaterial.

## Check the actual saved answer and map

Reopen the delivered spatial file through a suitable native reader. Check CRS and axis interpretation, field types and IDs, geometry or grid structure, validity states and representative values. Verify that the output contains the intended sources and relationships, including excluded or unresolved records where needed. For a CSV or simpler export, state losses such as absent geometry/CRS metadata or ambiguous blank values, and preserve a way to interpret them.

Use independent checks that challenge the consequential operation: a known coordinate transform, a boundary or hole case, a raw distance, an area reconciliation, a raster footprint calculation or a missing-support case. Counts, file integrity, numerical calculations and visual inspection establish different things. A map that looks aligned does not prove correct units, and a correct in-memory array does not prove a saved raster retained its mask or transform.

When a map is requested, render and inspect the actual export at its reading size. Show the relevant extent, units or scale, meaningful legend and missing coverage. Use a suitable spatial aspect and projection; label coordinate offsets and approximations. Avoid obscuring coincident or nearby features, and distinguish unlocated records from points omitted merely for readability. Inspect map labels and classes against the saved data after revisions.

Lead the handoff with the spatial answer and its practical limits. Deliver only the requested data, map and useful reproducible method, with enough source/version and operation detail to check the result. A small answer does not require a GIS project, multiple exports or an audit ledger. Distinguish native file readback from GUI interaction and nominal model geometry from independently measured physical conditions. Publication, service updates or sharing source locations remain separate actions unless authorized.
