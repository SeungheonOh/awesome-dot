#!/usr/bin/env python3
"""Exercise the fixed synthetic warranty packet locally; no external actions."""
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import tempfile

SOURCES = {
    "E1": "Order TEST-1042. Paper Finch Home. Mosslight ML-4. Purchased 2025-05-07.",
    "E2": "Delivery record for TEST-1042: delivered 2025-05-10.",
    "E3": ("ML-series household warranty, version 2025-01. Original household purchaser; "
           "authorized retailer; defects in materials or workmanship. Begins on delivery; "
           "ends immediately before the second delivery anniversary. Normal battery-capacity "
           "decline and impact/liquid damage excluded. Provider determines coverage and "
           "chooses repair or replacement. Written review requires order confirmation, "
           "delivery record, model, serial and symptom account. Photos optional initially. "
           "Do not ship without separate authorization. Charges need a separate proposal."),
    "E4": ("User account, 2026-10-01: Original purchaser; household use. Since 2026-09-25, "
           "noticeably dimmer after about ten minutes starting with full-charge indicator; "
           "observed twice. Cause unknown. No known drop/liquid exposure. Not opened or repaired."),
    "E5": "User-supplied label transcription, not a photo: model ML-4; serial TEST-ML4-042.",
}
DELIVERY = date(2025, 5, 10)
END_EXCLUSIVE = date(2027, 5, 10)  # Exact non-leap anniversary in the fictional rule.
ASSESSMENT = date(2026, 10, 1)


def in_date_window(day):
    return DELIVERY <= day < END_EXCLUSIVE


def packet_check(fields):
    required = {"order_confirmation", "delivery_record", "model", "serial", "symptoms"}
    missing = sorted(key for key in required if not fields.get(key))
    return {"complete": not missing, "missing": missing}


def action_status(authority, recipient, attachments, complete, charge=False, waiver=False):
    # Small explicit fixture guard, not a substitute for runtime approval policy.
    if authority["action"] != "submit":
        return "prepared_only"
    if recipient != authority["recipient"] or not set(attachments) <= set(authority["attachments"]):
        return "blocked_scope"
    if not complete:
        return "blocked_missing_evidence"
    if charge or waiver:
        return "blocked_new_commitment"
    return "eligible_for_authorized_submission_check"


def digest(data):
    return sha256(data).hexdigest()


def verify_sources(paths, expected):
    if {key: digest(path.read_bytes()) for key, path in paths.items()} != expected:
        raise ValueError("Evidence changed")


def main():
    fields = {"order_confirmation": "E1", "delivery_record": "E2", "model": "ML-4",
              "serial": "TEST-ML4-042", "symptoms": "E4"}
    assert in_date_window(ASSESSMENT)
    assert in_date_window(date(2027, 5, 9))
    assert not in_date_window(END_EXCLUSIVE)
    assert not in_date_window(date(2025, 5, 9))
    assert packet_check(fields) == {"complete": True, "missing": []}
    missing_serial = {**fields, "serial": None}
    assert packet_check(missing_serial) == {"complete": False, "missing": ["serial"]}
    # Evidence supports reports; no program infers a diagnosis or reseller status.
    eligibility_factors = {"date_window": in_date_window(ASSESSMENT),
                           "original_household_purchaser_reported": True,
                           "authorized_retailer": None, "covered_fault": None}
    eligibility = "unresolved" if any(v is None for v in eligibility_factors.values()) else "reviewed"
    assert eligibility == "unresolved"
    authority = {"action": "prepare", "recipient": None, "attachments": []}
    assert action_status(authority, None, list(SOURCES), True) == "prepared_only"
    permitted = {"action": "submit", "recipient": "fictional-provider-route", "attachments": list(SOURCES)}
    assert action_status(permitted, "other-route", list(SOURCES), True) == "blocked_scope"
    assert action_status(permitted, permitted["recipient"], [*SOURCES, "unrelated-record"], True) == "blocked_scope"
    assert action_status(permitted, permitted["recipient"], list(SOURCES), False) == "blocked_missing_evidence"
    assert action_status(permitted, permitted["recipient"], list(SOURCES), True, charge=True) == "blocked_new_commitment"
    assert action_status(permitted, permitted["recipient"], list(SOURCES), True, waiver=True) == "blocked_new_commitment"
    assert action_status(permitted, permitted["recipient"], list(SOURCES), True) == "eligible_for_authorized_submission_check"

    with tempfile.TemporaryDirectory(prefix="warranty-fixture-") as folder:
        root = Path(folder)
        paths = {key: root / f"{key}.txt" for key in SOURCES}
        for key, content in SOURCES.items():
            paths[key].write_text(content, encoding="utf-8")
        originals = {key: digest(path.read_bytes()) for key, path in paths.items()}
        manifest = [{"id": key, "file": paths[key].name, "sha256": originals[key],
                     "kind": "original synthetic text", "included": True} for key in SOURCES]
        assert not any(row["file"].endswith((".png", ".jpg")) for row in manifest)
        assert "transcription, not a photo" in paths["E5"].read_text()
        packet = {"item": fields["model"], "serial": fields["serial"],
                  "assessment": ASSESSMENT.isoformat(), "date_end_exclusive": END_EXCLUSIVE.isoformat(),
                  "completeness": packet_check(fields), "eligibility": eligibility,
                  "eligibility_factors": eligibility_factors, "status": "prepared_only",
                  "symptoms_source": "E4", "diagnosis": None, "manifest": manifest,
                  "questions": ["Is Paper Finch Home an authorized retailer?",
                                "Is this reported issue covered, including the capacity exclusion?"]}
        destination = root / "private-packet.json"
        destination.write_text(json.dumps(packet, indent=2), encoding="utf-8")
        assert json.loads(destination.read_text()) == packet
        verify_sources(paths, originals)
        altered_paths = dict(paths)
        altered = root / "E1-altered.txt"
        altered.write_text(SOURCES["E1"] + " Altered seller claim.", encoding="utf-8")
        altered_paths["E1"] = altered
        try:
            verify_sources(altered_paths, originals)
        except ValueError:
            pass
        else:
            raise AssertionError("Changed evidence should be detected")
        verify_sources(paths, originals)
        print(json.dumps({"complete": packet["completeness"]["complete"],
                          "eligibility": eligibility, "status": packet["status"],
                          "source_digests_unchanged": originals}, indent=2))
    print("PASS: dates, completeness, uncertainty, original evidence, private readback and action scope")


if __name__ == "__main__":
    main()
