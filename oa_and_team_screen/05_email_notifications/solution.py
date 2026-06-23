from collections import defaultdict

def solution(current_day, accounts, rules):
    # Group rules with their original index to preserve configuration order
    on_create_rules = []
    after_expiration_rules = []
    days_before_expiration_rules = defaultdict(list)

    for idx, rule in enumerate(rules):
        rule_info = {
            "name": rule["name"],
            "template": rule["template"],
            "index": idx
        }
        trigger = rule["trigger"]
        if trigger == 'on_create':
            on_create_rules.append(rule_info)
        elif trigger == 'after_expiration':
            after_expiration_rules.append(rule_info)
        elif trigger == 'days_before_expiration':
            offset = rule["offset_days"]
            days_before_expiration_rules[offset].append(rule_info)

    notifications = []
    for account in accounts:
        matched = []
        
        # Check on_create
        if account['created_day'] == current_day:
            for r in on_create_rules:
                matched.append(r)

        # Check after_expiration
        if current_day > account["expires_day"]:
            for r in after_expiration_rules:
                matched.append(r)

        # Check days_before_expiration
        offset = account['expires_day'] - current_day
        if offset in days_before_expiration_rules:
            for r in days_before_expiration_rules[offset]:
                matched.append(r)

        # Sort matched rules by their original index
        matched.sort(key=lambda x: x["index"])

        for r in matched:
            noti = f"{account['account_id']} {r['name']} {r['template']}"
            notifications.append(noti)

    return notifications
