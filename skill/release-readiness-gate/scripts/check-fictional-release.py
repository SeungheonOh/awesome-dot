#!/usr/bin/env python3
"""Offline checks for one fictional packet; not a production release controller.

Reads only the adjacent checked-in fixture, uses no network/subprocesses, and
writes nothing. All test changes are deep-copied, in-memory synthetic evidence.
"""
import copy
import json
import math
from datetime import datetime, timedelta
from pathlib import Path
import re
import sys
import unittest

INPUT = Path(__file__).resolve().parents[1] / 'references/fictional-release-input.json'
IDENTITY_KEYS = ('release_id', 'source_commit', 'artifact_sha256', 'migration_sha256')


def instant(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.utcoffset() != timedelta(0):
        raise ValueError('This fixture requires explicit UTC timestamps')
    return parsed


def load_fixture():
    return json.loads(INPUT.read_text())


def validate_input(data):
    """Refuse inconsistent policy/mapping before issuing any recommendation."""
    candidate = data['candidate']
    if not all(candidate.get(k) for k in IDENTITY_KEYS):
        raise ValueError('Incomplete candidate identity')
    for key, width in [('source_commit', 40), ('artifact_sha256', 64), ('migration_sha256', 64)]:
        if not re.fullmatch(r'[0-9a-f]{' + str(width) + '}', candidate[key]):
            raise ValueError('Malformed candidate ' + key)
    gates = data['policy']['gates']
    ids = [gate['id'] for gate in gates]
    if len(ids) != len(set(ids)) or not ids:
        raise ValueError('Duplicate or empty policy gate list')
    if set(ids) != set(data['gate_evidence']):
        raise ValueError('Policy coverage mismatch')
    evidence = {item['id']: item for item in data['evidence']}
    if len(evidence) != len(data['evidence']):
        raise ValueError('Duplicate evidence identifier')
    mapped = []
    for gate in gates:
        if not gate['checks'] or type(gate['mandatory']) is not bool:
            raise ValueError('Incomplete gate definition')
        for rule in gate['checks'].values():
            if rule['op'] not in ('eq', 'lte'):
                raise ValueError('Unsupported check operator')
        for evidence_id in data['gate_evidence'][gate['id']]:
            if evidence_id not in evidence or evidence[evidence_id]['gate_id'] != gate['id']:
                raise ValueError('Missing or misfiled evidence')
            mapped.append(evidence_id)
    if len(mapped) != len(set(mapped)) or set(mapped) != set(evidence):
        raise ValueError('Unmapped or duplicate evidence mapping')
    exception_ids = [item['id'] for item in data['exception_records']]
    if len(exception_ids) != len(set(exception_ids)):
        raise ValueError('Duplicate exception identifier')
    if any(item['gate_id'] not in ids for item in data['exception_records']):
        raise ValueError('Exception names a gate outside policy')
    return evidence


def binding_errors(item, candidate):
    return ['candidate mismatch: ' + key for key in IDENTITY_KEYS
            if item.get('candidate', {}).get(key) != candidate[key]]


def metric_state(observed, rule):
    expected = rule['value']
    if type(expected) in (int, float):
        if type(observed) not in (int, float) or not math.isfinite(observed):
            return 'unknown'
    elif type(observed) is not type(expected):
        return 'unknown'
    passed = observed == expected if rule['op'] == 'eq' else observed <= expected
    return 'satisfied' if passed else 'failed'


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def assess_first_rollout_plan(data):
    """Validate this fixture's proposed first stage, not live rollout health."""
    scope = data['requested_scope']
    policy = data['policy']['stage_rules']['first_rollout']
    checks = []

    def record(name, state, reason):
        checks.append({'check': name, 'state': state, 'reason': reason})

    numeric_fields = ('cohort_pct', 'observation_minutes', 'reporting_lag_s',
                      'normal_p99_ms', 'exception_p99_ms', 'error_rate_pct',
                      'duplicate_deliveries', 'late_over_60s', 'queue_age_s')
    valid = {}
    for field in numeric_fields:
        value = policy.get(field)
        valid[field] = finite_number(value) and value >= 0
        if field in ('cohort_pct', 'observation_minutes'):
            valid[field] = valid[field] and value > 0
        if field == 'cohort_pct':
            valid[field] = valid[field] and value <= 100
        record('policy.' + field, 'satisfied' if valid[field] else 'unknown',
               'Finite, usable policy value supplied' if valid[field]
               else 'Missing or invalid stage policy value; owner must supply it')

    for field, expected in [('stage', 'first_rollout'),
                            ('environment', policy.get('environment'))]:
        actual = scope.get(field)
        state = ('unknown' if not actual or not expected else
                 'satisfied' if actual == expected else 'failed')
        record('scope.' + field, state, 'Must match the supplied first-rollout policy')
    cohort = scope.get('cohort_pct')
    state = ('unknown' if not finite_number(cohort) or not valid['cohort_pct'] else
             'satisfied' if cohort == policy['cohort_pct'] else 'failed')
    record('scope.cohort_pct', state, 'Requested cohort must equal the policy first group')

    starts, ends = None, None
    try:
        starts, ends = instant(scope['starts_at']), instant(scope['ends_at'])
    except (KeyError, TypeError, ValueError, AttributeError):
        record('scope.window', 'unknown', 'Complete UTC start/end timestamps are required')
    if starts is not None and ends is not None:
        if ends <= starts:
            record('scope.window', 'failed', 'End must follow start')
        elif valid['observation_minutes']:
            duration = (ends - starts).total_seconds() / 60
            record('scope.window', 'satisfied' if duration >= policy['observation_minutes'] else 'failed',
                   f'Planned {duration:g} minutes; policy minimum {policy["observation_minutes"]:g}')

    future_rule = policy.get('start_at_or_after_assessment')
    if type(future_rule) is not bool:
        record('scope.start_time', 'unknown', 'Policy must specify treatment of past proposed starts')
    elif future_rule and starts is not None:
        record('scope.start_time', 'satisfied' if starts >= instant(data['as_of']) else 'failed',
               'This fictional policy requires a new proposed start if the old one is past')

    state = ('failed' if any(check['state'] == 'failed' for check in checks) else
             'unknown' if any(check['state'] == 'unknown' for check in checks) else 'satisfied')
    return {'stage': 'first_rollout', 'kind': 'planning_only', 'state': state, 'checks': checks}


def exception_errors(record, data, gate, failures, eligible):
    policy = data['policy']['exceptions']
    scope = data['requested_scope']
    now = instant(data['as_of'])
    errors = binding_errors(record, data['candidate'])
    if record['policy_id'] != data['policy']['id']:
        errors.append('wrong policy')
    if gate['id'] != policy['allowed_gate'] or record['gate_id'] != gate['id']:
        errors.append('gate is not exception-eligible')
    if (set(record['failed_checks']) != failures
            or not failures <= set(policy['allowed_failed_checks'])):
        errors.append('failed-check scope is not permitted')
    if not record['approved_by'] or record['approver_role'] != policy['approver_role']:
        errors.append('unauthorized approver')
    approved, start, end = map(instant, (record['approved_at'], record['valid_from'], record['expires_at']))
    if not approved <= start <= now < end:
        errors.append('exception not yet valid or expired')
    if record['scope'] != scope:
        errors.append('requested scope differs from approved scope')
    if (scope.get('stage') != policy['allowed_stage']
            or not finite_number(scope.get('cohort_pct'))
            or scope['cohort_pct'] > policy['max_cohort_pct']):
        errors.append('stage or cohort exceeds policy')
    stage = data['policy']['stage_rules']['first_rollout']
    lag = stage.get('reporting_lag_s')
    if not finite_number(lag) or lag < 0:
        errors.append('reporting delay unavailable for exception-window validation')
    else:
        try:
            scope_start, scope_end = instant(scope['starts_at']), instant(scope['ends_at'])
            finish_observing = scope_end + timedelta(seconds=lag)
            if not start <= scope_start < scope_end <= finish_observing <= end:
                errors.append('exception does not cover rollout plus reporting lag')
        except (KeyError, TypeError, ValueError, AttributeError):
            errors.append('rollout timestamps incomplete or invalid')
    if any(record['mitigations'].get(key) is not True for key in policy['required_mitigations']):
        errors.append('required prepared mitigation missing')
    ceiling = record['p99_ceiling_ms']
    if type(ceiling) not in (int, float) or not math.isfinite(ceiling) or ceiling > policy['max_p99_ms']:
        errors.append('exception ceiling exceeds policy')
    else:
        for item in eligible:
            p99 = item['metrics'].get('p99_ms')
            if type(p99) not in (int, float) or not math.isfinite(p99) or p99 > ceiling:
                errors.append('observed p99 outside exception ceiling')
                break
    return errors


def assess(data):
    """Derive the fictional gate ledger, preserving raw failures and exclusions."""
    evidence = validate_input(data)
    now = instant(data['as_of'])
    rows = []
    for gate in data['policy']['gates']:
        audits, eligible, checks = [], [], []
        for evidence_id in data['gate_evidence'][gate['id']]:
            item = evidence[evidence_id]
            errors = binding_errors(item, data['candidate'])
            for field, expected in [('policy_id', data['policy']['id']),
                                    ('type', gate['evidence_type']),
                                    ('environment', gate['environment'])]:
                if item.get(field) != expected:
                    errors.append(field + ' mismatch')
            age = now - instant(item['ended_at'])
            if age < timedelta(0):
                errors.append('future timestamp')
            elif age > timedelta(hours=gate['max_age_hours']):
                errors.append('stale evidence')
            if item.get('complete') is not True:
                errors.append('incomplete export')
            audit = {'id': evidence_id, 'status': 'rejected' if errors else 'eligible', 'reasons': errors}
            if not errors:
                eligible.append(item)
                audit['checks'] = {name: metric_state(item['metrics'].get(name), rule)
                                   for name, rule in gate['checks'].items()}
                checks.extend(audit['checks'].items())
            audits.append(audit)
        failures = {name for name, state in checks if state == 'failed'}
        unknown = not eligible or any(state == 'unknown' for _, state in checks)
        raw = 'failed' if failures else 'unknown' if unknown else 'satisfied'
        state, applied, exceptions = raw, None, []
        if failures:
            for record in data['exception_records']:
                if record['gate_id'] != gate['id']:
                    continue
                errors = exception_errors(record, data, gate, failures, eligible)
                exceptions.append({'id': record['id'], 'reasons': errors})
                if not errors:
                    applied = record['id']
                    state = 'unknown' if unknown else 'satisfied_by_exception'
                    break
        rows.append({'gate_id': gate['id'], 'owner': gate['owner'], 'mandatory': gate['mandatory'],
                     'raw_state': raw, 'state': state, 'failed_checks': sorted(failures),
                     'applied_exception': applied, 'exception_checks': exceptions, 'evidence': audits})
    mandatory = [row for row in rows if row['mandatory']]
    plan = assess_first_rollout_plan(data)
    gate_failed = any(row['state'] == 'failed' for row in mandatory)
    gate_unknown = any(row['state'] == 'unknown' for row in mandatory)
    recommendation = ('hold' if gate_failed or plan['state'] == 'failed'
                      else 'unknown' if gate_unknown or plan['state'] == 'unknown'
                      else 'ready_for_owner_decision')
    blocking_stage = ('preparation' if gate_failed or gate_unknown else
                      'first_rollout' if plan['state'] != 'satisfied' else None)
    next_decision = ('Resolve failed and unknown mandatory gates and any blocked stage planning'
                     if gate_failed or gate_unknown else
                     'Correct or complete the first-rollout plan, then reassess the exact scope'
                     if plan['state'] != 'satisfied' else
                     'Release owner decides whether to authorize this exact first-rollout scope')
    return {'candidate': data['candidate'], 'as_of': data['as_of'], 'policy_id': data['policy']['id'],
            'scope': data['requested_scope'], 'advisory_only': True, 'recommendation': recommendation,
            'blocking_stage': blocking_stage, 'next_decision': next_decision,
            'gates': rows, 'stage_readiness': plan}


def gate_row(result, gate_id):
    return next(row for row in result['gates'] if row['gate_id'] == gate_id)


def item(data, evidence_id):
    return next(row for row in data['evidence'] if row['id'] == evidence_id)


def synthetic_recovery_success(data):
    """Counterfactual test evidence only; no real recovery or approval occurs."""
    evidence = item(data, 'E-RECOVERY-FAIL')
    evidence['metrics']['new_row_recovery_ok'] = True
    evidence['metrics']['data_owner_approved_strategy'] = True
    evidence['metrics']['migration_scope_and_old_reader_plan_verified'] = True
    evidence['reported_result'] = 'passed'
    evidence['notes'] = 'Synthetic alternative: approved forward-fix handles migrated and new rows.'


def synthetic_fresh_behavior(data):
    evidence = item(data, 'E-BHV-OLD')
    evidence['ended_at'] = '2026-10-01T11:50:00Z'
    evidence['notes'] = 'Synthetic rerun only; no live test ran.'


class PacketChecks(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(load_fixture())

    def test_base_hold_preserves_exception_and_recovery_failure(self):
        result = assess(self.data)
        self.assertEqual(result['recommendation'], 'hold')
        self.assertEqual(gate_row(result, 'G2')['state'], 'unknown')
        self.assertEqual(gate_row(result, 'G3')['raw_state'], 'failed')
        self.assertEqual(gate_row(result, 'G3')['state'], 'satisfied_by_exception')
        self.assertEqual(gate_row(result, 'G4')['state'], 'failed')
        self.assertEqual(result['blocking_stage'], 'preparation')

    def test_candidate_binding_and_stale_sources_are_excluded(self):
        audits = gate_row(assess(self.data), 'G2')['evidence']
        self.assertIn('stale evidence', audits[0]['reasons'])
        self.assertIn('candidate mismatch: artifact_sha256', audits[1]['reasons'])
        self.assertTrue(all(audit['status'] == 'rejected' for audit in audits))

    def test_same_release_label_does_not_override_different_artifact(self):
        other = item(self.data, 'E-BHV-OTHER')
        other['candidate'] = {**self.data['candidate'], 'artifact_sha256': 'a' * 64}
        self.assertEqual(gate_row(assess(self.data), 'G2')['state'], 'unknown')

    def test_each_identity_component_is_required(self):
        for key in IDENTITY_KEYS:
            with self.subTest(key=key):
                data = copy.deepcopy(self.data)
                item(data, 'E-BUILD-418')['candidate'][key] = 'wrong'
                self.assertEqual(gate_row(assess(data), 'G1')['state'], 'unknown')

    def test_missing_or_extra_policy_gate_mapping_is_rejected(self):
        for change in ('missing', 'extra'):
            with self.subTest(change=change):
                data = copy.deepcopy(self.data)
                if change == 'missing':
                    del data['gate_evidence']['G4']
                else:
                    data['gate_evidence']['NOT-IN-POLICY'] = []
                with self.assertRaisesRegex(ValueError, 'Policy coverage mismatch'):
                    assess(data)

    def test_expiry_is_exclusive(self):
        self.data['as_of'] = '2026-10-01T13:00:00Z'
        self.assertEqual(gate_row(assess(self.data), 'G3')['state'], 'failed')

    def test_exception_must_cover_reporting_lag(self):
        for scope in (self.data['requested_scope'], self.data['exception_records'][0]['scope']):
            scope['ends_at'] = '2026-10-01T12:59:00Z'
        self.assertEqual(gate_row(assess(self.data), 'G3')['state'], 'failed')

    def test_broader_cohort_and_later_stage_are_not_covered(self):
        for key, value in [('cohort_pct', 25), ('stage', 'expansion')]:
            with self.subTest(key=key):
                data = copy.deepcopy(self.data)
                data['requested_scope'][key] = value
                self.assertEqual(gate_row(assess(data), 'G3')['state'], 'failed')
                data['exception_records'][0]['scope'][key] = value
                result = gate_row(assess(data), 'G3')
                self.assertEqual(result['state'], 'failed')
                self.assertIn('stage or cohort exceeds policy', result['exception_checks'][0]['reasons'])

    def test_exception_cannot_waive_other_metrics_or_gate(self):
        item(self.data, 'E-LOAD-218')['metrics']['error_rate_pct'] = 0.2
        self.assertEqual(gate_row(assess(self.data), 'G3')['state'], 'failed')
        self.data['exception_records'][0]['gate_id'] = 'G4'
        result = gate_row(assess(self.data), 'G4')
        self.assertEqual(result['state'], 'failed')
        self.assertIn('gate is not exception-eligible', result['exception_checks'][0]['reasons'])

    def test_exception_authority_candidate_and_mitigations(self):
        variants = [('approver_role', 'Release reviewer'), ('policy_id', 'another-policy')]
        for field, value in variants:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data['exception_records'][0][field] = value
                self.assertEqual(gate_row(assess(data), 'G3')['state'], 'failed')
        self.data['exception_records'][0]['candidate']['artifact_sha256'] = 'f' * 64
        self.assertEqual(gate_row(assess(self.data), 'G3')['state'], 'failed')
        self.data = load_fixture()
        self.data['exception_records'][0]['mitigations']['prepared_queue_stop_guard'] = False
        self.assertEqual(gate_row(assess(self.data), 'G3')['state'], 'failed')

    def test_exception_ceiling_is_enforced(self):
        item(self.data, 'E-LOAD-218')['metrics']['p99_ms'] = 226
        self.assertEqual(gate_row(assess(self.data), 'G3')['state'], 'failed')

    def test_missing_future_and_incomplete_evidence_cannot_pass(self):
        for field, value in [('ended_at', '2026-10-01T12:01:00Z'), ('complete', False)]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                item(data, 'E-BUILD-418')[field] = value
                self.assertEqual(gate_row(assess(data), 'G1')['state'], 'unknown')
        del item(self.data, 'E-BUILD-418')['metrics']['unit_failures']
        self.assertEqual(gate_row(assess(self.data), 'G1')['state'], 'unknown')

    def test_boolean_or_nonfinite_latency_does_not_pass(self):
        for value in (True, float('nan'), float('inf')):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                item(data, 'E-LOAD-218')['metrics']['p99_ms'] = value
                self.assertEqual(gate_row(assess(data), 'G3')['state'], 'unknown')

    def test_hold_unknown_ready_transitions(self):
        self.assertEqual(assess(self.data)['recommendation'], 'hold')
        synthetic_recovery_success(self.data)
        self.assertEqual(assess(self.data)['recommendation'], 'unknown')
        synthetic_fresh_behavior(self.data)
        result = assess(self.data)
        self.assertEqual(result['recommendation'], 'ready_for_owner_decision')
        self.assertTrue(result['advisory_only'])
        self.assertEqual(result['scope']['cohort_pct'], 2)
        self.assertIsNone(result['blocking_stage'])

    def test_all_normal_gates_pass_without_using_exception(self):
        synthetic_recovery_success(self.data)
        synthetic_fresh_behavior(self.data)
        item(self.data, 'E-LOAD-218')['metrics']['p99_ms'] = 195
        item(self.data, 'E-LOAD-218')['reported_result'] = 'passed'
        item(self.data, 'E-LOAD-218')['notes'] = 'Synthetic normal-threshold success only.'
        result = assess(self.data)
        self.assertEqual(result['recommendation'], 'ready_for_owner_decision')
        self.assertIsNone(gate_row(result, 'G3')['applied_exception'])

    def test_first_rollout_window_must_meet_policy_minimum(self):
        synthetic_recovery_success(self.data)
        synthetic_fresh_behavior(self.data)
        self.assertEqual(assess(self.data)['recommendation'], 'ready_for_owner_decision')
        for scope in (self.data['requested_scope'], self.data['exception_records'][0]['scope']):
            scope['ends_at'] = '2026-10-01T12:11:00Z'
        result = assess(self.data)
        self.assertEqual(result['recommendation'], 'hold')
        self.assertEqual(result['blocking_stage'], 'first_rollout')
        self.assertEqual(result['stage_readiness']['state'], 'failed')
        self.assertTrue(any(check['check'] == 'scope.window' and check['state'] == 'failed'
                            for check in result['stage_readiness']['checks']))

    def test_blank_or_invalid_stage_thresholds_block_readiness(self):
        synthetic_recovery_success(self.data)
        synthetic_fresh_behavior(self.data)
        self.data['policy']['stage_rules']['first_rollout']['queue_age_s'] = None
        result = assess(self.data)
        self.assertEqual(result['recommendation'], 'unknown')
        self.assertEqual(result['blocking_stage'], 'first_rollout')
        for field in ('cohort_pct', 'observation_minutes', 'reporting_lag_s', 'normal_p99_ms',
                      'exception_p99_ms', 'error_rate_pct', 'duplicate_deliveries',
                      'late_over_60s', 'queue_age_s'):
            for value in (None, '', True, float('nan'), float('inf')):
                with self.subTest(field=field, value=value):
                    data = load_fixture()
                    synthetic_recovery_success(data)
                    synthetic_fresh_behavior(data)
                    data['policy']['stage_rules']['first_rollout'][field] = value
                    result = assess(data)
                    self.assertNotEqual(result['recommendation'], 'ready_for_owner_decision')
                    self.assertEqual(result['stage_readiness']['state'], 'unknown')

    def test_past_proposed_start_requires_rescoping_under_fixture_policy(self):
        synthetic_recovery_success(self.data)
        synthetic_fresh_behavior(self.data)
        for scope in (self.data['requested_scope'], self.data['exception_records'][0]['scope']):
            scope['starts_at'], scope['ends_at'] = '2026-10-01T11:55:00Z', '2026-10-01T12:25:00Z'
        result = assess(self.data)
        self.assertEqual(result['recommendation'], 'hold')
        self.assertEqual(result['blocking_stage'], 'first_rollout')
        self.assertTrue(any(check['check'] == 'scope.start_time' and check['state'] == 'failed'
                            for check in result['stage_readiness']['checks']))
        for scope in (self.data['requested_scope'], self.data['exception_records'][0]['scope']):
            scope['starts_at'], scope['ends_at'] = '2026-10-01T12:00:00Z', '2026-10-01T12:30:00Z'
        self.assertEqual(assess(self.data)['recommendation'], 'ready_for_owner_decision')

    def test_wrong_stage_scope_stays_blocked_without_an_exception(self):
        synthetic_recovery_success(self.data)
        synthetic_fresh_behavior(self.data)
        item(self.data, 'E-LOAD-218')['metrics']['p99_ms'] = 195
        item(self.data, 'E-LOAD-218')['reported_result'] = 'passed'
        for field, value in [('environment', 'another-environment'), ('stage', 'expansion'), ('cohort_pct', 25)]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data['requested_scope'][field] = value
                result = assess(data)
                self.assertEqual(result['recommendation'], 'hold')
                self.assertEqual(result['blocking_stage'], 'first_rollout')

    def test_passing_export_does_not_hide_current_failure(self):
        newer = copy.deepcopy(item(self.data, 'E-RECOVERY-FAIL'))
        newer['id'], newer['ended_at'] = 'E-RECOVERY-NEW', '2026-10-01T11:55:00Z'
        newer['metrics']['new_row_recovery_ok'] = True
        newer['metrics']['data_owner_approved_strategy'] = True
        newer['metrics']['migration_scope_and_old_reader_plan_verified'] = True
        newer['reported_result'] = 'passed'
        self.data['evidence'].append(newer)
        self.data['gate_evidence']['G4'].append(newer['id'])
        self.assertEqual(gate_row(assess(self.data), 'G4')['state'], 'failed')


if __name__ == '__main__':
    if sys.argv[1:] == ['--report']:
        print(json.dumps(assess(load_fixture()), indent=2))
    elif not sys.argv[1:]:
        unittest.main(verbosity=2)
    else:
        raise SystemExit('Usage: python scripts/check-fictional-release.py [--report]')
