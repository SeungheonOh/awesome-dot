"""Independent event-history model, without importing or calling the product."""
from copy import deepcopy


def replay(actions):
    observations = {}
    base = {'title': 'Base', 'limit': 5}
    draft, jobs, history, notice = dict(base), {}, [], None
    for action in actions:
        op = action['op']
        if op == 'reset':
            draft, jobs, history, notice = dict(base), {}, [], None
        elif op == 'edit':
            draft[action['field']] = action['value']
        elif op == 'save':
            job = (action['field'], draft[action['field']], len(history))
            history.append({'job': job, 'done': False})
            jobs[action['request']] = job
        elif op == 'complete':
            field, value, order = jobs.pop(action['request'])
            history[order]['done'] = True
            notice = 'Saved ' + field + ': ' + str(value)
        elif op == 'observe':
            saved = dict(base)
            for item in history:
                if item['done']:
                    field, value, _ = item['job']
                    saved[field] = value
            observations[action['name']] = deepcopy({'saved': saved, 'draft': draft,
                                                     'pending': list(jobs), 'notice': notice})
    return observations
