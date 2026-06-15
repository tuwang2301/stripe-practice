from collections import *
import math

def process_authorizations(requests, rules):
    # Parsing the data in to 2 dicts
    sorted_requests = sorted(requests, key= lambda x : x["time"])
    sorted_rules = sorted(rules, key= lambda x : x["time"])

    result = []
    active_rules = []
    rules_idx = 0

    for request in sorted_requests:
        while rules_idx < len(sorted_rules) and sorted_rules[rules_idx]["time"] < request["time"]:
            active_rules.append(sorted_rules[rules_idx])
            rules_idx += 1

        rejected = any(
            str(request[rule["field"]]) == rule["value"]
            for rule in active_rules
        )

        decision = "REJECT" if rejected else "APPROVE"

        result.append(f"{request['time']} {request['unique_id']} {request['amount']} {decision}")

    return result

if __name__ == "__main__":
    # TC1
    requests = [{"time": 5, "unique_id": "A1", "amount": 120, "card_number": "4111", "merchant": "X"}, {"time": 1, "unique_id": "A0", "amount": 300, "card_number": "5555", "merchant": "Y"}, {"time": 5, "unique_id": "A2", "amount": 120, "card_number": "4111", "merchant": "Z"}]
    rules = []

    # Output ["1 A0 300 APPROVE", "5 A1 120 APPROVE", "5 A2 120 APPROVE"]

    # TC2

    requests = [{"time": 5, "unique_id": "A1", "amount": 120, "card_number": "4111", "merchant": "X"}, {"time": 1, "unique_id": "A0", "amount": 300, "card_number": "5555", "merchant": "Y"}, {"time": 5, "unique_id": "A2", "amount": 120, "card_number": "4111", "merchant": "Z"}]
    rules = [{"time": 3, "field": "card_number", "value": "4111"}, {"time": 5, "field": "merchant", "value": "Y"}, {"time": 5, "field": "amount", "value": "120"}]
    
    #Output ["1 A0 300 APPROVE", "5 A1 120 REJECT", "5 A2 120 REJECT"]


    result = process_authorizations(requests, rules)
    print(result)
