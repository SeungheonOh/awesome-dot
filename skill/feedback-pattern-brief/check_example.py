#!/usr/bin/env python3
"""Check this fictional fixture's accounting, not live data or semantic coding."""
from collections import Counter
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import re

START = datetime.fromisoformat("2026-09-01T00:00:00+00:00")
END = datetime.fromisoformat("2026-09-08T00:00:00+00:00")
STANCES = {"problem_reported", "no_problem_reported", "mixed", "unclear"}


def inventory(rows):
    """Record ID establishes copies; content or respondent equality does not."""
    originals, aliases = {}, {}
    for row in rows:
        source = row["source"]
        content = {key: value for key, value in row.items() if key != "row"}
        if source in originals:
            if content != originals[source]:
                raise ValueError(f"Unresolved versions/content for {source}")
        else:
            originals[source] = content
        aliases.setdefault(source, []).append(row["row"])
    included, excluded = {}, {}
    for source, record in originals.items():
        submitted = datetime.fromisoformat(record["submitted"].replace("Z", "+00:00"))
        if submitted.tzinfo is None:
            raise ValueError("Timezone is required")
        if not START <= submitted < END:
            excluded[source] = "outside_window"
        elif not record["text"].strip():
            excluded[source] = "blank"
        else:
            included[source] = record
    return included, excluded, {key: sorted(value) for key, value in aliases.items()}


def respondent_counts(records):
    return {
        "known_respondents": len({r["respondent"] for r in records if r["respondent"] is not None}),
        "unknown_identity_sources": sum(r["respondent"] is None for r in records),
    }


def summarize(included, coding):
    if set(coding) != set(included):
        raise ValueError("Every included source must be reviewed; no excluded sources may be coded")
    groups, by_stance = {}, {}
    for source, assignments in coding.items():
        seen = set()
        for theme, stance, excerpt in assignments:
            if theme in seen:
                raise ValueError("One assignment per source/theme; repeated mentions are not extra sources")
            if stance not in STANCES or not excerpt or excerpt not in included[source]["text"]:
                raise ValueError("Unsupported stance or non-exact excerpt")
            seen.add(theme)
            groups.setdefault(theme, set()).add(source)
            by_stance.setdefault(theme, Counter())[stance] += 1
    summary = {}
    for theme, source_ids in sorted(groups.items()):
        summary[theme] = {
            "sources": len(source_ids),
            "eligible_comments": len(included),  # All C is eligible in this fixture only.
            **respondent_counts([included[source] for source in source_ids]),
            "stances": dict(sorted(by_stance[theme].items())),
        }
        assert sum(by_stance[theme].values()) == len(source_ids)
    return summary, groups


def must_reject(operation, message):
    try:
        operation()
    except ValueError:
        return
    raise AssertionError(message)


