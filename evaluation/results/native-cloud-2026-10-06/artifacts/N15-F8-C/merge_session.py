"""Snapshot-based positional merge sessions for the fictional Fieldcard editor."""
from copy import deepcopy
from merge_primitive import merge_lines


class StaleChoiceError(ValueError):
    """A choice belongs to a different source generation."""


class MergeSession:
    def __init__(self, base, left, right):
        self._sources = self._validated(base, left, right)
        self._generation = 0
        self._choices = {}

    @staticmethod
    def _validated(base, left, right):
        # Validate before committing anything to an existing session. The only
        # accepted snapshot values are strings and integers, copied below.
        incoming = {"base": base, "left": left, "right": right}
        for item in incoming.values():
            if (not isinstance(item, dict)
                    or set(item) != {"document_id", "revision", "text"}
                    or not isinstance(item["document_id"], str)
                    or not item["document_id"]
                    or type(item["revision"]) is not int
                    or item["revision"] < 0):
                raise ValueError("invalid source snapshot")
        if len({item["document_id"] for item in incoming.values()}) != 1:
            raise ValueError("source identities disagree")
        merge_lines(*(incoming[k]["text"] for k in ("base", "left", "right")))
        return deepcopy(incoming)

    def _parts(self):
        return merge_lines(*(self._sources[k]["text"] for k in ("base", "left", "right")))

    def replace_sources(self, base, left, right):
        sources = self._validated(base, left, right)
        if sources["base"]["document_id"] != self._sources["base"]["document_id"]:
            raise ValueError("an existing session cannot switch document identity")
        if sources != self._sources:
            self._sources = sources
            self._generation += 1
            # Even matching alternatives at the same index are new snapshots.
            self._choices = {}

    def choose(self, index, side, generation):
        # Check the token first, even when the index or side is also invalid.
        if type(generation) is not int or generation != self._generation:
            raise StaleChoiceError("choice token does not match the current generation")
        conflicts = {part["index"] for part in self._parts() if part["kind"] == "conflict"}
        if type(index) is not int or index not in conflicts or side not in ("left", "right"):
            raise ValueError("choose a current conflict index and left/right side")
        self._choices[index] = side

    def view(self):
        conflicts, lines = [], []
        for part in self._parts():
            if part["kind"] == "automatic":
                lines.append(part["automatic"])
            else:
                side = self._choices.get(part["index"])
                conflicts.append({"index": part["index"], "base": part["base"],
                                  "left": part["left"], "right": part["right"], "choice": side})
                lines.append(part[side] if side else part["base"])
        status = "draft" if any(c["choice"] is None for c in conflicts) else "complete"
        return {"document_id": self._sources["base"]["document_id"],
                "generation": self._generation, "status": status,
                "text": "\n".join(lines) + "\n", "conflicts": conflicts}

    def to_state(self):
        return {"schema": 1, "sources": deepcopy(self._sources), "generation": self._generation,
                "choices": [{"index": i, "side": side} for i, side in sorted(self._choices.items())]}

    @classmethod
    def from_state(cls, state):
        sources = state["sources"]
        session = cls(sources["base"], sources["left"], sources["right"])
        session._generation = state["generation"]
        for choice in state["choices"]:
            session.choose(choice["index"], choice["side"], session._generation)
        return session
