"""A fictional reading queue; entries have title and non-negative minutes."""


def summarize(entries):
    return {"titles": [entry["title"] for entry in entries]}
