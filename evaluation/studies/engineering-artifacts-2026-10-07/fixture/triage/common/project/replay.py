"""Deterministic completion scheduler; no sleeps, network, or wall-clock races."""
from controller import Controller


def replay(actions):
    product = Controller()
    observations = {}
    for action in actions:
        op = action['op']
        if op == 'reset': product.reset()
        elif op == 'edit': product.edit(action['field'], action['value'])
        elif op == 'save': product.save(action['field'], action['request'])
        elif op == 'complete': product.complete(action['request'])
        elif op == 'observe': observations[action['name']] = product.snapshot()
    return observations
