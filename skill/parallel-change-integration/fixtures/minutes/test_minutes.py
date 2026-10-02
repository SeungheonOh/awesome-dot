import unittest

from queue_summary import summarize


class MinutesTests(unittest.TestCase):
    def test_minutes_are_summed(self):
        entries = [{"title": "Zebra", "minutes": 7}, {"title": "Apple", "minutes": 4}]
        self.assertEqual(summarize(entries)["total_minutes"], 11)

    def test_zero_minute_entry_is_valid(self):
        self.assertEqual(summarize([{"title": "A", "minutes": 0}])["total_minutes"], 0)

    def test_empty_total_is_zero(self):
        self.assertEqual(summarize([])["total_minutes"], 0)
