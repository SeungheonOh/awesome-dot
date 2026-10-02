"""Original fictional product: completed additions must not be lost."""


class Tally:
    """One owner for one asynchronous store, used on one event loop."""

    def __init__(self, store):
        self.store = store

    async def add(self, actor, amount):
        current = await self.store.read(actor)
        await self.store.write(actor, current + amount)