def main():
    text = Path(__file__).with_name("example.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```json\n(.*?)\n```", text, flags=re.DOTALL)
    assert len(blocks) == 2
    rows, coding = map(json.loads, blocks)
    before = deepcopy((rows, coding))
    assert len({row["row"] for row in rows}) == len(rows) == 11
    included, excluded, aliases = inventory(rows)
    assert len(aliases) == 10
    assert sum(len(value) - 1 for value in aliases.values()) == 1
    assert aliases["survey:S1"] == ["R01", "R02"]
    assert excluded == {"survey:S7": "blank", "support:C3": "outside_window"}
    assert len(rows) == 1 + len(excluded) + len(included)
    assert len(included) == 8
    assert Counter(r["channel"] for r in included.values()) == {"survey": 6, "support": 2}
    assert respondent_counts(list(included.values())) == {
        "known_respondents": 5, "unknown_identity_sources": 2}
    assert sum(r["respondent"] is not None for r in included.values()) == 6

    summary, groups = summarize(included, coding)
    assert summary == {
        "D": {"sources": 5, "eligible_comments": 8, "known_respondents": 4,
              "unknown_identity_sources": 0,
              "stances": {"no_problem_reported": 1, "problem_reported": 4}},
        "L": {"sources": 6, "eligible_comments": 8, "known_respondents": 3,
              "unknown_identity_sources": 2,
              "stances": {"no_problem_reported": 2, "problem_reported": 4}},
        "T": {"sources": 1, "eligible_comments": 8, "known_respondents": 1,
              "unknown_identity_sources": 0, "stances": {"problem_reported": 1}},
    }
    assert len(groups["D"] & groups["L"]) == 3
    assert len(groups["L"] & groups["T"]) == 1
    assert not groups["D"] & groups["T"]
    assert set.union(*groups.values()) == set(included)
    assert sum(map(len, groups.values())) == 12 > len(included)
    # Problem-only denominators use the eligible comment set, not all theme tags.
    for theme, expected_known, expected_unknown in [("D", 3, 0), ("L", 1, 2)]:
        problem_sources = [source for source, codes in coding.items()
                           if any(t == theme and s == "problem_reported" for t, s, _ in codes)]
        assert len(problem_sources) == 4
        assert respondent_counts([included[source] for source in problem_sources]) == {
            "known_respondents": expected_known, "unknown_identity_sources": expected_unknown}

    # Same wording is not a merge rule, whether identities are known or unknown.
    for left, right in [("survey:S2", "survey:S3"), ("survey:S4", "support:C2")]:
        assert included[left]["text"] == included[right]["text"]
        assert left != right and left in included and right in included
    assert included["survey:S2"]["respondent"] != included["survey:S3"]["respondent"]
    assert included["support:C1"]["respondent"] == included["survey:S1"]["respondent"]
    assert included["support:C1"]["same_episode_as"] == "survey:S1"

    # Unknown sources are not silently assigned unique fictional people.
    known = {r["respondent"] for r in included.values() if r["respondent"] is not None}
    assert None not in known and len(known) == 5
    possible_same = deepcopy(included)
    possible_distinct = deepcopy(included)
    for index, source in enumerate(["survey:S4", "support:C2"]):
        possible_same[source]["respondent"] = "P1"
        possible_distinct[source]["respondent"] = f"HYPOTHETICAL-{index}"
    assert respondent_counts(list(possible_same.values()))["known_respondents"] == 5
    assert respondent_counts(list(possible_distinct.values()))["known_respondents"] == 7
    # Both assignments fit the missing identities; neither is an asserted result.

    reversed_included, reversed_excluded, reversed_aliases = inventory(list(reversed(rows)))
    assert (reversed_included, reversed_excluded, reversed_aliases) == (included, excluded, aliases)
    assert summarize(reversed_included, coding) == (summary, groups)
    extra_copy = deepcopy(rows[0])
    extra_copy["row"] = "TEST-COPY"
    copied_included, copied_excluded, copied_aliases = inventory(rows + [extra_copy])
    assert copied_included == included and copied_excluded == excluded
    assert sum(len(value) - 1 for value in copied_aliases.values()) == 2
    assert summarize(copied_included, coding) == (summary, groups)
    changed_copy = deepcopy(extra_copy)
    changed_copy["text"] = "A changed version must not be silently selected."
    must_reject(lambda: inventory(rows + [changed_copy]), "Changed copies must stay unresolved")

    repeated = deepcopy(coding)
    repeated["survey:S1"].append(deepcopy(repeated["survey:S1"][0]))
    must_reject(lambda: summarize(included, repeated), "Repeated theme mentions must not inflate counts")
    bad_quote = deepcopy(coding)
    bad_quote["survey:S1"][0][2] = "An invented customer quotation."
    must_reject(lambda: summarize(included, bad_quote), "Non-exact excerpts must be rejected")
    # A mixed source gets one mutually exclusive stance, not two source counts.
    mixed = deepcopy(coding)
    mixed["survey:S1"][0][1] = "mixed"
    mixed_summary, _ = summarize(included, mixed)
    assert mixed_summary["D"]["sources"] == 5
    assert mixed_summary["D"]["stances"] == {
        "no_problem_reported": 1, "problem_reported": 3, "mixed": 1}

    boundary = deepcopy(rows[0])
    boundary.update(row="TEST-BOUNDARY", source="survey:boundary", submitted=START.isoformat())
    assert "survey:boundary" in inventory([boundary])[0]
    boundary["submitted"] = END.isoformat()
    assert inventory([boundary])[1] == {"survey:boundary": "outside_window"}
    assert (rows, coding) == before
    print(json.dumps({"included_comments": len(included),
                      **respondent_counts(list(included.values())), "themes": summary}, indent=2))
    print("PASS: copies, identities, excerpts, exclusions, overlaps, denominators, stances and boundaries")


if __name__ == "__main__":
    main()
