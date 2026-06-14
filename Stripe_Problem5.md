Generate Account Email Notifications
Medium
Stripe
Software Engineer
Quick Overview
This question evaluates the ability to implement date-based rule evaluation, efficient filtering and ordering over large account lists, and template rendering with attention to algorithmic efficiency and correctness.

You are building an email notification scheduler for user accounts.

Given a current_day, a list of account records, and a list of notification rules, return all email notifications that should be sent on that day.

Each account is a dictionary with:

account_id: string
created_day: integer
expires_day: integer
Each rule is a dictionary with:

name: the email type
trigger: one of on_create, days_before_expiration, or after_expiration
offset_days: integer, only present when trigger == "days_before_expiration"
template: the message text to use verbatim
A rule matches an account when:

on_create: created_day == current_day
days_before_expiration: expires_day - current_day == offset_days
after_expiration: current_day > expires_day
Return the notifications in this order:

Accounts must be processed in the same order they appear in the input.
For a single account, if multiple rules match, their notifications must appear in the same order as the rules in the configuration.
Each returned notification must be a string formatted as: <account_id> <rule_name> <template>

If no rules match any account, return an empty list.

Examples
Example 1
Input
(10, [{"account_id": "A1", "created_day": 10, "expires_day": 30}, {"account_id": "A2", "created_day": 2, "expires_day": 13}, {"account_id": "A3", "created_day": 1, "expires_day": 8}], [{"name": "welcome", "trigger": "on_create", "template": "Welcome!"}, {"name": "three_day_reminder", "trigger": "days_before_expiration", "offset_days": 3, "template": "Your account expires in 3 days."}, {"name": "expired", "trigger": "after_expiration", "template": "Your account has expired."}])
Output
["A1 welcome Welcome!", "A2 three_day_reminder Your account expires in 3 days.", "A3 expired Your account has expired."]
Notes
A1 was created today, A2 expires in 3 days, and A3 is already expired.
Example 2
Input
(5, [], [{"name": "welcome", "trigger": "on_create", "template": "Welcome!"}])
Output
[]
Notes
There are no accounts, so no notifications are generated.
Constraints
0 <= len(accounts) <= 200000
0 <= len(rules) <= 200000
0 <= current_day, created_day, expires_day, offset_days <= 10^9
For every account, created_day <= expires_day
Each rule trigger is one of: `on_create`, `days_before_expiration`, `after_expiration`
The total number of generated notifications will not exceed 200000