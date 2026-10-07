"""Synthetic independent-field editor, revision controller-fixture-1."""
from copy import deepcopy

class Controller:
    def __init__(self):
        self.reset()

    def reset(self):
        self.saved = {'title': 'Base', 'limit': 5}
        self.draft = dict(self.saved)
        self.pending = {}
        self.generation = {'title': 0, 'limit': 0}
        self.applied = {'title': 0, 'limit': 0}
        self.notice = None

    def edit(self, field, value):
        self.draft[field] = value

    def save(self, field, request):
        self.generation[field] += 1
        self.pending[request] = (field, self.draft[field], self.generation[field])

    def complete(self, request):
        field, value, generation = self.pending.pop(request)
        if generation >= self.applied[field]:
            self.saved[field] = value
            self.applied[field] = generation
        self.notice = f'Saved {field}: {value}'

    def snapshot(self):
        return deepcopy({'saved': self.saved, 'draft': self.draft,
                         'pending': list(self.pending), 'notice': self.notice})
