import unittest
from merge_primitive import merge_lines
from merge_session import MergeSession

def source(text, revision=0):
    return {"document_id": "sample-card", "revision": revision, "text": text}

class SmokeTests(unittest.TestCase):
    def test_minimal_primitive(self):
        parts = merge_lines("Check seal\n", "Check seal twice\n", "Check seal\n")
        self.assertEqual(parts[0]["automatic"], "Check seal twice")

    def test_unchanged(self):
        doc = source("Keep card dry\n")
        session = MergeSession(doc, doc, doc)
        self.assertEqual(session.view()["text"], doc["text"])
        self.assertEqual(session.view()["status"], "complete")

    def test_independent_lines(self):
        session = MergeSession(source("First\nSecond\n"), source("Left first\nSecond\n"),
                               source("First\nRight second\n"))
        self.assertEqual(session.view()["text"], "Left first\nRight second\n")

if __name__ == "__main__":
    unittest.main()
