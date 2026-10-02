"""Three implementations of the fictional observation-summary contract.

Inputs have already been validated. No I/O, cache, global mutable state, or
input mutation is part of any implementation.
"""


def baseline(records, requests):
    """Scan all observation occurrences for each request occurrence."""
    output = []
    for requested_id in requests:
        matches = known = total = 0
        for record in records:
            if record["id"] == requested_id:
                matches += 1
                value = record.get("value")
                if value is not None:
                    known += 1
                    total += value
        output.append({"id": requested_id, "matches": matches,
                       "known": known, "total": total if known else None})
    return output


def candidate(records, requests):
    """Aggregate occurrences once; build this index on EVERY invocation."""
    totals = {}
    for record in records:
        aggregate = totals.setdefault(record["id"], [0, 0, 0])
        aggregate[0] += 1
        value = record.get("value")
        if value is not None:
            aggregate[1] += 1
            aggregate[2] += value
    output = []
    for requested_id in requests:
        matches, known, total = totals.get(requested_id, (0, 0, 0))
        output.append({"id": requested_id, "matches": matches,
                       "known": known, "total": total if known else None})
    return output


def wrong_last_record(records, requests):
    """NEGATIVE CONTROL: an ID index silently drops earlier occurrences."""
    last = {record["id"]: record for record in records}
    output = []
    for requested_id in requests:
        record = last.get(requested_id)
        value = record.get("value") if record is not None else None
        output.append({"id": requested_id, "matches": int(record is not None),
                       "known": int(value is not None), "total": value})
    return output
