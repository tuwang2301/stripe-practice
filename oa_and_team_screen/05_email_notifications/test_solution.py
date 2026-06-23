import unittest
from solution import solution

class TestEmailNotifications(unittest.TestCase):
    def test_sample_case_1(self):
        current_day = 10
        accounts = [
            {"account_id": "A1", "created_day": 10, "expires_day": 30},
            {"account_id": "A2", "created_day": 2, "expires_day": 13},
            {"account_id": "A3", "created_day": 1, "expires_day": 8}
        ]
        rules = [
            {"name": "welcome", "trigger": "on_create", "template": "Welcome!"},
            {"name": "three_day_reminder", "trigger": "days_before_expiration", "offset_days": 3, "template": "Your account expires in 3 days."},
            {"name": "expired", "trigger": "after_expiration", "template": "Your account has expired."}
        ]
        expected = [
            "A1 welcome Welcome!",
            "A2 three_day_reminder Your account expires in 3 days.",
            "A3 expired Your account has expired."
        ]
        self.assertEqual(solution(current_day, accounts, rules), expected)

    def test_multiple_matching_rules_order(self):
        current_day = 10
        accounts = [
            {"account_id": "A1", "created_day": 10, "expires_day": 10}
        ]
        # In this case:
        # created_day == current_day (on_create matches)
        # expires_day - current_day = 10 - 10 = 0 (days_before_expiration matches with offset_days=0)
        rules = [
            {"name": "reminder", "trigger": "days_before_expiration", "offset_days": 0, "template": "Expires today."},
            {"name": "welcome", "trigger": "on_create", "template": "Welcome!"}
        ]
        # Since reminder appears before welcome in the rules list,
        # reminder must be generated before welcome.
        expected = [
            "A1 reminder Expires today.",
            "A1 welcome Welcome!"
        ]
        self.assertEqual(solution(current_day, accounts, rules), expected)

if __name__ == '__main__':
    unittest.main()
