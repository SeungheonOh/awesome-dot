"""A fictional reading queue; entries have title and non-negative minutes."""


def summarize(entries):
    return {"titles": sorted(entry["title"] for entry in entries)}
