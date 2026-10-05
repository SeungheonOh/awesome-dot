"""Changed positional-line merge primitive for the fictional Fieldcard editor."""
def merge_lines(base, left, right):
    texts = (base, left, right)
    for text in texts:
        if not isinstance(text, str) or not text or not text.endswith("\n") or "\r" in text:
            raise ValueError("each document must be nonempty LF-terminated text without CR")
    lines = [text[:-1].split("\n") for text in texts]
    if len({len(part) for part in lines}) != 1 or not 1 <= len(lines[0]) <= 12:
        raise ValueError("all three documents need the same 1..12 positional lines")
    result = []
    for index, (b, l, r) in enumerate(zip(*lines)):
        automatic = l if l == r else r if l == b else l if r == b else None
        result.append({"index": index, "base": b, "left": l, "right": r,
                       "kind": "conflict" if automatic is None else "automatic",
                       "automatic": automatic})
    return result
