"""Author-authored harness validation, never a candidate/model trial."""
from pathlib import Path
import copy
import importlib.util
import itertools
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from bounded_json import read_artifact, ArtifactError


def load(case, name):
    return json.loads((ROOT/case/'controls'/f'{name}.json').read_text())


def evaluate(case, payload=None, raw=None, setup=None):
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        target = root/'tests/cases.json' if case == 'exporter' else root/'reproduction.json'
        target.parent.mkdir(parents=True,exist_ok=True)
        if payload is not None: target.write_text(json.dumps(payload))
        if raw is not None: target.write_bytes(raw)
        if setup: setup(root,target)
        env = {key:value for key,value in os.environ.items() if not key.startswith('PYTHON')}
        p = subprocess.run([sys.executable,'-I','-B',str(ROOT/case/'trusted/grade.py'),str(root)],
                           capture_output=True,text=True,timeout=5,cwd=ROOT,env=env)
        if p.returncode != 0: raise AssertionError(f'grader crash: {p.stderr}')
        return json.loads(p.stdout)


class ExporterControls(unittest.TestCase):
    def test_strong_accepts_both_correct_and_kills_five(self):
        got=evaluate('exporter',load('exporter','strong'))
        self.assertTrue(got['all_required_outcomes'])
        self.assertEqual(got['executed_cases'],8)
        self.assertEqual(got['correct_program_failures'],{'correct_a':[],'correct_b':[]})
        self.assertEqual(sum(got['mutation_detection'].values()),5)

    def test_ordinary_green_suite_is_not_strong(self):
        got=evaluate('exporter',load('exporter','weak'))
        self.assertTrue(got['correct_program_specificity'])
        self.assertFalse(any(got['mutation_detection'].values()))

    def test_wrong_expectation_cannot_get_mutation_credit(self):
        got=evaluate('exporter',load('exporter','wrong_expectation'))
        self.assertFalse(got['correct_program_specificity'])
        self.assertTrue(any(got['raw_mutant_failures'].values()))
        self.assertFalse(any(got['mutation_detection'].values()))

    def test_core_only_misses_consumer_fault(self):
        got=evaluate('exporter',load('exporter','core_only'))
        self.assertTrue(got['correct_program_specificity'])
        self.assertEqual(sum(got['mutation_detection'].values()),4)
        self.assertFalse(got['mutation_detection']['consumer_filter_bypass'])

    def test_each_mutant_has_selective_witness(self):
        data=load('exporter','strong')
        expected={'repeated-occurrence':'duplicate_collapse','explicit-zero':'zero_as_missing',
                  'stable-order':'sort_instead_of_stable_order','mixed-selection':'consumer_filter_bypass'}
        for case in data['cases']:
            if case['id'] in expected:
                got=evaluate('exporter',{'version':1,'cases':[case]})
                self.assertEqual([key for key,v in got['mutation_detection'].items() if v],[expected[case['id']]])
        empty={'version':1,'cases':[{'id':'empty','entry_point':'export_rows','records':[],
                                   'expected':{'items':[]}}]}
        got=evaluate('exporter',empty)
        self.assertEqual([key for key,v in got['mutation_detection'].items() if v],['wrong_empty_representation'])

    def test_absent_empty_wrong_location_not_discovered(self):
        for setup in [None,lambda root,path: (root/'cases.json').write_text(json.dumps(load('exporter','strong')))]:
            self.assertFalse(evaluate('exporter',setup=setup)['discovery'])
        self.assertFalse(evaluate('exporter',{'version':1,'cases':[]})['discovery'])

    def test_public_runner_real_discovery(self):
        with tempfile.TemporaryDirectory() as td:
            project=Path(td)/'project'
            shutil.copytree(ROOT/'exporter/common/project',project)
            (project/'tests').mkdir(exist_ok=True)
            shutil.copyfile(ROOT/'exporter/controls/strong.json',project/'tests/cases.json')
            p=subprocess.run([sys.executable,'-I','-B','run_tests.py'],cwd=project,
                             text=True,capture_output=True,timeout=5)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(json.loads(p.stdout),{'discovered':True,'executed':8,'failed':[]})

    def test_untrusted_program_is_never_imported(self):
        with tempfile.TemporaryDirectory() as td:
            sentinel=Path(td)/'executed'
            def setup(root,target):
                for filename in ['exporter.py','correct_a.py','schema.py','sitecustomize.py','grade.py']:
                    (root/filename).write_text(f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('BAD')\nraise Exception('candidate code ran')\n")
            self.assertTrue(evaluate('exporter',load('exporter','strong'),setup=setup)['all_required_outcomes'])
            self.assertFalse(sentinel.exists())


class TriageControls(unittest.TestCase):
    def test_strong_bounded_non_reproduction(self):
        got=evaluate('triage',load('triage','strong'))
        self.assertTrue(got['all_required_outcomes'])
        self.assertEqual(got['executed_scenarios'],3)
        actual=got['state_checks'][1]['actual']
        self.assertEqual(actual,{'saved':{'title':'Nova','limit':0},'draft':{'title':'Nova','limit':0},
                                 'pending':[],'notice':'Saved title: Nova'})

    def test_honest_unrun_predictions_pass_without_execution_relabeling(self):
        got=evaluate('triage',load('triage','honest_unrun'))
        self.assertTrue(got['all_required_outcomes'])
        self.assertEqual(got['submitted_disposition'],'unrun')
        self.assertIn('candidate tool-execution provenance',got['unassessed'])

    def test_invented_bug_rejected_without_invalidating_replay(self):
        got=evaluate('triage',load('triage','invented_bug'))
        self.assertTrue(got['all_state_claims_correct'])
        self.assertFalse(any(got['structured_report_checks'].values()))
        self.assertFalse(got['all_required_outcomes'])

    def test_wrong_saved_data_rejected(self):
        got=evaluate('triage',load('triage','wrong_saved_claim'))
        self.assertFalse(got['all_state_claims_correct'])
        self.assertTrue(all(row['independent_expected_correct'] for row in got['state_checks']))

    def test_contract_expectation_independent_of_predicted_state(self):
        data=load('triage','strong')
        data['scenarios'][0]['claims'][-1]['expected']['saved']['limit']=5
        got=evaluate('triage',data)
        self.assertFalse(got['all_state_claims_correct'])
        self.assertTrue(all(row['predicted_state_correct'] for row in got['state_checks']))

    def test_label_is_not_saved_snapshot(self):
        got=evaluate('triage',load('triage','strong'))
        before,after=got['state_checks'][:2]
        self.assertNotEqual(before['actual']['notice'],after['actual']['notice'])
        self.assertEqual(before['actual']['saved']['limit'],0)
        self.assertEqual(after['actual']['saved']['limit'],0)

    def test_weak_neighbor_does_not_claim_report_coverage(self):
        got=evaluate('triage',load('triage','weak'))
        self.assertEqual(got['coverage'],{'reported_reverse_completion':False,
                                        'normal_forward_completion':True,'pending_reset_observed':False})
        self.assertFalse(got['all_required_outcomes'])

    def test_overclaim_rejected(self):
        got=evaluate('triage',load('triage','overclaim'))
        self.assertFalse(got['structured_report_checks']['bounded_conclusion'])

    def test_scenario_labels_alone_do_not_satisfy_coverage(self):
        data=load('triage','weak');data['scenarios'][0]['purpose']='reported'
        self.assertFalse(evaluate('triage',data)['coverage']['reported_reverse_completion'])

    def test_request_aliases_are_not_hardcoded(self):
        data=load('triage','strong')
        encoded=json.dumps(data).replace('title-save','request-A').replace('limit-save','request-B')
        self.assertTrue(evaluate('triage',json.loads(encoded))['all_required_outcomes'])

    def test_pending_reset_is_real_reset(self):
        data=load('triage','strong');data['scenarios'][2]['actions'][5]={'op':'observe','name':'not-reset'}
        data['scenarios'][2]['claims'].append({'observation':'not-reset','expected':data['scenarios'][2]['claims'][0]['expected'],
                                             'predicted':data['scenarios'][2]['claims'][0]['predicted']})
        got=evaluate('triage',data)
        self.assertFalse(got['coverage']['pending_reset_observed'])
        self.assertFalse(got['all_state_claims_correct'])

    def test_summary_semantics_explicitly_unassessed(self):
        data=load('triage','strong');data['brief']['summary']='This invented sentence intentionally contradicts the structured claims.'
        got=evaluate('triage',data)
        self.assertTrue(got['all_required_outcomes'])
        self.assertIn('summary prose semantics',got['unassessed'])

    def test_invalid_sequences_are_not_non_reproduction(self):
        for action in [{'op':'complete','request':'missing'},{'op':'sleep','seconds':1},
                       {'op':'edit','field':'limit','value':True}]:
            data=load('triage','strong');data['scenarios'][0]['actions'].insert(1,action)
            self.assertEqual(evaluate('triage',data)['status'],'invalid_artifact')


class CandidatePacketIntegrity(unittest.TestCase):
    def test_common_trusted_boundary_parity(self):
        pairs=[('bounded_json.py','exporter/common/project/bounded_json.py'),
               ('bounded_json.py','triage/common/project/bounded_json.py'),
               ('exporter/common/project/exporter.py','exporter/trusted/correct_a.py'),
               ('exporter/common/project/schema.py','exporter/trusted/schema.py'),
               ('triage/common/project/controller.py','triage/trusted/controller.py'),
               ('triage/common/project/replay.py','triage/trusted/replay.py'),
               ('triage/common/project/schema.py','triage/trusted/schema.py')]
        for source,target in pairs:
            self.assertEqual((ROOT/source).read_bytes(),(ROOT/target).read_bytes(),(source,target))

    def test_candidate_common_inventory_is_exact(self):
        expected={
            'exporter':{'PROMPT.md','project/README.md','project/bounded_json.py',
                        'project/exporter.py','project/schema.py','project/run_tests.py'},
            'triage':{'PROMPT.md','project/REPORT.md','project/CONTRACT.md','project/FORMAT.md',
                      'project/controller.py','project/replay.py','project/schema.py',
                      'project/replay_cli.py','project/bounded_json.py'}}
        for case,paths in expected.items():
            common=ROOT/case/'common'
            actual={str(p.relative_to(common)) for p in common.rglob('*') if p.is_file()}
            self.assertEqual(actual,paths)
            self.assertFalse(any(p.is_symlink() for p in common.rglob('*')))

    def test_candidate_common_excludes_hidden_sources(self):
        hidden=[ROOT/'exporter/trusted'/name for name in ['grade.py','correct_b.py','mutants.py']]
        hidden += [ROOT/'triage/trusted'/name for name in ['grade.py','oracle.py']]
        hidden += list((ROOT/'exporter/controls').glob('*.json'))
        hidden += list((ROOT/'triage/controls').glob('*.json'))
        denied=[p.read_bytes() for p in hidden]
        hidden_markers=[b'raw_mutant_failures',b'correct_program_specificity',b'from oracle import',
                        b'from correct_a import',b'import correct_b',b'all_required_outcomes']
        for case in ['exporter','triage']:
            for p in (ROOT/case/'common').rglob('*'):
                if p.is_file():
                    blob=p.read_bytes()
                    self.assertNotIn(blob,denied,str(p))
                    for marker in hidden_markers:self.assertNotIn(marker,blob,str(p))

    def test_isolated_public_triage_runner_contract_smoke(self):
        with tempfile.TemporaryDirectory() as td:
            project=Path(td)/'project'
            shutil.copytree(ROOT/'triage/common/project',project)
            shutil.copyfile(ROOT/'triage/controls/strong.json',project/'reproduction.json')
            env={key:value for key,value in os.environ.items() if not key.startswith('PYTHON')}
            p=subprocess.run([sys.executable,'-I','-B','replay_cli.py','reproduction.json'],
                             cwd=project,text=True,capture_output=True,timeout=5,env=env)
            self.assertEqual(p.returncode,0,p.stderr)
            actual=json.loads(p.stdout)
            self.assertEqual(actual,{
                'reverse':{
                    'partial':{'saved':{'title':'Base','limit':0},'draft':{'title':'Nova','limit':0},
                               'pending':['title-save'],'notice':'Saved limit: 0'},
                    'finished':{'saved':{'title':'Nova','limit':0},'draft':{'title':'Nova','limit':0},
                                'pending':[],'notice':'Saved title: Nova'}},
                'forward':{'finished':{'saved':{'title':'Nova','limit':0},'draft':{'title':'Nova','limit':0},
                                       'pending':[],'notice':'Saved limit: 0'}},
                'cancel-pending':{'fresh':{'saved':{'title':'Base','limit':5},'draft':{'title':'Base','limit':5},
                                         'pending':[],'notice':None}}})


class BoundedInputSafety(unittest.TestCase):
    def test_malformed_utf8_duplicate_keys_nonfinite_and_deep_json(self):
        invalid=[b'\xff',b'{',b'{"version":1,"version":1,"cases":[]}',b'NaN',b'Infinity',
                 b'['*20+b'0'+b']'*20,b'"' + b'x'*65536 + b'"',b'1'*5000]
        for case in ['exporter','triage']:
            for raw in invalid:
                self.assertFalse(evaluate(case,raw=raw)['discovery'],(case,raw[:30]))

    def test_oversized_sparse_file_rejected_before_full_read(self):
        def setup(root,path):
            with open(path,'wb') as f: f.truncate(100_000_000)
        self.assertFalse(evaluate('exporter',setup=setup)['discovery'])

    def test_symlink_file_and_parent_rejected(self):
        def file_link(root,path): path.symlink_to(ROOT/'exporter/controls/strong.json')
        def parent_link(root,path):
            path.parent.rmdir();other=root/'other';other.mkdir();(other/'cases.json').write_text(json.dumps(load('exporter','strong')));path.parent.symlink_to(other,target_is_directory=True)
        for setup in [file_link,parent_link]:
            self.assertFalse(evaluate('exporter',setup=setup)['discovery'])

    def test_fifo_nonblocking_and_directory_rejected(self):
        for setup in [lambda root,path:os.mkfifo(path),lambda root,path:path.mkdir()]:
            self.assertFalse(evaluate('exporter',setup=setup)['discovery'])

    def test_wrong_shapes_rejected_without_crash(self):
        for case in ['exporter','triage']:
            for payload in [[],None,True,1,{'version':1},{'version':1,'scenarios':None,'brief':{}}]:
                raw=json.dumps(payload).encode()
                self.assertFalse(evaluate(case,raw=raw)['discovery'])

    def test_unknown_keys_and_bounds_rejected(self):
        data=load('exporter','strong');data['cases'][0]['execute']='echo unauthorized'
        self.assertFalse(evaluate('exporter',data)['discovery'])
        data=load('exporter','strong');data['cases']=data['cases']*4
        self.assertFalse(evaluate('exporter',data)['discovery'])
        data=load('triage','strong');data['scenarios'][0]['actions']=[{'op':'reset'}]*49
        self.assertFalse(evaluate('triage',data)['discovery'])


def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


class IndependentOracleChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product=load_module('frozen_controller',ROOT/'triage/trusted/controller.py')
        cls.oracle=load_module('independent_oracle',ROOT/'triage/trusted/oracle.py')

    def product_replay(self,actions):
        c=self.product.Controller();out={}
        for a in actions:
            if a['op']=='reset':c.reset()
            elif a['op']=='edit':c.edit(a['field'],a['value'])
            elif a['op']=='save':c.save(a['field'],a['request'])
            elif a['op']=='complete':c.complete(a['request'])
            else:out[a['name']]=c.snapshot()
        return out

    def test_hand_calculated_same_field_reverse_completion(self):
        actions=[{'op':'reset'},{'op':'edit','field':'title','value':'Earlier'},
                 {'op':'save','field':'title','request':'a'},{'op':'edit','field':'title','value':'Later'},
                 {'op':'save','field':'title','request':'b'},{'op':'complete','request':'b'},
                 {'op':'complete','request':'a'},{'op':'observe','name':'final'}]
        expected={'final':{'saved':{'title':'Later','limit':5},'draft':{'title':'Later','limit':5},
                           'pending':[],'notice':'Saved title: Earlier'}}
        self.assertEqual(self.product_replay(actions),expected)
        self.assertEqual(self.oracle.replay(actions),expected)

    def test_all_24_four_save_completion_orders(self):
        start=[{'op':'reset'}]
        for alias,field,value in [('a','title','Early'),('b','limit',0),('c','title','Latest'),('d','limit',9)]:
            start += [{'op':'edit','field':field,'value':value},{'op':'save','field':field,'request':alias}]
        for order in itertools.permutations('abcd'):
            actions=copy.deepcopy(start)
            for n,alias in enumerate(order):actions += [{'op':'complete','request':alias},{'op':'observe','name':str(n)}]
            a,b=self.product_replay(actions),self.oracle.replay(actions)
            self.assertEqual(a,b)
            self.assertEqual(a['3']['saved'],{'title':'Latest','limit':9})

    def test_fixed_seed_500_mixed_scripts_with_resets(self):
        rng=random.Random(20261007)
        for _ in range(500):
            actions=[{'op':'reset'}];pending=[];counter=0
            for step in range(36):
                operation=rng.choice(['edit','save','complete','reset','observe'])
                field=rng.choice(['title','limit'])
                if operation=='edit':actions.append({'op':'edit','field':field,'value':rng.choice(['One','Two','Three']) if field=='title' else rng.choice([0,1,9])})
                elif operation=='save':
                    alias=f'q{counter}';counter+=1;pending.append(alias);actions.append({'op':'save','field':field,'request':alias})
                elif operation=='complete' and pending:
                    alias=rng.choice(pending);pending.remove(alias);actions.append({'op':'complete','request':alias})
                elif operation=='reset':pending=[];actions.append({'op':'reset'})
                elif operation=='observe':actions.append({'op':'observe','name':str(step)})
            actions.append({'op':'observe','name':'last'})
            self.assertEqual(self.product_replay(actions),self.oracle.replay(actions))


if __name__=='__main__':
    unittest.main(verbosity=2)
