"""A fictional reading queue; entries have title and non-negative minutes."""


def summarize(entries):
    return {
        "titles": [entry["title"] for entry in entries],
        "count": len(entries),
        "total_minutes": sum(entry["minutes"] for entry in entries),
    }
