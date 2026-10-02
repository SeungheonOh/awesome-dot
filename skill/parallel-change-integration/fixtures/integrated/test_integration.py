from copy import deepcopy
import unittest

from queue_summary import summarize


class CombinedContractTests(unittest.TestCase):
    def test_fields_agree_and_calls_do_not_share_output(self):
        entries = [
            {"title": "Zebra", "minutes": 7},
            {"title": "Apple", "minutes": 0},
            {"title": "Zebra", "minutes": 4},
        ]
        before = deepcopy(entries)
        expected = {"titles": ["Zebra", "Apple", "Zebra"], "count": 3, "total_minutes": 11}
        first, second = summarize(entries), summarize(entries)
        self.assertEqual(first, expected)
        self.assertEqual(second, expected)
        self.assertEqual(first["count"], len(first["titles"]))
        first["titles"].append("Later")
        self.assertEqual(second, expected)
        self.assertEqual(summarize(entries), expected)
        self.assertEqual(entries, before)

    def test_combined_empty_result(self):
        self.assertEqual(summarize([]), {"titles": [], "count": 0, "total_minutes": 0})
