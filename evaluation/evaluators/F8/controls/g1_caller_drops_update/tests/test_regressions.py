import json
from pathlib import Path
import tempfile
import unittest
from card_editor import CardEditor
from merge_session import StaleChoiceError

def source(text, revision=0):
    return {"document_id": "regression-card", "revision": revision, "text": text}

class RegressionTests(unittest.TestCase):
    def test_revision_change_through_saved_caller(self):
        base, left, right = source("base\n"), source("left\n", 1), source("right\n", 2)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "card.json"
            editor = CardEditor(base, left, right)
            generation = editor.view()["generation"]
            editor.choose(0, "left", generation)
            self.assertEqual(editor.save(path)["completed_text"], "left\n")
            editor = CardEditor.load(path)
            editor.replace_sources(base, left, source("new right\n", 3))
            self.assertEqual(editor.view()["status"], "draft")
            with self.assertRaises(StaleChoiceError):
                editor.choose(0, "right", generation)
            record = editor.save(path)
            self.assertEqual(record["status"], "draft")
            self.assertEqual(record["text"], "base\n")
            self.assertEqual(record["completed_text"], "left\n")
            loaded = CardEditor.load(path)
            self.assertEqual(loaded.view(), editor.view())
            loaded.choose(0, "right", loaded.view()["generation"])
            self.assertEqual(loaded.save(path)["completed_text"], "new right\n")

    def test_unresolved_first_save_is_draft(self):
        editor = CardEditor(source("original\n"), source("left\n", 1), source("right\n", 2))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "new-card.json"
            record = editor.save(path)
            self.assertEqual(record["status"], "draft")
            self.assertIsNone(record["completed_text"])
            self.assertEqual(record, json.loads(path.read_text(encoding="utf-8")))
            loaded = CardEditor.load(path)
            self.assertEqual(loaded.view()["status"], "draft")
            self.assertEqual(loaded.view()["text"], "original\n")

if __name__ == "__main__":
    unittest.main()
