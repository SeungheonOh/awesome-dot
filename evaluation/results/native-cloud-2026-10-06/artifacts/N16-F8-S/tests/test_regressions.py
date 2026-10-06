"""Public-API regressions for source identity and the real JSON consumer.

Save/reload fixtures are local to output/.work/ and are cleaned after each test.
Expected text is specified independently of the implementation's merge primitive.
"""
from copy import deepcopy
import itertools
import json
from pathlib import Path
import tempfile
import unittest

from card_editor import CardEditor
from merge_session import MergeSession, StaleChoiceError


def source(text, revision=0, document_id="pump-card"):
    return {"document_id": document_id, "revision": revision, "text": text}


def conflict_sources():
    return (source("Inspect\nSet\n", 7),
            source("Inspect twice\nSet green\n", 2),
            source("Inspect daily\nSet blue\n", 2))


class RegressionTests(unittest.TestCase):
    def setUp(self):
        self.work = Path(__file__).resolve().parents[1] / ".work"
        self.work.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=self.work, prefix="regression-")
        self.path = Path(self.temporary.name) / "card.json"

    def tearDown(self):
        self.temporary.cleanup()
        # Another local check may also have a fixture under .work.
        if self.work.exists() and not any(self.work.iterdir()):
            self.work.rmdir()

    def read_record(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def assert_saved(self, editor, path=None):
        view = editor.view()
        state = editor.session.to_state()
        record = editor.save(self.path if path is None else path)
        self.assertEqual(record, self.read_record())
        self.assertEqual(record["format"], 1)
        self.assertEqual(record["session"], state)
        self.assertEqual(record["status"], view["status"])
        self.assertEqual(record["text"], view["text"])
        self.assertEqual(editor.view(), view)
        self.assertEqual(editor.session.to_state(), state)
        return record

    def test_revision_change_stale_choice_save_and_reload(self):
        snapshots = conflict_sources()
        editor = CardEditor(*snapshots)
        self.assertIsInstance(editor.session, MergeSession)
        token = editor.view()["generation"]
        editor.choose(index=0, side="left", generation=token)
        editor.choose(index=1, side="right", generation=token)
        completed = "Inspect twice\nSet blue\n"
        self.assertEqual(self.assert_saved(editor)["completed_text"], completed)
        editor = CardEditor.load(str(self.path))

        replacement = deepcopy(snapshots)
        replacement[2]["revision"] += 1  # Same alternatives, different source snapshot.
        editor.replace_sources(*replacement)
        self.assertEqual(editor.view()["generation"], token + 1)
        self.assertEqual(editor.view()["status"], "draft")
        self.assertEqual(editor.view()["text"], "Inspect\nSet\n")
        self.assertEqual([c["choice"] for c in editor.view()["conflicts"]], [None, None])
        self.assertEqual(editor.session.to_state()["choices"], [])
        before = editor.session.to_state()
        with self.assertRaises(StaleChoiceError):
            editor.choose(index=0, side="right", generation=token)
        self.assertEqual(editor.session.to_state(), before)

        record = self.assert_saved(editor, str(self.path))
        self.assertEqual(record["status"], "draft")
        self.assertEqual(record["completed_text"], completed)
        loaded = CardEditor.load(self.path)
        self.assertEqual(loaded.view(), editor.view())
        self.assertEqual(loaded.session.to_state(), editor.session.to_state())
        with self.assertRaises(StaleChoiceError):
            loaded.choose(0, "left", token)
        loaded.choose(0, "right", token + 1)
        loaded.choose(1, "left", token + 1)
        record = self.assert_saved(loaded)
        self.assertEqual(record["status"], "complete")
        self.assertEqual(record["completed_text"], "Inspect daily\nSet green\n")
        self.assertEqual(CardEditor.load(self.path).view(), loaded.view())

    def test_brand_new_unresolved_save_and_reload(self):
        editor = CardEditor(source("first\nmode\nlast\n"),
                            source("  left first\nvert\nlast\n", 1),
                            source("first\nbleu\n終わり \n", 1))
        initial = editor.view()
        self.assertEqual(initial["status"], "draft")
        self.assertEqual(initial["text"], "  left first\nmode\n終わり \n")
        self.assertEqual(initial["conflicts"], [
            {"index": 1, "base": "mode", "left": "vert", "right": "bleu", "choice": None}])
        record = self.assert_saved(editor)
        self.assertEqual(record["status"], "draft")
        self.assertIsNone(record["completed_text"])
        loaded = CardEditor.load(str(self.path))
        self.assertEqual(loaded.view(), initial)
        self.assertEqual(loaded.session.to_state(), editor.session.to_state())
        self.assertIsNone(self.assert_saved(loaded)["completed_text"])
        loaded.choose(1, "right", loaded.view()["generation"])
        record = self.assert_saved(loaded, str(self.path))
        self.assertEqual(record["status"], "complete")
        self.assertEqual(record["text"], "  left first\nbleu\n終わり \n")
        self.assertEqual(record["completed_text"], record["text"])

    def test_partial_choices_and_empty_alternative_survive_reload(self):
        editor = CardEditor(source("base\nstay\nfull\nend\n"),
                            source("left\nstay\n\nL end\n", 4),
                            source("right\nstay\nR full\nR end\n", 3))
        editor.choose(2, "left", 0)
        self.assertEqual(editor.view()["text"], "base\nstay\n\nend\n")
        self.assertEqual(editor.view()["status"], "draft")
        self.assertIsNone(self.assert_saved(editor)["completed_text"])
        loaded = CardEditor.load(self.path)
        self.assertEqual(loaded.view(), editor.view())
        self.assertEqual(loaded.session.to_state()["choices"], [{"index": 2, "side": "left"}])
        loaded.choose(3, "right", 0)
        loaded.choose(0, "left", 0)
        self.assertEqual(loaded.session.to_state()["choices"], [
            {"index": 0, "side": "left"}, {"index": 2, "side": "left"},
            {"index": 3, "side": "right"}])
        self.assertEqual(loaded.view()["text"], "left\nstay\n\nR end\n")
        self.assertEqual(self.assert_saved(loaded)["completed_text"], "left\nstay\n\nR end\n")

    def test_identical_sources_preserve_generation_and_choices(self):
        snapshots = conflict_sources()
        editor = CardEditor(*snapshots)
        changed = deepcopy(snapshots)
        changed[0]["revision"] = 8
        editor.replace_sources(*changed)
        token = editor.view()["generation"]
        editor.choose(1, "right", token)
        before = editor.view(), editor.session.to_state()
        editor.replace_sources(base=deepcopy(changed[0]), left=deepcopy(changed[1]),
                               right=deepcopy(changed[2]))
        self.assertEqual((editor.view(), editor.session.to_state()), before)
        editor.choose(0, "left", token)
        self.assertEqual(editor.view()["status"], "complete")

    def test_every_changed_snapshot_discards_all_choices(self):
        variants = []
        for branch in range(3):
            revision_change = deepcopy(conflict_sources())
            revision_change[branch]["revision"] += 1
            variants.append(("revision " + str(branch), revision_change))
            text_change = deepcopy(conflict_sources())
            text_change[branch]["text"] = "different\n" + text_change[branch]["text"].split("\n")[1] + "\n"
            variants.append(("text " + str(branch), text_change))
        variants.append(("line count", (source("a\nb\nc\n"),
                                        source("l\nb\nc\n"), source("r\nb\nc\n"))))
        variants.append(("conflicts disappear", (source("same\ntext\n"),) * 3))
        for label, replacement in variants:
            with self.subTest(change=label):
                editor = CardEditor(*conflict_sources())
                editor.choose(0, "left", 0)
                editor.choose(1, "right", 0)
                editor.replace_sources(*replacement)
                self.assertEqual(editor.view()["generation"], 1)
                self.assertEqual(editor.session.to_state()["choices"], [])
                self.assertTrue(all(c["choice"] is None for c in editor.view()["conflicts"]))
                with self.assertRaises(StaleChoiceError):
                    editor.choose(0, "left", 0)
                before = editor.session.to_state()
                editor.replace_sources(*deepcopy(replacement))
                self.assertEqual(editor.session.to_state(), before)

    def test_generation_tokens_are_strict_and_checked_first(self):
        editor = CardEditor(*conflict_sources())
        editor.choose(0, "left", 0)
        for token in (True, False, 0.0, "0", None, -1, 1, [], {}):
            with self.subTest(token=repr(token)):
                before = editor.view(), editor.session.to_state()
                with self.assertRaises(StaleChoiceError):
                    editor.choose(index=[], side="invalid", generation=token)
                self.assertEqual((editor.view(), editor.session.to_state()), before)
        self.assertTrue(issubclass(StaleChoiceError, ValueError))
        class IntegerSubclass(int):
            pass
        with self.assertRaises(StaleChoiceError):
            editor.choose(0, "left", IntegerSubclass(0))

    def test_current_invalid_choices_do_not_change_state(self):
        editor = CardEditor(source("B\nkeep\n"), source("L\nkeep\n"), source("R\nkeep\n"))
        editor.choose(0, "left", 0)
        invalid = [(1, "right"), (-1, "left"), (2, "left"), (True, "left"),
                   (False, "left"), (0.0, "left"), ("0", "left"), (None, "left"),
                   ([], "left"), ({}, "left"), (0, "base"), (0, "LEFT"),
                   (0, ""), (0, None), (0, []), (0, 1)]
        for index, side in invalid:
            with self.subTest(index=repr(index), side=repr(side)):
                before = editor.view(), editor.session.to_state()
                with self.assertRaises(ValueError):
                    editor.choose(index, side, 0)
                self.assertEqual((editor.view(), editor.session.to_state()), before)
        editor.choose(0, "right", 0)
        self.assertEqual(editor.view()["text"], "R\nkeep\n")
        self.assertEqual(editor.view()["conflicts"][0]["choice"], "right")

    def test_invalid_replacements_are_transactional(self):
        valid = conflict_sources()
        invalid_sources = [None, [], "not a source", {},
                           {"document_id": "pump-card", "revision": 0},
                           {**valid[0], "extra": "no"}]
        for field, values in (("document_id", ("", None, 1)),
                              ("revision", (-1, True, False, 1.0, "1", None)),
                              ("text", ("", "missing LF", "x\r\n", None, 3,
                                        "x\n" * 13, "single\n"))):
            invalid_sources.extend({**valid[0], field: value} for value in values)
        editor = CardEditor(*valid)
        editor.choose(0, "left", 0)
        for bad in invalid_sources:
            for branch in range(3):
                with self.subTest(source=repr(bad), branch=branch):
                    candidate = list(deepcopy(valid))
                    candidate[branch] = bad
                    before = editor.view(), editor.session.to_state()
                    with self.assertRaises(ValueError):
                        editor.replace_sources(*candidate)
                    self.assertEqual((editor.view(), editor.session.to_state()), before)
        other_document = tuple({**item, "document_id": "different-card"} for item in valid)
        before = editor.view(), editor.session.to_state()
        with self.assertRaises(ValueError):
            editor.replace_sources(*other_document)
        self.assertEqual((editor.view(), editor.session.to_state()), before)
        mismatch = deepcopy(valid)
        mismatch[1]["document_id"] = "different-card"
        with self.assertRaises(ValueError):
            editor.replace_sources(*mismatch)
        self.assertEqual((editor.view(), editor.session.to_state()), before)

    def test_invalid_construction_and_supported_boundaries(self):
        for text in ("", "no newline", "\r\n", "\n" * 13, None, 42):
            with self.subTest(text=repr(text)):
                with self.assertRaises(ValueError):
                    CardEditor(source(text), source(text), source(text))
        for text in ("\n", "\n" * 12, "é \n" * 12):
            with self.subTest(text=repr(text)):
                editor = CardEditor(source(text, 9), source(text, 1), source(text, 1))
                self.assertEqual(editor.view()["text"], text)
                self.assertEqual(editor.view()["status"], "complete")
                self.assertEqual(editor.view()["generation"], 0)

    def test_inputs_views_states_and_save_records_are_detached(self):
        snapshots = conflict_sources()
        editor = CardEditor(*snapshots)
        editor.choose(0, "left", 0)
        expected_view = editor.view()
        expected_state = editor.session.to_state()
        for snapshot in snapshots:
            snapshot["document_id"] = "mutated"
            snapshot["revision"] = 100
            snapshot["text"] = "mutated\n"
        view = editor.view()
        view["text"] = "mutated\n"
        view["conflicts"][0]["left"] = "mutated"
        view["conflicts"].clear()
        state = editor.session.to_state()
        state["sources"]["left"]["text"] = "mutated\n"
        state["choices"][0]["side"] = "right"
        state["generation"] = 100
        self.assertEqual(editor.view(), expected_view)
        self.assertEqual(editor.session.to_state(), expected_state)
        saved = self.assert_saved(editor)
        saved["session"]["sources"]["base"]["text"] = "mutated\n"
        saved["session"]["choices"].clear()
        saved["text"] = "mutated\n"
        saved["completed_text"] = "mutated\n"
        self.assertEqual(editor.view(), expected_view)
        self.assertEqual(editor.session.to_state(), expected_state)
        self.assertIsNone(self.assert_saved(editor)["completed_text"])

    def test_replacement_inputs_are_detached(self):
        editor = CardEditor(*conflict_sources())
        replacements = (source("B\n"), source("L\n"), source("R\n"))
        editor.replace_sources(*replacements)
        expected_view = editor.view()
        expected_state = editor.session.to_state()
        for snapshot in replacements:
            snapshot.clear()
        self.assertEqual(editor.view(), expected_view)
        self.assertEqual(editor.session.to_state(), expected_state)

    def test_session_state_round_trip_and_detached_restore(self):
        session = MergeSession(*conflict_sources())
        snapshots = conflict_sources()
        snapshots[0]["revision"] = 0
        session.replace_sources(*snapshots)
        session.choose(1, "right", 1)
        state = json.loads(json.dumps(session.to_state(), ensure_ascii=False))
        restored = MergeSession.from_state(state)
        self.assertEqual(restored.view(), session.view())
        self.assertEqual(restored.to_state(), session.to_state())
        state["sources"]["left"]["text"] = "corrupt\n"
        state["generation"] = 0
        state["choices"][0]["side"] = "left"
        self.assertEqual(restored.view(), session.view())
        self.assertEqual(restored.to_state(), session.to_state())
        restored.choose(0, "left", 1)
        self.assertEqual(restored.view()["status"], "complete")
        self.assertEqual(session.view()["status"], "draft")

    def test_automatic_merge_patterns_preserve_exact_text(self):
        cases = [
            (" \n\nété\n", " \n\nété\n", " \n\nété\n", " \n\nété\n"),
            ("\n", " left \n", "\n", " left \n"),
            ("base\n", "base\n", "右\n", "右\n"),
            ("base\n", "\n", "\n", "\n"),
            ("A\nB\nC\n", " 左 \nB\nC\n", "A\n\nC\n", " 左 \n\nC\n"),
            ("repeat\nrepeat\nrepeat\n", "L\nrepeat\nrepeat\n",
             "repeat\nrepeat\nR\n", "L\nrepeat\nR\n"),
        ]
        for base, left, right, expected in cases:
            with self.subTest(base=repr(base), left=repr(left), right=repr(right)):
                editor = CardEditor(source(base), source(left), source(right))
                self.assertEqual(editor.view()["text"], expected)
                self.assertEqual(editor.view()["status"], "complete")
                self.assertEqual(editor.view()["conflicts"], [])
                self.assertEqual(self.assert_saved(editor)["completed_text"], expected)
                self.assertEqual(CardEditor.load(self.path).view(), editor.view())

    def test_exhaustive_single_line_rules(self):
        for base, left, right in itertools.product(("", "same", "  é \t"), repeat=3):
            with self.subTest(base=base, left=left, right=right):
                editor = CardEditor(source(base + "\n"), source(left + "\n"), source(right + "\n"))
                if left == right:
                    expected = left
                elif left == base:
                    expected = right
                elif right == base:
                    expected = left
                else:
                    expected = None
                view = editor.view()
                self.assertEqual(set(view), {"document_id", "generation", "status", "text", "conflicts"})
                self.assertIs(type(view["generation"]), int)
                if expected is not None:
                    self.assertEqual(view["text"], expected + "\n")
                    self.assertEqual(view["conflicts"], [])
                    self.assertEqual(view["status"], "complete")
                else:
                    self.assertEqual(view["text"], base + "\n")
                    self.assertEqual(view["status"], "draft")
                    conflict = {"index": 0, "base": base, "left": left, "right": right, "choice": None}
                    self.assertEqual(view["conflicts"], [conflict])
                    for side, line in (("right", right), ("left", left)):
                        editor.choose(0, side, 0)
                        self.assertEqual(editor.view()["text"], line + "\n")
                        self.assertEqual(editor.view()["status"], "complete")
                        self.assertEqual(editor.view()["conflicts"], [{**conflict, "choice": side}])

    def test_repeated_lines_conflicts_stay_at_current_positions(self):
        editor = CardEditor(source("same\nsame\nsame\n"),
                            source("left\nsame\nleft\n"), source("right\nsame\nright\n"))
        self.assertEqual(editor.view()["conflicts"], [
            {"index": 0, "base": "same", "left": "left", "right": "right", "choice": None},
            {"index": 2, "base": "same", "left": "left", "right": "right", "choice": None}])
        editor.choose(2, "right", 0)
        editor.replace_sources(source("same\nsame\nsame\n"),
                               source("same\nleft\nleft\n"), source("same\nright\nright\n"))
        self.assertEqual(editor.view()["conflicts"], [
            {"index": 1, "base": "same", "left": "left", "right": "right", "choice": None},
            {"index": 2, "base": "same", "left": "left", "right": "right", "choice": None}])
        self.assertEqual(editor.view()["text"], "same\nsame\nsame\n")

    def test_completed_text_tracks_saves_not_resolutions(self):
        editor = CardEditor(*conflict_sources())
        editor.choose(0, "left", 0)
        editor.choose(1, "right", 0)
        # Reaching a complete view without saving is not a completed save.
        changed = deepcopy(conflict_sources())
        changed[1]["revision"] = 3
        editor.replace_sources(*changed)
        self.assertIsNone(self.assert_saved(editor)["completed_text"])
        editor.choose(0, "left", 1)
        editor.choose(1, "left", 1)
        self.assertEqual(self.assert_saved(editor)["completed_text"], "Inspect twice\nSet green\n")
        editor.choose(0, "right", 1)
        self.assertEqual(self.assert_saved(editor)["completed_text"], "Inspect daily\nSet green\n")
        editor = CardEditor.load(self.path)
        changed[2]["text"] = "New inspection\nNew setting\n"
        editor.replace_sources(*changed)
        editor.choose(0, "left", 2)
        draft = self.assert_saved(editor)
        self.assertEqual(draft["status"], "draft")
        self.assertEqual(draft["text"], "Inspect twice\nSet\n")
        self.assertEqual(draft["completed_text"], "Inspect daily\nSet green\n")
        loaded = CardEditor.load(self.path)
        self.assertEqual(self.assert_saved(loaded)["completed_text"], draft["completed_text"])


if __name__ == "__main__":
    unittest.main()
