"""Bounded declarative reproduction format; executable strings are never evaluated."""
from bounded_json import exact, bounded_text, reject


def value(field, item):
    if field == 'title': bounded_text(item, 32)
    elif field == 'limit':
        if type(item) is not int or not 0 <= item <= 100: reject('invalid limit')
    else: reject('unknown field')


def snapshot(item):
    exact(item, ('saved', 'draft', 'pending', 'notice'))
    for key in ('saved', 'draft'):
        exact(item[key], ('title', 'limit'))
        for field in ('title', 'limit'): value(field, item[key][field])
    if type(item['pending']) is not list or len(item['pending']) > 12: reject('pending bound')
    for request in item['pending']: bounded_text(request, 32)
    if len(set(item['pending'])) != len(item['pending']): reject('duplicate pending request')
    if item['notice'] is not None: bounded_text(item['notice'], 96)


def validate(payload):
    exact(payload, ('version', 'scenarios', 'brief'))
    if type(payload['version']) is not int or payload['version'] != 1: reject('unsupported version')
    scenarios = payload['scenarios']
    if type(scenarios) is not list or not 1 <= len(scenarios) <= 6: reject('require 1..6 scenarios')
    ids = set()
    for scenario in scenarios:
        exact(scenario, ('id', 'purpose', 'actions', 'claims'))
        bounded_text(scenario['id'],48)
        if scenario['id'] in ids: reject('duplicate scenario id')
        ids.add(scenario['id'])
        if scenario['purpose'] not in ('reported', 'normal', 'reset', 'additional'): reject('invalid purpose')
        actions = scenario['actions']
        if type(actions) is not list or not 1 <= len(actions) <= 48: reject('action bound')
        if actions[0] != {'op':'reset'}: reject('each scenario must begin with explicit reset')
        used, pending, observations = set(), set(), set()
        for action in actions:
            if type(action) is not dict: reject('invalid action')
            op = action.get('op')
            if op == 'reset':
                exact(action, ('op',)); used, pending = set(), set()
            elif op == 'edit':
                exact(action, ('op','field','value')); value(action['field'],action['value'])
            elif op == 'save':
                exact(action, ('op','field','request'))
                if action['field'] not in ('title','limit'): reject('unknown field')
                bounded_text(action['request'],32)
                if action['request'] in used: reject('request alias reused without reset')
                used.add(action['request']); pending.add(action['request'])
                if len(pending) > 12: reject('too many pending requests')
            elif op == 'complete':
                exact(action, ('op','request')); bounded_text(action['request'],32)
                if action['request'] not in pending: reject('completion needs live request')
                pending.remove(action['request'])
            elif op == 'observe':
                exact(action, ('op','name')); bounded_text(action['name'],32)
                if action['name'] in observations: reject('observation name reused')
                observations.add(action['name'])
            else: reject('unknown operation')
        claims = scenario['claims']
        if type(claims) is not list or not 1 <= len(claims) <= 12: reject('claim bound')
        names = set()
        for claim in claims:
            exact(claim, ('observation','expected','predicted'))
            bounded_text(claim['observation'],32)
            if claim['observation'] not in observations or claim['observation'] in names:
                reject('claim must refer to one unique observation')
            names.add(claim['observation']); snapshot(claim['expected']); snapshot(claim['predicted'])
        if names != observations: reject('every observation requires one claim')
    brief = payload['brief']
    exact(brief, ('disposition','data_loss_reproduced','display_proves_data_loss','scope',
                  'root_cause','product_change_required','evidence_basis','summary','next_check'))
    if brief['disposition'] not in ('reproduced','not_reproduced','unrun'): reject('invalid disposition')
    for key in ('data_loss_reproduced','display_proves_data_loss','product_change_required'):
        if type(brief[key]) is not bool: reject('claim must be boolean')
    if brief['scope'] not in ('supplied_fixture_only','all_environments'): reject('invalid scope')
    if brief['root_cause'] not in ('not_established','save_order_data_loss','other'): reject('invalid cause')
    if brief['evidence_basis'] != 'source_derived_replay_claims': reject('invalid evidence basis')
    for key in ('summary','next_check'): bounded_text(brief[key],1000)
    return scenarios, brief
