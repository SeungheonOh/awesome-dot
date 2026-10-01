# Fictional Source Packet: Evening-Hours Pilot

Everything in this packet is invented, including the organization, articles, timestamps and example.invalid URLs. The short source passages are the entire supplied evidence for this rehearsal. They are not extracts of real reporting. No URL needs to be opened for the offline exercise.

The reader is planning a public calendar entry for the fictional Larkspur Quay Library Service's North and Quay branches. Compare the saved brief through September 18 with what was knowable through September 28 at 12:00 UTC. Preserve the same branches, Monday pilot hours, staffing claim and funding decision. The packet was assembled September 29 and deliberately includes later evidence; its availability does not make that evidence eligible for the earlier cutoff.

Event IDs and source relationships below are explicit editorial annotations of this small fixture. They can be inspected against the passages. They are not the output of an automatic news-matching service. A source may discuss multiple events, and the same URL may have multiple retained versions.

```json
{
  "fictional": true,
  "topic": "Larkspur Quay Library Service evening-hours pilot",
  "scope": "North and Quay branches; Monday hours, announced pilot dates, staffing and the pilot grant",
  "prior_cutoff": "2026-09-18T18:00:00+00:00",
  "cutoff": "2026-09-28T12:00:00+00:00",
  "packet_assembled_at": "2026-09-29T09:30:00+00:00",
  "baseline": {
    "id": "brief-2026-09-18-v1",
    "statements": [
      {"id": "B1", "text": "The planned pilot runs October 5 through December 14, with Monday hours of 18:00–20:00 at North and Quay.", "supports": ["P1#plan"]},
      {"id": "B2", "text": "Eight newly hired library assistants will cover the pilot.", "supports": ["P1#staffing"]},
      {"id": "B3", "text": "The council approved a $60,000 pilot grant on May 12.", "supports": ["G0#decision"]},
      {"id": "B4", "text": "Planning inference: October 5 is the first date to put on the provisional calendar; the staffing notice describes eight added jobs.", "supports": ["P1#plan", "P1#staffing"]}
    ]
  },
  "sources": [
    {
      "id": "G0", "title": "Council minutes: pilot grant", "issuer": "Larkspur Quay Council",
      "url": "https://council.example.invalid/minutes/2026-05-12", "version": "minutes-adopted-v1", "role": "official record",
      "published_at": "2026-05-13T09:00:00+00:00", "updated_at": null,
      "available_at": "2026-05-13T09:00:00+00:00", "retrieved_at": "2026-09-18T17:00:00+00:00",
      "access": "read", "coverage": "entire supplied passage", "derived_from": [], "cites": [],
      "events": {"grant-decision": "2026-05-12"},
      "passages": {"decision": "On May 12, the council approved a $60,000 grant for the North and Quay branches' evening-hours pilot."}
    },
    {
      "id": "P1", "title": "Evening-hours pilot notice", "issuer": "Larkspur Quay Library Service",
      "url": "https://library.example.invalid/notices/evening-pilot", "version": "notice-v1", "role": "official notice",
      "published_at": "2026-09-16T09:00:00+00:00", "updated_at": null,
      "available_at": "2026-09-16T09:00:00+00:00", "retrieved_at": "2026-09-18T17:10:00+00:00",
      "access": "read", "coverage": "entire supplied passage", "derived_from": [], "cites": [],
      "events": {"pilot-decision": "2026-09-15"},
      "planned_start": "2026-10-05", "planned_end": "2026-12-14",
      "passages": {
        "plan": "Following its September 15 decision, the service plans Monday opening from 18:00 to 20:00 at North and Quay, from October 5 through December 14. Branch-specific exceptions will be listed in a separate register.",
        "staffing": "Eight newly hired library assistants will cover the pilot."
      }
    },
    {
      "id": "R1", "title": "Autumn bulletin: how the pilot was funded", "issuer": "Larkspur Quay Council",
      "url": "https://council.example.invalid/bulletins/autumn-pilot", "version": "bulletin-v1", "role": "official historical recap",
      "published_at": "2026-09-22T09:00:00+00:00", "updated_at": null,
      "available_at": "2026-09-22T09:00:00+00:00", "retrieved_at": "2026-09-28T11:00:00+00:00",
      "access": "read", "coverage": "entire supplied passage", "derived_from": ["G0"], "cites": ["G0"],
      "events": {"grant-decision": "2026-05-12"},
      "passages": {"recap": "From the May 12 council minutes: the council approved a $60,000 grant for the North and Quay evening-hours pilot. This bulletin republishes that decision for autumn readers and announces no additional grant."}
    },
    {
      "id": "D1", "title": "Two branches to offer evening pilot", "issuer": "Quay Notebook",
      "url": "https://notebook.example.invalid/library-evenings", "version": "story-v1", "role": "derivative reporting",
      "published_at": "2026-09-24T09:00:00+00:00", "updated_at": null,
      "available_at": "2026-09-24T09:00:00+00:00", "retrieved_at": "2026-09-28T11:02:00+00:00",
      "access": "read", "coverage": "entire supplied passage", "derived_from": ["P1"], "cites": ["P1"],
      "events": {"pilot-decision": "2026-09-15"},
      "passages": {"report": "This story summarizes the service's September 16 notice: North and Quay plan Monday evening hours from October 5 through December 14, covered by eight newly hired library assistants. The notice is our sole source; we have done no additional reporting."}
    },
    {
      "id": "N1", "title": "Pilot timetable amendment", "issuer": "Larkspur Quay Library Service",
      "url": "https://library.example.invalid/notices/pilot-timetable-amendment", "version": "amendment-v1", "role": "official amendment",
      "published_at": "2026-09-25T14:00:00+00:00", "updated_at": null,
      "available_at": "2026-09-25T14:00:00+00:00", "retrieved_at": "2026-09-28T11:04:00+00:00",
      "access": "read", "coverage": "entire supplied passage", "derived_from": [], "cites": ["P1"],
      "events": {"schedule-change": "2026-09-25"},
      "planned_start": "2026-10-12", "planned_end": "2026-12-14",
      "passages": {
        "change": "Today, September 25, the service decided to move the planned first pilot evening from October 5 to October 12 to allow time for branch inspections. This amends the September 16 notice. It is a change of plan, not a correction of that notice's original date.",
        "retained": "North and Quay remain the participating branches. Monday hours remain 18:00–20:00 and the planned end remains December 14. Branch-specific exceptions are governed by the separate register."
      }
    },
    {
      "id": "P2", "title": "Evening-hours pilot notice, corrected", "issuer": "Larkspur Quay Library Service",
      "url": "https://library.example.invalid/notices/evening-pilot", "version": "notice-v2", "supersedes": "P1", "role": "official corrected notice",
      "published_at": "2026-09-16T09:00:00+00:00", "updated_at": "2026-09-26T10:00:00+00:00",
      "available_at": "2026-09-26T10:00:00+00:00", "retrieved_at": "2026-09-28T11:06:00+00:00",
      "access": "read", "coverage": "entire supplied passage", "derived_from": [], "cites": ["P1", "N1"],
      "events": {"pilot-decision": "2026-09-15", "staffing-correction": "2026-09-26"},
      "passages": {
        "plan": "The September 15 pilot decision concerned North and Quay. Its schedule is amended by the September 25 timetable notice.",
        "staffing": "Eight existing library assistants are assigned to cover the pilot.",
        "correction": "Correction, September 26: the original notice mistakenly described these eight assistants as newly hired. They were already employed when assigned on September 15. This correction announces no hiring or staffing change."
      }
    },
    {
      "id": "X1", "title": "Branch exceptions register", "issuer": "Larkspur Quay Library Service",
      "url": "https://library.example.invalid/registers/pilot-exceptions", "version": null, "role": "official register",
      "published_at": null, "updated_at": null, "available_at": null,
      "retrieved_at": "2026-09-28T11:08:00+00:00", "access": "failed",
      "coverage": "simulated HTTP 503; no register content inspected", "derived_from": [], "cites": [], "events": {}, "passages": {}
    },
    {
      "id": "L1", "title": "Pilot withdrawn", "issuer": "Larkspur Quay Library Service",
      "url": "https://library.example.invalid/notices/pilot-withdrawn", "version": "withdrawal-v1", "role": "official withdrawal",
      "published_at": "2026-09-29T08:00:00+00:00", "updated_at": null,
      "available_at": "2026-09-29T08:00:00+00:00", "retrieved_at": "2026-09-29T09:00:00+00:00",
      "access": "read", "coverage": "entire supplied passage", "derived_from": [], "cites": ["N1"],
      "events": {"pilot-withdrawal": "2026-09-29"},
      "passages": {"withdrawal": "On September 29 the service withdrew the announced pilot for both branches. No replacement date has been announced."}
    }
  ],
  "editorial_assignments": [
    {"id": "C1", "status": "unchanged", "event": "grant-decision", "baseline": ["B3"], "supports": ["R1#recap", "G0#decision"], "reason": "R1 explicitly republishes the same May decision and amount."},
    {"id": "C2", "status": "unchanged", "event": "pilot-decision", "baseline": ["B1", "B2"], "supports": ["D1#report", "P1#plan", "P1#staffing"], "reason": "Derivative evidence repeats the original account; this label describes its lack of added evidence, not the current truth of its stale claims."},
    {"id": "C3", "status": "new", "event": "schedule-change", "baseline": ["B1", "B4"], "supports": ["N1#change", "P1#plan"], "reason": "An explicit follow-on decision changes the planned first evening."},
    {"id": "C4", "status": "confirmation", "event": "schedule-change", "baseline": ["B1"], "supports": ["N1#retained", "P1#plan"], "reason": "Fresh official reaffirmation of branches, hours and end date; not independent observation."},
    {"id": "C5", "status": "correction", "event": "staffing-correction", "baseline": ["B2", "B4"], "supports": ["P2#staffing", "P2#correction", "P1#staffing"], "reason": "Explicit correction revises the account of September 15 staffing; no real-world headcount change is asserted."}
  ]
}
```

All date-only event fields have day precision. Their ordering relative to a time-of-day boundary must not be inferred from midnight defaults. Here they are several days from the cutoff and source-version availability has explicit offsets. Planned operating hours are local hours as printed; no conversion to a real place's timezone is attempted for this invented setting.
