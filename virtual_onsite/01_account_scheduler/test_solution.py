import unittest
from solution import AccountScheduler

class TestAccountScheduler(unittest.TestCase):
    def test_basic_availability_and_acquire(self):
        accounts = [1, 2, 3, 4]
        locked_until = {
            1: 10,
            2: 5,
            3: 0,
            4: 20
        }
        scheduler = AccountScheduler(accounts, locked_until)

        self.assertFalse(scheduler.is_available(1, 8))   # 8 < 10
        self.assertTrue(scheduler.is_available(2, 8))    # 8 >= 5
        self.assertTrue(scheduler.is_available(3, 1))    # 1 >= 0
        self.assertTrue(scheduler.is_available(4, 21))   # 21 >= 20

        # Explicit acquire
        self.assertTrue(scheduler.acquire(2, 8, 5))      # available, locks [8, 13)
        self.assertFalse(scheduler.is_available(2, 10))  # 10 < 13
        self.assertTrue(scheduler.is_available(2, 13))   # 13 >= 13

    def test_auto_acquire_lru(self):
        accounts = [1, 2, 3]
        locked_until = {
            1: 0,
            2: 0,
            3: 0
        }
        scheduler = AccountScheduler(accounts, locked_until)

        # Initial LRU order: 1, 2, 3
        # Auto acquire at t=0 for duration 10
        # Should pick 1 (first in LRU list)
        self.assertEqual(scheduler.auto_acquire(0, 10), 1)
        # Order is now: 2, 3, 1 (1 is MRU)

        # Auto acquire at t=0
        # 1 is locked until 10. 2 and 3 are available. 2 is oldest.
        self.assertEqual(scheduler.auto_acquire(0, 10), 2)
        # Order is now: 3, 1, 2

        # Auto acquire at t=5
        # 1 is locked until 10. 2 is locked until 10. 3 is available.
        self.assertEqual(scheduler.auto_acquire(5, 10), 3)
        # Order is now: 1, 2, 3

        # Auto acquire at t=10
        # All are available (locked_until are: 1->10, 2->10, 3->15)
        # 1 and 2 are available. LRU order: 1, 2, 3. 1 is oldest available.
        self.assertEqual(scheduler.auto_acquire(10, 5), 1)

if __name__ == '__main__':
    unittest.main()
