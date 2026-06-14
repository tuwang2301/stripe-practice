from collections import *
import math

class AccountScheduler:
    def __init__(self, accounts, locked_until):
        self.accounts = defaultdict(int)
        for ac in accounts:
            self.accounts[ac] = 0

        for acc_id, loc in locked_until.items():
            self.accounts[acc_id] = loc

        self.lru = OrderedDict()
        for acc in self.accounts:
            self.lru[acc] = None

    def is_available(self, account_id, t):
        return t >= self.accounts[account_id]

    def acquire(self, account_id, t, duration):
        if not self.is_available(account_id, t):
            return False
        self.accounts[account_id] = max(t, self.accounts[account_id]) + duration
        self.lru.move_to_end(account_id)
        return True

    def auto_acquire(self, t, duration):
        for acc in list(self.lru):
            if self.is_available(acc, t):
                self.acquire(acc, t, duration)
                return acc
        return None

    # move_to_end('a') → b <-> c <-> a (MRU)
    # move_to_end('a', last=False) → a <-> b <-> c (move to front)
    # popitem(last=True) → pop c (MRU), returns ('c', 3)
    # popitem(last=False) → pop a (LRU), returns ('a', 1)
    # next(iter(od)) → 'a' (peek LRU, no pop)
    # next(reversed(od)) → 'c' (peek MRU, no pop)

if __name__ == "__main__":
    # logs = [(1, 'A', 404, 2), (1, 'A', 404, 1), (2, 'B', 500, 3), (3, 'A', 404, 1), (4, 'B', 500, 1)]
    logs = [(1, 'm1', 500, 2), (2, 'm1', 500, 2), (5, 'm1', 500, 1), (6, 'm1', 500, 1)]
    window_size = 3
    threshold = 4

    result = solution(logs=logs, window_size=window_size, threshold=threshold)
    print(result)
