import unittest
from solution import find_direct_links, find_links_within_two_hops, find_all_linked

class TestFindLinkedUsers(unittest.TestCase):
    def test_direct_links(self):
        rows = [
            {"id": 1, "name": "Alice", "email": "alice@gmail.com", "company": "Stripe"},
            {"id": 2, "name": "Alicia", "email": "alice@gmail.com", "company": "Stripe"},
            {"id": 3, "name": "Alice", "email": "alice@yahoo.com", "company": "Google"},
            {"id": 4, "name": "Bob", "email": "bob@gmail.com", "company": "Stripe"}
        ]
        weights = {
            "name": 0.2,
            "email": 0.5,
            "company": 0.3
        }
        threshold = 0.5
        # 1 and 2 share email(0.5) + company(0.3) = 0.8 -> direct
        # 1 and 3 share name(0.2) = 0.2 -> not direct
        # 1 and 4 share company(0.3) = 0.3 -> not direct
        self.assertEqual(find_direct_links(rows, weights, threshold, 1), [2])

    def test_two_hops_bug_scenario(self):
        # Build a graph structure:
        # 1 - 2 - 3 - 4
        # 1 - 3
        # Direct links:
        # 1: [2, 3]
        # 2: [1, 3]
        # 3: [1, 2, 4]
        # 4: [3]
        # Nodes within 2 hops from 1:
        # dist 1: 2, 3
        # dist 2: 4 (via 3)
        # Expected: {2, 3, 4}
        rows = [
            {"id": 1, "name": "Alice", "email": "alice@gmail.com", "company": "Stripe"},
            {"id": 2, "name": "Alice", "email": "alice@gmail.com", "company": "Google"},   # shares name+email (0.7) with 1
            {"id": 3, "name": "Bob", "email": "alice@gmail.com", "company": "Google"},     # shares email+company (0.8) with 2, shares email (0.5) with 1
            {"id": 4, "name": "Bob", "email": "bob@gmail.com", "company": "Google"},       # shares name+company (0.5) with 3
        ]
        weights = {
            "name": 0.2,
            "email": 0.5,
            "company": 0.3
        }
        threshold = 0.5 # 1-2(0.7), 1-3(0.5), 2-3(0.8), 3-4(0.5)
        # Verify direct links:
        self.assertCountEqual(find_direct_links(rows, weights, threshold, 1), [2, 3])
        self.assertCountEqual(find_direct_links(rows, weights, threshold, 2), [1, 3])
        self.assertCountEqual(find_direct_links(rows, weights, threshold, 3), [1, 2, 4])
        self.assertCountEqual(find_direct_links(rows, weights, threshold, 4), [3])

        # Verify 2-hop links: 4 should be reachable
        expected = {2, 3, 4}
        self.assertEqual(find_links_within_two_hops(rows, weights, threshold, 1), expected)

    def test_all_linked(self):
        rows = [
            {"id": 1, "name": "Alice", "email": "alice@gmail.com", "company": "Stripe"},
            {"id": 2, "name": "Alice", "email": "alice@gmail.com", "company": "Google"},
            {"id": 3, "name": "Bob", "email": "alice@gmail.com", "company": "Google"},
            {"id": 4, "name": "Carol", "email": "carol@gmail.com", "company": "Meta"},
            {"id": 5, "name": "Bob", "email": "bob@gmail.com", "company": "Google"},
        ]
        weights = {"name": 0.2, "email": 0.5, "company": 0.3}
        threshold = 0.7
        # 1 and 2: name+email = 0.7 >= 0.7 -> linked
        # 2 and 3: email+company = 0.8 >= 0.7 -> linked
        # 3 and 5: name+company = 0.5 < 0.7 -> not linked
        # So 1 is linked to 2, 2 to 3. Component containing 1 is {1, 2, 3}.
        # Target = 1, should return [2, 3] (excluding target itself, sorted).
        self.assertEqual(find_all_linked(rows, weights, threshold, 1), [2, 3])

if __name__ == '__main__':
    unittest.main()
