import unittest

from queue_summary import summarize


class CountTests(unittest.TestCase):
    def test_count_includes_duplicate_titles(self):
        entries = [{"title": "Same", "minutes": 3}, {"title": "Same", "minutes": 0}]
        self.assertEqual(summarize(entries)["count"], 2)

    def test_empty_count_is_zero(self):
        self.assertEqual(summarize([])["count"], 0)
