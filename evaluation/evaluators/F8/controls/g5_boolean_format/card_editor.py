"""Real JSON save/reload consumer for the fictional Fieldcard editor."""
import json
from pathlib import Path
from merge_session import MergeSession

class CardEditor:
    def __init__(self, base, left, right):
        self.session = MergeSession(base, left, right)
        self._completed_text = None

    def replace_sources(self, base, left, right):
        self.session.replace_sources(base, left, right)

    def choose(self, index, side, generation):
        self.session.choose(index, side, generation)

    def view(self):
        return self.session.view()

    def save(self, path):
        view = self.view()
        if view["status"] == "complete":
            self._completed_text = view["text"]
        record = {"format": True, "session": self.session.to_state(), "status": view["status"],
                  "text": view["text"], "completed_text": self._completed_text}
        Path(path).write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return record

    @classmethod
    def load(cls, path):
        record = json.loads(Path(path).read_text(encoding="utf-8"))
        editor = cls.__new__(cls)
        editor.session = MergeSession.from_state(record["session"])
        editor._completed_text = record["completed_text"]
        return editor
