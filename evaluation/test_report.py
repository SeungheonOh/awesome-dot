"""Local data/format tests. No model calls or submitted-code execution."""
import copy
import json
import unittest

import report


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.summary = json.loads((report.STUDY / 'results/summary.json').read_text())
        self.attempts = json.loads((report.STUDY / 'results/attempts.json').read_text())
        self.schedule = json.loads((report.STUDY / 'methods/schedule.json').read_text())
        self.rendered = report.tables(self.summary)
        self.docs = {'overview': (report.ROOT / 'README.md').read_text(),
                     'study': (report.STUDY / 'README.md').read_text()}

    def validate(self):
        report.validate(self.summary, self.attempts, self.schedule)

    def test_saved_inputs_and_current_docs(self):
        self.validate()
        report.check_docs(self.rendered, self.docs)

    def test_rejects_missing_attempt(self):
        self.attempts.pop()
        with self.assertRaisesRegex(ValueError, 'missing, extra, or duplicate attempt'):
            self.validate()

    def test_rejects_duplicate_attempt(self):
        self.attempts[-1] = copy.deepcopy(self.attempts[0])
        with self.assertRaisesRegex(ValueError, 'missing, extra, or duplicate attempt'):
            self.validate()

    def test_rejects_swapped_condition(self):
        self.attempts[0]['condition'] = 'C'
        with self.assertRaisesRegex(ValueError, 'condition or schedule mismatch'):
            self.validate()

    def test_rejects_stale_summary_count(self):
        self.summary['conditions']['S']['counts']['pass'] -= 1
        with self.assertRaisesRegex(ValueError, 'stale condition counts'):
            self.validate()

    def test_rejects_missing_requirement(self):
        self.attempts[0]['requirements'].pop()
        with self.assertRaises(ValueError):
            self.validate()

    def test_rejects_unknown_status(self):
        self.attempts[0]['requirements'][0]['status'] = 'pending'
        with self.assertRaisesRegex(ValueError, 'unknown requirement status'):
            self.validate()

    def test_rejects_stale_table(self):
        self.docs['overview'] = self.docs['overview'].replace('159/159', '158/159')
        with self.assertRaisesRegex(ValueError, 'stale or missing result table'):
            report.check_docs(self.rendered, self.docs)

    def test_rejects_swapped_table_labels(self):
        self.docs['overview'] = self.docs['overview'].replace('| With skill | Baseline |', '| Baseline | With skill |')
        with self.assertRaisesRegex(ValueError, 'stale or missing result table'):
            report.check_docs(self.rendered, self.docs)

    def test_rejects_absent_caveats_in_either_report(self):
        for name, guards in report.GUARDS.items():
            for text in guards:
                with self.subTest(document=name, caveat=text):
                    docs = self.docs.copy()
                    docs[name] = docs[name].replace(text, '')
                    with self.assertRaisesRegex(ValueError, 'missing condition definition or limitation'):
                        report.check_docs(self.rendered, docs)

    def test_preserves_zero_delta(self):
        for table in self.rendered.values():
            self.assertIn('| 159/159 | 159/159 | 0 |', table)


if __name__ == '__main__':
    unittest.main()
