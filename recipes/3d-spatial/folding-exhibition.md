---
id: folding-exhibition
title: "Folding Exhibition Layout"
summary: "Create a movable exhibition layout model and measured plan for comparing visitor routes."
category: 3d-spatial
level: intermediate
timebox_minutes: 120
capabilities: ["code", "files"]
tags: ["layout", "exhibition", "spatial-planning"]
status: recipe-not-run
---

# Folding Exhibition Layout

Create a movable exhibition layout model and measured plan for comparing visitor routes.

## Scenario

A small arts group is planning a temporary exhibition in a borrowed rectangular room. Folding panels, tables, and a check-in desk must fit while keeping visitor movement understandable. The group wants to compare two arrangements and see obstructions, using sanitized room measurements instead of a private venue floor plan.

## Inputs to prepare

- [ROOM DIMENSIONS] and ceiling height in meters
- [DOORS AND FIXED OBSTACLES] as measured coordinates
- [PANEL AND TABLE SIZES] plus quantities
- [DESIRED CLEAR ROUTE WIDTH] and visitor sequence

## Copy this prompt into dot

```text
dot, develop a folding-exhibition layout study from [ROOM DIMENSIONS], [DOORS AND FIXED OBSTACLES], [PANEL AND TABLE SIZES], and [DESIRED CLEAR ROUTE WIDTH]. The required toolchain is Blender with Python scripting and a supported renderer; check what is available first. If unavailable, prepare a dimensioned placement schedule and modeling script without claiming rendered or exported results. Ask before any software installation.

Create simple labeled proxy geometry for the room, fixed obstructions, panels, tables, and check-in point. Use meters and an explicit origin. Propose two layouts with different visitor sequences, then compare occupied area, narrow passages, door-swing conflicts, and views from the entrance. Treat route width as my design input, not proof of compliance with building or accessibility rules.

Target an editable Blender scene, a dimensioned top-view SVG generated from placement data, and PNG views if the installed toolchain successfully produces them. Keep the placement data in a readable CSV or JSON file as well. Verify object counts, floor contact, bounds, duplicate names, and overlapping door-swing zones. Include an edge case where the requested furniture cannot fit and explain the conflict rather than silently shrinking it. Use only fictional or sanitized venue information. Keep previews private; ask before publication, venue sharing, or booking anything.
```

## Iterate with a purpose

### 1. Test a different visitor order

```text
Rearrange the same inventory for the revised exhibit sequence I provide, and compare route length and the narrowest passage with the original layout.
```

### 2. Add installation phases

```text
Create three assembly-stage views showing placement order and temporary staging zones, without asserting that the plan is a safety-approved method statement.
```

### 3. Create a venue review packet

```text
Prepare a concise review packet with dimensions, unresolved questions, and labeled views for me to approve before sharing with the venue.
```

## Expected deliverables

- Two layout alternatives and comparison notes
- Editable placement data with units and origin
- Blender scene if supported
- Dimensioned plan SVG and PNG views if rendered successfully
- Conflict and verification log

## Acceptance checks

- Every supplied panel and table appears exactly once in each proposed layout
- All fixed obstacles remain at their supplied coordinates
- No furniture is silently scaled to resolve a space conflict
- The narrowest measured route is reported against the user-supplied target
- Door-swing intersections are visibly marked
- An overfilled-room fixture produces an infeasibility report
- Exported plans and scene objects use the same coordinate convention

## Access, privacy and stop conditions

- Blender rendering and scene exports depend on the installed toolchain
- Layout checks do not certify accessibility, occupancy, fire safety, or structural adequacy
- Venue drawings may be private and must be sanitized or explicitly authorized
- External sharing, publication, and bookings require approval

## Two possible extensions

- Add artwork-height variants for a later curatorial review
- Create a pack-down inventory linked to the approved placement data
