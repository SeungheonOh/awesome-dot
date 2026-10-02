from copy import deepcopy
import unittest

from queue_summary import summarize


class QueueContractTests(unittest.TestCase):
    def test_input_order_is_preserved(self):
        entries = [{"title": "Zebra", "minutes": 7}, {"title": "Apple", "minutes": 4}]
        self.assertEqual(summarize(entries)["titles"], ["Zebra", "Apple"])

    def test_empty_queue_has_empty_titles(self):
        self.assertEqual(summarize([])["titles"], [])

    def test_input_is_unchanged(self):
        entries = [{"title": "Zebra", "minutes": 7}, {"title": "Apple", "minutes": 4}]
        before = deepcopy(entries)
        summarize(entries)
        self.assertEqual(entries, before)
