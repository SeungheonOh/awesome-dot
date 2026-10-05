#!/usr/bin/env python3
"""Local stdlib checks. These do not run or validate a semantic reviewer."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from grade import grade

HERE = Path(__file__).resolve().parent
PACKET = HERE.parents[1]/'cases/F4'
REFERENCE = HERE/'reference'


class F4Checks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='f4-check-')
        self.work = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def report(self, packet=PACKET, submission=REFERENCE, semantic=True):
        review = submission/'semantic.json' if semantic is True else semantic
        return grade(packet, submission, review)

    def review_copy(self):
        return json.loads((REFERENCE/'semantic.json').read_text())

    def write_review(self, record):
        dest = self.work/'semantic.json'
        dest.write_text(json.dumps(record))
        return dest

    def packet_copy(self):
        dest = self.work/'packet'
        shutil.copytree(PACKET, dest)
        return dest

    def assert_integrity_failed(self, report):
        self.assertFalse(report['integrity']['passed'])
        self.assertFalse(report['accepted'])

    def test_01_reference_with_synthetic_scores(self):
        report = self.report()
        self.assertTrue(report['integrity']['passed'])
        self.assertTrue(report['accepted'])
        self.assertEqual(report['quality'], {'passed_groups':5,'scored_groups':5,'total_groups':5})
        self.assertEqual(len((REFERENCE/'decision-brief.txt').read_text().split()), 288)

    def test_02_reference_without_review_stays_pending(self):
        report = self.report(semantic=None)
        self.assertTrue(report['integrity']['passed'])
        self.assertIsNone(report['accepted'])
        self.assertTrue(all(g['passed'] is None for g in report['groups']))
        self.assertEqual(report['quality'], {'passed_groups':0,'scored_groups':0,'total_groups':5})

    def test_03_all_control_expected_outcomes(self):
        index = json.loads((HERE/'controls/control-index.json').read_text())
        covered = set()
        for control in index['controls']:
            with self.subTest(control=control['id']):
                report = self.report(submission=HERE/'controls'/control['id'])
                self.assertEqual(report['integrity']['passed'], control['expected_integrity'])
                self.assertEqual(report['accepted'], control['expected_accepted'])
                failed = [g['id'] for g in report['groups'] if g['passed'] is False]
                self.assertEqual(failed, control['expected_failed_groups'])
                covered.update(failed)
        self.assertEqual(covered, {'g1','g2','g3','g4','g5'})

    def test_04_independent_integer_cost_key(self):
        oracle = json.loads((HERE/'oracle-costs.json').read_text())
        annual = {}
        for row in oracle['candidates']:
            computed = oracle['users']*row['seat_cents_per_month'] + row['organization_module_cents_per_month']
            self.assertEqual(computed, row['monthly_cents'])
            self.assertEqual(computed*oracle['months'], row['annual_cents'])
            annual[row['application']] = computed*oracle['months']
        self.assertEqual(annual['AlderRoster']-annual['CedarShift'], oracle['conditional_annual_savings_cents'])

    def test_05_every_protected_file_byte_tamper_fails(self):
        frozen = json.loads((HERE/'frozen-packet-manifest.json').read_text())
        for entry in frozen['files']:
            with self.subTest(path=entry['path']):
                packet = self.work/('copy-' + entry['path'].replace('/','_'))
                shutil.copytree(PACKET, packet)
                changed = packet/entry['path']
                changed.write_bytes(changed.read_bytes()+b'\n')
                self.assert_integrity_failed(self.report(packet=packet))

    def test_06_missing_source_fails(self):
        packet = self.packet_copy()
        (packet/'inputs/04-beaconcrew-overview.txt').unlink()
        self.assert_integrity_failed(self.report(packet=packet))

    def test_07_extra_packet_file_fails(self):
        packet = self.packet_copy()
        (packet/'extra.txt').write_text('Extra protected-packet material')
        self.assert_integrity_failed(self.report(packet=packet))

    def test_08_source_symlink_fails(self):
        packet = self.packet_copy()
        changed = packet/'inputs/02-alderroster-community-3.4.txt'
        changed.unlink()
        changed.symlink_to(PACKET/'inputs/02-alderroster-community-3.4.txt')
        self.assert_integrity_failed(self.report(packet=packet))

    def test_09_missing_empty_and_non_utf8_report_fail(self):
        submission = self.work/'submission'; submission.mkdir()
        dest = submission/'decision-brief.txt'
        for content in (None,b'',b' \n\t',b'\xff\xfe'):
            with self.subTest(content=content):
                if content is not None:
                    dest.write_bytes(content)
                self.assert_integrity_failed(self.report(submission=submission,semantic=None))

    def test_10_report_symlink_fails(self):
        submission = self.work/'submission'; submission.mkdir()
        (submission/'decision-brief.txt').symlink_to(REFERENCE/'decision-brief.txt')
        self.assert_integrity_failed(self.report(submission=submission,semantic=None))

    def test_11_review_hash_mismatch_fails(self):
        record = self.review_copy(); record['submission_sha256']='0'*64
        self.assert_integrity_failed(self.report(semantic=self.write_review(record)))

    def test_12_duplicate_missing_extra_assertions_fail(self):
        for mode in ('duplicate','missing','extra'):
            with self.subTest(mode=mode):
                record = self.review_copy()
                values = record['groups'][0]['assertions']
                if mode == 'duplicate': values[1] = copy.deepcopy(values[0])
                elif mode == 'missing': values.pop()
                else: values.append({'id':'g1.extra','passed':True,'reason':'unrecognized'})
                self.assert_integrity_failed(self.report(semantic=self.write_review(record)))

    def test_13_integer_score_is_not_boolean(self):
        record = self.review_copy(); record['groups'][0]['assertions'][0]['passed']=1
        self.assert_integrity_failed(self.report(semantic=self.write_review(record)))

    def test_14_malformed_review_fails(self):
        dest = self.work/'broken.json'; dest.write_text('{bad json')
        self.assert_integrity_failed(self.report(semantic=dest))

    def test_15_partial_review_stays_pending(self):
        record = self.review_copy()
        record['groups'][0]['assertions'][0].update(passed=None, reason='')
        report = self.report(semantic=self.write_review(record))
        self.assertTrue(report['integrity']['passed'])
        self.assertIsNone(report['accepted'])
        self.assertEqual(report['quality'],{'passed_groups':4,'scored_groups':4,'total_groups':5})

    def test_16_failure_dominates_pending_review(self):
        record = self.review_copy()
        record['groups'][0]['assertions'][0].update(passed=None,reason='')
        record['groups'][1]['assertions'][0].update(passed=False,reason='Synthetic failure')
        report = self.report(semantic=self.write_review(record))
        self.assertFalse(report['accepted'])
        self.assertEqual(report['quality'],{'passed_groups':3,'scored_groups':4,'total_groups':5})

    def test_17_word_boundary_500_pass_501_fail(self):
        submission = self.work/'submission'; submission.mkdir()
        reference = (REFERENCE/'decision-brief.txt').read_text()
        for target in (500,501):
            with self.subTest(target=target):
                text = reference + '\n' + ' '.join(['extra']*(target-len(reference.split())))
                (submission/'decision-brief.txt').write_text(text)
                record = self.review_copy(); record['submission_sha256']=hashlib.sha256(text.encode()).hexdigest()
                report = self.report(submission=submission,semantic=self.write_review(record))
                self.assertTrue(report['integrity']['passed'])
                self.assertEqual(report['accepted'], target == 500)
                words = next(a for a in report['groups'][-1]['assertions'] if a['id']=='g5.words')
                self.assertEqual(words['passed'],target == 500)

    def test_18_overlong_without_review_is_failure_not_pending(self):
        report = self.report(submission=HERE/'controls/defect_objective_overlength',semantic=None)
        self.assertFalse(report['accepted'])
        self.assertEqual(report['quality'],{'passed_groups':0,'scored_groups':1,'total_groups':5})

    def test_19_generic_words_never_become_semantic_pass(self):
        submission = self.work/'submission'; submission.mkdir()
        (submission/'decision-brief.txt').write_text('eligible offline CSV AlderRoster correct recommendation prices uncertainty')
        report = self.report(submission=submission,semantic=None)
        self.assertTrue(report['integrity']['passed'])
        self.assertIsNone(report['accepted'])
        self.assertEqual(report['quality']['passed_groups'],0)

    def test_20_cli_json_report_and_exit(self):
        out = self.work/'result.json'
        result = subprocess.run([sys.executable,str(HERE/'grade.py'),'--packet',str(PACKET),
            '--submission',str(REFERENCE),'--semantic',str(REFERENCE/'semantic.json'),'--out',str(out)],
            check=True,text=True,capture_output=True)
        self.assertTrue(json.loads(out.read_text())['accepted'])
        self.assertTrue(json.loads(result.stdout)['accepted'])

    def test_21_score_reason_is_required(self):
        record = self.review_copy(); record['groups'][0]['assertions'][0]['reason']=' '
        self.assert_integrity_failed(self.report(semantic=self.write_review(record)))

    def test_22_review_case_and_group_ids_are_bound(self):
        for mode in ('case','group'):
            with self.subTest(mode=mode):
                record = self.review_copy()
                if mode=='case': record['case_id']='F9'
                else: record['groups'][0]['id']='g9'
                self.assert_integrity_failed(self.report(semantic=self.write_review(record)))

    def test_23_frozen_time_limit(self):
        metadata=json.loads((HERE/'case-metadata.json').read_text())
        self.assertEqual(metadata['frozen_time_limit_seconds'],900)

    def test_24_malformed_manifest_top_level_fails_safely(self):
        packet = self.packet_copy()
        for malformed in ([], None, True, 7, "not an object"):
            with self.subTest(malformed=malformed):
                (packet/'input-manifest.json').write_text(json.dumps(malformed))
                self.assert_integrity_failed(self.report(packet=packet))


if __name__ == '__main__':
    unittest.main(verbosity=2)
