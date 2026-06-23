# Problem 5: Generate Account Email Notifications

Build an email notification scheduler for user accounts.

## Inputs

- `current_day`: integer
- `accounts`: a list of account dictionaries:
  ```python
  {
      "account_id": "A1",
      "created_day": 10,
      "expires_day": 30
  }
  ```
- `rules`: a list of notification rule dictionaries:
  ```python
  {
      "name": "welcome",
      "trigger": "on_create",
      "template": "Welcome!"
  }
  ```
  Note: When `trigger == "days_before_expiration"`, it contains an `offset_days` integer.

## Match Rules

A rule matches an account when:
- `on_create`: `created_day == current_day`
- `days_before_expiration`: `expires_day - current_day == offset_days`
- `after_expiration`: `current_day > expires_day`

## Order of Outputs

1. Accounts must be processed in the same order they appear in the input list.
2. For a single account, if multiple rules match, their notifications must appear in the **same order as the rules in the configuration**.
3. Each returned notification must be formatted as: `<account_id> <rule_name> <template>`

If no rules match any account, return an empty list.
