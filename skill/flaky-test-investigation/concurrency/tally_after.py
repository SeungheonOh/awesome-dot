"""Scoped repair: serialize the complete read/modify/write operation."""

import asyncio


class Tally:
    """One owner for one asynchronous store, used on one event loop."""

    def __init__(self, store):
        self.store = store
        self._lock = asyncio.Lock()

    async def add(self, actor, amount):
        async with self._lock:
            current = await self.store.read(actor)
            await self.store.write(actor, current + amount)
