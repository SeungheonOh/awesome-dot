"""Public-API regression tests, with real JSON round trips in local fixtures."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from card_editor import CardEditor
from merge_session import MergeSession, StaleChoiceError


def source(text, revision=0, document_id="pump-card"):
    return {"document_id": document_id, "revision": revision, "text": text}


def conflicting_sources():
    return (
        source("Inspect collar\nSet dial to amber\nStore card flat\n", 8),
        source("Inspect collar twice\nSet dial to green\nStore card flat\n", 3),
        source("Inspect collar\nSet dial to blue\nStore card in sleeve\n", 3),
    )


class RegressionTests(unittest.TestCase):
    def setUp(self):
        # Keep every temporary save inside this submission's temporary workspace.
        work = Path(__file__).resolve().parents[1] / ".work"
        work.mkdir(exist_ok=True)
        self._temporary = tempfile.TemporaryDirectory(prefix="regression-", dir=work)
        self.directory = Path(self._temporary.name)
        self.addCleanup(self._temporary.cleanup)

    def assert_saved_record(self, editor, path):
        before = editor.view()
        state = editor.session.to_state()
        record = editor.save(path)
        parsed = json.loads(Path(path).read_text(encoding="utf-8"))
        self.assertEqual(record, parsed)
        self.assertEqual(record["format"], 1)
        self.assertEqual(record["session"], state)
        self.assertEqual(record["status"], before["status"])
        self.assertEqual(record["text"], before["text"])
        self.assertEqual(editor.view(), before)
        self.assertEqual(editor.session.to_state(), state)
        return record

    def test_replacement_stale_choice_save_and_reload(self):
        sources = conflicting_sources()
        editor = CardEditor(*sources)
        self.assertIsInstance(editor.session, MergeSession)
        token = editor.view()["generation"]
        editor.choose(index=1, side="left", generation=token)
        completed = "Inspect collar twice\nSet dial to green\nStore card in sleeve\n"
        path = self.directory / "card.json"
        first = self.assert_saved_record(editor, path)
        self.assertEqual(first["status"], "complete")
        self.assertEqual(first["completed_text"], completed)
        editor = CardEditor.load(path)
        self.assertEqual(editor.view()["text"], completed)
        self.assertEqual(editor.session.to_state(), first["session"])

        # The alternatives have not changed: revision identity alone invalidates
        # both the old choice and the token that authorized it.
        changed = deepcopy(sources)
        changed[1]["revision"] += 1
        editor.replace_sources(base=changed[0], left=changed[1], right=changed[2])
        pending = editor.view()
        self.assertEqual(pending["generation"], token + 1)
        self.assertEqual(pending["status"], "draft")
        self.assertEqual(pending["conflicts"][0]["choice"], None)
        self.assertEqual(editor.session.to_state()["choices"], [])
        self.assertEqual(pending["text"], "Inspect collar twice\nSet dial to amber\nStore card in sleeve\n")
        with self.assertRaises(StaleChoiceError):
            editor.choose(index=1, side="right", generation=token)
        self.assertEqual(editor.view(), pending)
        draft = self.assert_saved_record(editor, str(path))
        self.assertEqual(draft["status"], "draft")
        self.assertEqual(draft["completed_text"], completed)

        restored = CardEditor.load(str(path))
        self.assertEqual(restored.view(), pending)
        self.assertEqual(restored.session.to_state(), draft["session"])
        second_draft = self.assert_saved_record(restored, path)
        self.assertEqual(second_draft["completed_text"], completed)
        restored.choose(index=1, side="right", generation=pending["generation"])
        final = self.assert_saved_record(restored, path)
        self.assertEqual(final["status"], "complete")
        self.assertEqual(final["completed_text"], "Inspect collar twice\nSet dial to blue\nStore card in sleeve\n")
        self.assertEqual(CardEditor.load(path).view(), restored.view())

    def test_brand_new_unresolved_save_and_reload(self):
        editor = CardEditor(*conflicting_sources())
        pending = editor.view()
        self.assertEqual(pending["status"], "draft")
        path = self.directory / "unresolved.json"
        record = self.assert_saved_record(editor, path)
        self.assertEqual(record["status"], "draft")
        self.assertIsNone(record["completed_text"])
        self.assertEqual(record["session"]["choices"], [])
        restored = CardEditor.load(path)
        self.assertEqual(restored.view(), pending)
        self.assertEqual(restored.session.to_state(), editor.session.to_state())
        self.assertIsNone(self.assert_saved_record(restored, path)["completed_text"])
        restored.choose(1, "left", restored.view()["generation"])
        complete = self.assert_saved_record(restored, path)
        self.assertEqual(complete["status"], "complete")
        self.assertEqual(complete["completed_text"], restored.view()["text"])

    def test_identical_sources_preserve_choices_and_generation(self):
        sources = conflicting_sources()
        editor = CardEditor(*sources)
        editor.choose(1, "right", 0)
        before = editor.view()
        state = editor.session.to_state()
        for _ in range(3):
            editor.replace_sources(*deepcopy(sources))
            self.assertEqual(editor.view(), before)
            self.assertEqual(editor.session.to_state(), state)
        editor.choose(1, "left", 0)
        self.assertEqual(editor.view()["conflicts"][0]["choice"], "left")

    def test_every_snapshot_change_invalidates_all_choices(self):
        original = (
            source("base zero\nbase one\n"),
            source("left zero\nleft one\n", 4),
            source("right zero\nright one\n", 2),
        )
        replacements = []
        for branch in range(3):
            changed = deepcopy(original)
            changed[branch]["revision"] += 1
            replacements.append(("revision-" + str(branch), changed))
            changed = deepcopy(original)
            changed[branch]["text"] = changed[branch]["text"].replace("zero", "new zero")
            replacements.append(("text-" + str(branch), changed))
        replacements.append(("line-count", (
            source("base zero\n"), source("left zero\n", 4), source("right zero\n", 2))))
        replacements.append(("automatic-line-added", (
            source("base zero\nbase one\nkeep\n"),
            source("left zero\nleft one\nkeep\n", 4),
            source("right zero\nright one\nkeep\n", 2))))
        for label, changed in replacements:
            with self.subTest(change=label):
                editor = CardEditor(*original)
                editor.choose(0, "left", 0)
                editor.choose(1, "right", 0)
                editor.replace_sources(*changed)
                self.assertEqual(editor.view()["generation"], 1)
                self.assertEqual(editor.session.to_state()["choices"], [])
                self.assertTrue(all(c["choice"] is None for c in editor.view()["conflicts"]))
                self.assertEqual(editor.view()["status"], "draft")
                before = editor.session.to_state()
                with self.assertRaises(StaleChoiceError):
                    editor.choose(0, "left", 0)
                self.assertEqual(editor.session.to_state(), before)
                editor.replace_sources(*deepcopy(changed))
                self.assertEqual(editor.view()["generation"], 1)
                editor.choose(0, "right", 1)
                editor.replace_sources(*original)
                self.assertEqual(editor.view()["generation"], 2)
                self.assertEqual(editor.session.to_state()["choices"], [])

    def test_generation_token_checked_first_and_exactly_int(self):
        editor = CardEditor(*conflicting_sources())
        self.assertTrue(issubclass(StaleChoiceError, ValueError))
        for token in [True, False, 0.0, "0", None, [], {}, -1, 1]:
            for index, side in [(1, "left"), (99, "neither")]:
                with self.subTest(token=token, index=index):
                    before = editor.session.to_state()
                    with self.assertRaises(StaleChoiceError):
                        editor.choose(index=index, side=side, generation=token)
                    self.assertEqual(editor.session.to_state(), before)
        editor.choose(1, "left", 0)
        changed = list(conflicting_sources())
        changed[2] = dict(changed[2], revision=20)
        editor.replace_sources(*changed)
        with self.assertRaises(StaleChoiceError):
            editor.choose(1, "right", True)
        editor.choose(1, "right", 1)

    def test_current_generation_invalid_choices_are_nonmutating(self):
        editor = CardEditor(*conflicting_sources())
        editor.choose(1, "left", 0)
        invalid = [(0, "left"), (2, "right"), (3, "left"), (-1, "left"),
                   (True, "left"), (1.0, "left"), ("1", "left"), (None, "left"),
                   ([], "left"), (1, None), (1, "base"), (1, "LEFT"), (1, [])]
        for index, side in invalid:
            with self.subTest(index=index, side=side):
                before = editor.session.to_state()
                view = editor.view()
                with self.assertRaises(ValueError):
                    editor.choose(index, side, 0)
                self.assertEqual(editor.session.to_state(), before)
                self.assertEqual(editor.view(), view)

    def test_invalid_sources_and_document_switch_leave_state_unchanged(self):
        originals = conflicting_sources()
        editor = CardEditor(*originals)
        editor.choose(1, "right", 0)
        invalid_sources = [None, [], "source", {},
                           {"document_id": "pump-card", "revision": 0},
                           dict(originals[0], extra=True),
                           dict(originals[0], document_id=""),
                           dict(originals[0], document_id=3),
                           dict(originals[0], revision=True),
                           dict(originals[0], revision=-1),
                           dict(originals[0], revision=0.0),
                           dict(originals[0], revision="0")]
        for text in [None, 1, "", "no newline", "with\r\n", "too few\n", "x\n" * 13]:
            invalid_sources.append(dict(originals[0], text=text))
        for bad in invalid_sources:
            for branch in range(3):
                with self.subTest(source=bad, branch=branch):
                    values = list(deepcopy(originals))
                    values[branch] = bad
                    before = editor.session.to_state()
                    with self.assertRaises(ValueError):
                        editor.replace_sources(*values)
                    self.assertEqual(editor.session.to_state(), before)
                    with self.assertRaises(ValueError):
                        MergeSession(*values)
        for values in [tuple(dict(s, document_id="another") for s in originals),
                       (dict(originals[0], document_id="another"), originals[1], originals[2])]:
            before = editor.session.to_state()
            with self.assertRaises(ValueError):
                editor.replace_sources(*values)
            self.assertEqual(editor.session.to_state(), before)

    def test_exact_automatic_text_including_empty_lines_and_unicode(self):
        cases = [
            ("unchanged", "  Inspect Ω  \n\nEnd \n", "  Inspect Ω  \n\nEnd \n", "  Inspect Ω  \n\nEnd \n", "  Inspect Ω  \n\nEnd \n"),
            ("left only", "base\n", "left \n", "base\n", "left \n"),
            ("right only", "base\n", "base\n", " 右\n", " 右\n"),
            ("identical edits", "base\n", "é\n", "é\n", "é\n"),
            ("independent", "base\n\nlast\n", "left\n\nlast\n", "base\n\n right \n", "left\n\n right \n"),
            ("single empty line", "\n", "\n", "\n", "\n"),
            ("two empty lines", "\n\n", "\n\n", "\n\n", "\n\n"),
            ("choose empty automatically", "base\n", "\n", "base\n", "\n"),
            ("unicode separators", "a\u2028b\n", "a\u2028b\n", "a\u2028b\n", "a\u2028b\n"),
            ("surrogate code point", "\ud800\n", "\ud800\n", "\ud800\n", "\ud800\n"),
            ("twelve lines", "\n" * 12, "\n" * 12, "\n" * 12, "\n" * 12),
        ]
        for label, base, left, right, expected in cases:
            with self.subTest(case=label):
                editor = CardEditor(source(base, 9), source(left, 2), source(right, 2))
                self.assertEqual(editor.view(), {"document_id": "pump-card", "generation": 0,
                                               "status": "complete", "text": expected, "conflicts": []})
                record = self.assert_saved_record(editor, self.directory / "exact.json")
                self.assertEqual(record["completed_text"], expected)
                self.assertEqual(CardEditor.load(self.directory / "exact.json").view(), editor.view())

    def test_conflicts_truthful_ordered_and_retained_after_choices(self):
        editor = CardEditor(source("base\nkeep\n\n"), source(" 左 \nkeep\nleft\n"),
                            source("\nkeep\n right \n"))
        expected = [{"index": 0, "base": "base", "left": " 左 ", "right": "", "choice": None},
                    {"index": 2, "base": "", "left": "left", "right": " right ", "choice": None}]
        self.assertEqual(editor.view()["conflicts"], expected)
        self.assertEqual(editor.view()["text"], "base\nkeep\n\n")
        editor.choose(2, "right", 0)
        expected[1]["choice"] = "right"
        self.assertEqual(editor.view()["conflicts"], expected)
        self.assertEqual(editor.view()["status"], "draft")
        self.assertEqual(editor.view()["text"], "base\nkeep\n right \n")
        editor.choose(0, "left", 0)
        editor.choose(0, "right", 0)
        expected[0]["choice"] = "right"
        self.assertEqual(editor.view()["conflicts"], expected)
        self.assertEqual(editor.view()["text"], "\nkeep\n right \n")
        self.assertEqual(editor.view()["status"], "complete")
        self.assertEqual(editor.session.to_state()["choices"],
                         [{"index": 0, "side": "right"}, {"index": 2, "side": "right"}])

    def test_positional_matching_does_not_relocate_conflicts(self):
        editor = CardEditor(source("a\nb\n"), source("b\na\n"), source("c\nd\n"))
        editor.choose(0, "left", 0)
        editor.choose(1, "right", 0)
        editor.replace_sources(source("b\na\n"), source("a\nb\n"), source("d\nc\n"))
        self.assertEqual(editor.view()["conflicts"], [
            {"index": 0, "base": "b", "left": "a", "right": "d", "choice": None},
            {"index": 1, "base": "a", "left": "b", "right": "c", "choice": None},
        ])
        self.assertEqual(editor.view()["text"], "b\na\n")
        self.assertEqual(editor.view()["generation"], 1)

    def test_input_view_state_and_save_results_are_detached(self):
        inputs = list(conflicting_sources())
        editor = CardEditor(*inputs)
        expected = editor.session.to_state()
        inputs[0]["text"] = "tampered\n"
        inputs[1]["document_id"] = "tampered"
        self.assertEqual(editor.session.to_state(), expected)
        replacements = list(conflicting_sources())
        replacements[0]["revision"] = 100
        editor.replace_sources(*replacements)
        expected = editor.session.to_state()
        replacements[2]["revision"] = 500
        self.assertEqual(editor.session.to_state(), expected)
        editor.choose(1, "left", 1)
        view = editor.view()
        expected_view = deepcopy(view)
        view["conflicts"][0]["choice"] = "right"
        view["conflicts"].clear()
        view["text"] = "tampered\n"
        self.assertEqual(editor.view(), expected_view)
        state = editor.session.to_state()
        expected_state = deepcopy(state)
        restored = MergeSession.from_state(state)
        state["sources"]["left"]["text"] = "tampered\n"
        state["choices"][0]["side"] = "right"
        state["generation"] = 99
        self.assertEqual(editor.session.to_state(), expected_state)
        self.assertEqual(restored.to_state(), expected_state)
        self.assertEqual(restored.view(), expected_view)
        path = self.directory / "detached.json"
        record = self.assert_saved_record(editor, path)
        record["session"]["sources"]["left"]["text"] = "tampered\n"
        record["session"]["choices"].clear()
        record["completed_text"] = "tampered\n"
        self.assertEqual(editor.session.to_state(), expected_state)
        self.assertEqual(CardEditor.load(path).view(), expected_view)
        self.assertEqual(self.assert_saved_record(editor, path)["completed_text"], expected_view["text"])

    def test_partial_choices_survive_json_and_finish_after_reload(self):
        editor = CardEditor(source("a\nb\nc\n"), source("l0\nl1\nl2\n"),
                            source("r0\nr1\nr2\n"))
        editor.replace_sources(source("a\nb\nc\n", 1), source("l0\nl1\nl2\n"),
                               source("r0\nr1\nr2\n"))
        editor.choose(2, "right", 1)
        editor.choose(0, "left", 1)
        state = editor.session.to_state()
        self.assertEqual(state["schema"], 1)
        self.assertEqual(state["choices"], [{"index": 0, "side": "left"}, {"index": 2, "side": "right"}])
        restored_session = MergeSession.from_state(json.loads(json.dumps(state)))
        self.assertEqual(restored_session.to_state(), state)
        self.assertEqual(restored_session.view(), editor.view())
        path = self.directory / "partial.json"
        draft = self.assert_saved_record(editor, path)
        self.assertEqual(draft["status"], "draft")
        self.assertIsNone(draft["completed_text"])
        restored = CardEditor.load(path)
        self.assertEqual(restored.session.to_state(), state)
        restored.choose(1, "right", 1)
        result = self.assert_saved_record(restored, path)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["text"], "l0\nr1\nr2\n")
        self.assertEqual(result["completed_text"], result["text"])

    def test_completed_text_tracks_saves_not_unsaved_complete_views(self):
        editor = CardEditor(source("old\n"), source("old\n"), source("old\n"))
        path = self.directory / "history.json"
        self.assertEqual(self.assert_saved_record(editor, path)["completed_text"], "old\n")
        editor.replace_sources(source("base\n"), source("left\n"), source("right\n"))
        editor.choose(0, "right", 1)
        self.assertEqual(editor.view()["status"], "complete")
        editor.replace_sources(source("new base\n"), source("new left\n"), source("new right\n"))
        draft = self.assert_saved_record(editor, path)
        self.assertEqual(draft["status"], "draft")
        self.assertEqual(draft["completed_text"], "old\n")
        restored = CardEditor.load(path)
        restored.choose(0, "left", 2)
        self.assertEqual(self.assert_saved_record(restored, path)["completed_text"], "new left\n")
        restored.replace_sources(source("new base\n", 1), source("new left\n"), source("new right\n"))
        self.assertEqual(self.assert_saved_record(restored, path)["completed_text"], "new left\n")

    def test_resolved_but_never_saved_does_not_become_last_completed_save(self):
        editor = CardEditor(*conflicting_sources())
        editor.choose(1, "left", 0)
        changed = list(conflicting_sources())
        changed[0]["revision"] += 1
        editor.replace_sources(*changed)
        record = self.assert_saved_record(editor, self.directory / "never-completed.json")
        self.assertEqual(record["status"], "draft")
        self.assertIsNone(record["completed_text"])

    def test_all_one_line_merge_relations(self):
        # Exhaustive small alphabet independently states the specified rule,
        # including empty strings and significant whitespace.
        values = ["", "x", " x "]
        for base in values:
            for left in values:
                for right in values:
                    with self.subTest(base=base, left=left, right=right):
                        editor = CardEditor(source(base + "\n"), source(left + "\n"), source(right + "\n"))
                        if left == right:
                            expected = left
                        elif left == base:
                            expected = right
                        elif right == base:
                            expected = left
                        else:
                            self.assertEqual(editor.view()["text"], base + "\n")
                            self.assertEqual(editor.view()["status"], "draft")
                            self.assertEqual(editor.view()["conflicts"], [{"index": 0, "base": base,
                                "left": left, "right": right, "choice": None}])
                            for side, expected in [("left", left), ("right", right)]:
                                editor.choose(0, side, 0)
                                self.assertEqual(editor.view()["text"], expected + "\n")
                                self.assertEqual(editor.view()["status"], "complete")
                            continue
                        self.assertEqual(editor.view()["text"], expected + "\n")
                        self.assertEqual(editor.view()["status"], "complete")
                        self.assertEqual(editor.view()["conflicts"], [])


if __name__ == "__main__":
    unittest.main()
