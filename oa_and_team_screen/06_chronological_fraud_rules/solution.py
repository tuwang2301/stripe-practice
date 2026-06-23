def process_authorizations(requests, rules):
    # Sort requests and rules by time. Python's sort is stable, which preserves input order.
    sorted_requests = sorted(requests, key=lambda x: x["time"])
    sorted_rules = sorted(rules, key=lambda x: x["time"])

    result = []
    active_rules = []
    rules_idx = 0

    for request in sorted_requests:
        # A rule with time t applies to any request with timestamp >= t
        while rules_idx < len(sorted_rules) and sorted_rules[rules_idx]["time"] <= request["time"]:
            active_rules.append(sorted_rules[rules_idx])
            rules_idx += 1

        rejected = any(
            str(request[rule["field"]]) == rule["value"]
            for rule in active_rules
        )

        decision = "REJECT" if rejected else "APPROVE"

        result.append(f"{request['time']} {request['unique_id']} {request['amount']} {decision}")

    return result
