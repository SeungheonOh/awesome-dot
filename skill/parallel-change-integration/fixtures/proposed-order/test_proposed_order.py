import unittest

from queue_summary import summarize


class ProposedOrderTests(unittest.TestCase):
    def test_proposed_default_is_alphabetical(self):
        entries = [{"title": "Zebra", "minutes": 7}, {"title": "Apple", "minutes": 4}]
        self.assertEqual(summarize(entries)["titles"], ["Apple", "Zebra"])
