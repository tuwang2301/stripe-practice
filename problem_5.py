from collections import defaultdict
import math

def solution(current_day, accounts, rules):
    # Group rules to different buckets
    on_create_rules = []
    after_expiration = []
    days_before_expiration = defaultdict(list)

    for rule in rules:
        if rule["trigger"] == 'on_create':
            on_create_rules.append({
                "name": rule["name"],
                "template": rule['template']
            })

        elif rule["trigger"] == 'days_before_expiration':
            days_before_expiration[rule['offset_days']].append({
                "name": rule["name"],
                "template": rule['template']
            })

        else:
            after_expiration.append({
                "name": rule["name"],
                "template": rule['template']
            })

    # Go through all accounts and check
    notifications = []
    for account in accounts:
        if account['created_day'] == current_day:
            for r in on_create_rules:
                noti = " ".join([account["account_id"], r["name"], r["template"]])
                notifications.append(noti)

        if current_day > account["expires_day"]:
            for r in after_expiration:
                noti = " ".join([account["account_id"], r["name"], r["template"]])
                notifications.append(noti)

        offset = account['expires_day'] - current_day
        for r in days_before_expiration[offset]:
            noti = " ".join([account["account_id"], r["name"], r["template"]])
            notifications.append(noti)

    return notifications


if __name__ == "__main__":
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

    result = solution(current_day=current_day, accounts=accounts, rules=rules)
    print(result)
