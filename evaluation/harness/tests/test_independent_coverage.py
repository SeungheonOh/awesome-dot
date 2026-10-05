"""Independent fixture arithmetic, privacy, and collector boundary checks; no external execution."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from dot_eval.core import IntegrityError, file_manifest
from dot_eval.execution import RuntimeGateError, run_live
from dot_eval.reporting import summarize
from dot_eval.telemetry import CodexEvents

class Coverage(unittest.TestCase):
    def sample(self):
        outcomes=[(False,True),(False,True),(False,True),(True,False),(True,True),(True,True),(False,False),(None,True)]
        protocol={'tasks':[{'task_id':str(i),'family_id':str(i)} for i in range(8)],
            'stage':'exploratory_pilot','protocol_sha256':'synthetic-unit-test-only','analysis':{'bootstrap_enabled':True}}
        rows=[]
        for i,pair in enumerate(outcomes):
            for arm,accepted in zip(('C','S'),pair):
                rows.append({'task_id':str(i),'family_id':str(i),'arm':arm,'attempt_id':f'{i}{arm}', 'block_id':str(i),
                    'accepted':accepted,'quality_fraction':None if accepted is None else float(accepted),
                    'elapsed_s':2.0,'timeout_s':4.0,'attempted':True,'finished':True,'rater_count':0 if accepted is None else 1,
                    'status':'completed','evidence_kind':'model_attempt','usage':None})
        return rows,protocol
    def test_full_exploratory_math_and_missingness(self):
        rows,protocol=self.sample()
        result=summarize(rows,protocol)
        self.assertEqual(result['primary']['effect_estimate'],3/8)
        self.assertEqual(result['primary']['missing_outcome_contrast_bounds'],[2/8,3/8])
        self.assertEqual(result['primary']['leave_one_case_out_range'],[2/7,4/7])
        self.assertEqual(result['paired_acceptance_comparison'],{'S_wins':3,'ties_both_accepted':2,'ties_both_rejected':1,'S_losses':1,'unknown_pairs':1})
        self.assertIsNone(result['primary']['cluster_bootstrap'])
        self.assertIsNone(result['primary']['quality_delta_S_minus_C'])
        self.assertEqual(result['primary']['capped_time_to_accepted_delta_s'],-.75)
        self.assertEqual(result['coverage']['C']['scheduled'],8)
        self.assertEqual(result['coverage']['S']['scheduled'],8)
        self.assertEqual(result['coverage']['C']['outcome_unknown'],1)
        self.assertIsNone(result['billing']['actual_cost'])
    def test_not_run_sixteen_attempts_has_no_percent_effect(self):
        rows,protocol=self.sample()
        for row in rows:
            row.update(accepted=None,quality_fraction=None,elapsed_s=None,attempted=False,finished=False,rater_count=0,status='not_started',evidence_kind='not_executed')
        result=summarize(rows,protocol)
        self.assertEqual(result['study_status'],'not_run')
        self.assertEqual(result['paired_acceptance_comparison']['unknown_pairs'],8)
        self.assertIsNone(result['primary']['effect_estimate'])
        for arm in result['coverage'].values():
            self.assertEqual(arm['scheduled'],8)
            self.assertEqual(arm['outcome_unknown'],8)
            self.assertIsNone(arm['observed_accepted_fraction_of_scheduled'])
    def test_usage_subsets_separate_and_unverified(self):
        parser=CodexEvents()
        for event in ({'type':'turn.started'},{'type':'turn.completed','usage':{'input_tokens':100,'cached_input_tokens':30,'cache_write_input_tokens':20,'output_tokens':80,'reasoning_output_tokens':40}}):
            parser.feed(json.dumps(event))
        result=parser.finish(0)
        for key,value in {'input_tokens':100,'cached_input_tokens':30,'cache_write_input_tokens':20,'output_tokens':80,'reasoning_output_tokens':40}.items():
            self.assertEqual(result['usage'][key],value)
        self.assertIsNone(result['usage']['cross_category_total'])
        self.assertFalse(result['usage']['counter_semantics_verified'])
        self.assertIsNone(result['billing']['actual_cost'])
    def test_live_gate_ignores_unverified_config_assertions(self):
        with self.assertRaises(RuntimeGateError):
            run_live({'isolation_verified':True,'runtime_supported':True,'approved':True})
    def test_collector_rejects_ancestor_and_descendant_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'owned/child').mkdir(parents=True)
            (root/'owned/child/canary.txt').write_text('harmless owned fixture')
            (root/'alias').symlink_to(root/'owned',target_is_directory=True)
            with self.assertRaises(IntegrityError):
                file_manifest(root/'alias/child')
            (root/'output').mkdir()
            (root/'output/link').symlink_to(root/'owned',target_is_directory=True)
            with self.assertRaises(IntegrityError):
                file_manifest(root/'output')
    def test_collector_rejects_depth_and_entry_count_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            nested=root
            for _ in range(34):
                nested=nested/'d'
                nested.mkdir()
            with self.assertRaises(IntegrityError):
                file_manifest(root)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for i in range(10001):
                (root/f'empty{i:05d}').touch()
            with self.assertRaises(IntegrityError):
                file_manifest(root)

if __name__=='__main__':
    unittest.main(verbosity=2)
