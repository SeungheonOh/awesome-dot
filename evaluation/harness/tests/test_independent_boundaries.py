"""Owned synthetic regression checks only. No models, external services, or sandbox launches."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from dot_eval.core import IntegrityError, Ledger, create_json, digest, file_manifest, load_json
from dot_eval.execution import run_fixture
from dot_eval.grading import blind_export, import_grade
from dot_eval.protocol import freeze, initialize, prepare, schedule
from dot_eval.reporting import report
from dot_eval.telemetry import CodexEvents
import dot_eval

EXAMPLE = Path(dot_eval.__file__).parent.parent / 'examples/fixture_only'

class Boundaries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.assets = self.root / 'assets'
        shutil.copytree(EXAMPLE, self.assets)
        config = load_json(self.assets / 'config.json')
        config['tasks'] = [dict(config['tasks'][0], task_id=f'task{i}', family_id=f'F{i}') for i in range(2)]
        (self.assets / 'config.json').write_text(json.dumps(config))
        self.protocol = freeze(self.assets / 'config.json', self.root / 'frozen.json')
        self.plan = schedule(self.protocol, 42)
        self.study = initialize(self.protocol, self.plan, self.root / 'study')
    def tearDown(self):
        self.temp.cleanup()
    def grade_file(self, blind):
        path = self.root / 'grade.json'
        create_json(path, {'blind_id': blind['blind_id'], 'submission_sha256': blind['submission_sha256'],
            'integrity': {'passed': True}, 'groups': [{'id': f'g{i}', 'passed': True} for i in range(1,6)]})
        return path
    def test_report_rejects_changed_frozen_protocol(self):
        path = self.study / 'protocol.json'
        protocol = load_json(path)
        protocol['tasks'][0]['criteria'][0] = 'changed-criterion'
        path.write_text(json.dumps(protocol))
        with self.assertRaises(IntegrityError):
            report(self.study)
    def test_report_rejects_valid_ledger_prefix_missing_planned_block(self):
        ledger = self.study / 'attempts.jsonl'
        lines = ledger.read_bytes().splitlines(keepends=True)
        ledger.write_bytes(b''.join(lines[:2]))
        with self.assertRaises(IntegrityError):
            report(self.study)
    def test_initialize_rejects_self_hashed_incomplete_schedule(self):
        plan = copy.deepcopy(self.plan)
        plan['rows'] = plan['rows'][:2]
        plan['schedule_sha256'] = digest({k:v for k,v in plan.items() if k!='schedule_sha256'})
        with self.assertRaises(IntegrityError):
            initialize(self.protocol, plan, self.root/'incomplete-study')
    def test_blind_export_rejects_changed_frozen_rubric(self):
        run_fixture(self.study, 'a0001')
        (self.assets / 'rubric.txt').write_text('Changed after freeze, harmless fixture text')
        with self.assertRaises(IntegrityError):
            blind_export(self.study, 'a0001', self.root/'review')
    def test_import_grade_binds_blind_contract(self):
        run_fixture(self.study, 'a0001')
        blind = blind_export(self.study, 'a0001', self.root/'review')
        contract = self.root/'review'/blind['blind_id']/'blind.json'
        content = load_json(contract)
        content['instructions'] = 'Changed reviewer instruction after export'
        contract.write_text(json.dumps(content))
        with self.assertRaises(IntegrityError):
            import_grade(self.study, blind['blind_id'], self.grade_file(blind), 'fixture-reviewer')
    def test_fixture_validates_control_against_frozen_preparation_record(self):
        metadata = prepare(self.study, 'a0001')
        workspace = Path(metadata['workspace'])
        (workspace/'inputs/source.txt').write_text('Changed protected test input')
        metadata['source_manifest'] = file_manifest(workspace)
        (self.study/'control/a0001.json').write_text(json.dumps(metadata))
        with self.assertRaises(IntegrityError):
            run_fixture(self.study, 'a0001')
    def test_collection_failure_preserves_observed_timing_and_usage(self):
        metadata = prepare(self.study, 'a0001')
        real_manifest = file_manifest
        def controlled_manifest(path):
            if (Path(metadata['workspace']) / 'output/result.txt').exists():
                raise IntegrityError('Synthetic post-process collection rejection')
            return real_manifest(path)
        with patch('dot_eval.execution.file_manifest', controlled_manifest):
            result = run_fixture(self.study, 'a0001')
        self.assertEqual(result['status'], 'integrity_failed')
        self.assertIsNotNone(result['timing'])
        self.assertIsNotNone(result['usage'])
        self.assertEqual(result['usage']['input_tokens'], 11)
    def test_parser_rejects_trailing_unfinished_turn(self):
        parser = CodexEvents()
        for event in ({'type':'turn.started'}, {'type':'turn.completed','usage':{'input_tokens':1}}, {'type':'turn.started'}):
            parser.feed(json.dumps(event))
        self.assertFalse(parser.finish(0)['capture_complete'])
    def test_parser_does_not_retain_unrecognized_status_payload(self):
        parser = CodexEvents()
        parser.feed(json.dumps({'type':'item.completed','item':{'id':'synthetic','type':'reasoning',
            'status':{'unexpected_text':'PRIVATE_FIXTURE_CANARY'}}}))
        self.assertNotIn('PRIVATE_FIXTURE_CANARY', json.dumps(parser.safe_events)+json.dumps(parser.finish(0)))
    def test_parser_preserves_failure_across_duplicate_updates(self):
        parser = CodexEvents()
        for event in ({'type':'turn.started'},
            {'type':'item.completed','item':{'id':'synthetic','type':'command_execution','status':'failed','exit_code':1}},
            {'type':'item.updated','item':{'id':'synthetic','type':'command_execution','status':'in_progress'}},
            {'type':'turn.completed','usage':{'input_tokens':1}}):
            parser.feed(json.dumps(event))
        self.assertEqual(parser.finish(0)['failed_items'],1)

if __name__=='__main__':
    unittest.main(verbosity=2)
