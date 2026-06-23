from collections import OrderedDict

class AccountScheduler:
    def __init__(self, accounts, locked_until):
        self.locked_until = {}
        for ac in accounts:
            self.locked_until[ac] = locked_until.get(ac, 0)

        # OrderedDict tracks LRU order.
        # Elements are ordered from least-recently-used (start) to most-recently-used (end).
        self.lru = OrderedDict()
        for ac in accounts:
            self.lru[ac] = None

    def is_available(self, account_id, t):
        if account_id not in self.locked_until:
            return False
        return t >= self.locked_until[account_id]

    def acquire(self, account_id, t, duration):
        if not self.is_available(account_id, t):
            return False
        
        self.locked_until[account_id] = max(t, self.locked_until[account_id]) + duration
        self.lru.move_to_end(account_id)
        return True

    def auto_acquire(self, t, duration):
        # Iterate in LRU order
        for acc in list(self.lru):
            if self.is_available(acc, t):
                self.acquire(acc, t, duration)
                return acc
        return None
