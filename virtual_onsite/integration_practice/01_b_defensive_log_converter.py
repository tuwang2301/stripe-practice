"""
STRIPE INTEGRATION PRACTICE 01B: Defensive Payout Log Converter (PRACTICE)
========================================================================

PROBLEM DESCRIPTION:
Stripe receives payout logs from multiple external gateways. 
Your task is to parse a JSON payout log file, filter for successfully completed payouts,
convert the fields, and write them to a clean CSV report.

Because the input data comes from external gateways, it is highly malformed and noisy.
Your solution must be exceptionally defensive and never crash on individual row corruption.

Input JSON format (List of dictionaries):
[
    {
        "payout_id": "po_901",
        "merchant_id": "acct_01",
        "amount_cents": 50000,
        "status": "completed",
        "payout_timestamp": 1656000000
    },
    ...
]

Requirements:
1. Open and parse the JSON input file defensively.
2. Filter for entries where `status == "completed"`.
3. Check and skip any entry that has:
   - Missing required keys (`payout_id`, `merchant_id`, `amount_cents`, `status`, `payout_timestamp`).
   - A non-positive amount (`amount_cents <= 0`).
   - An invalid or corrupted timestamp that cannot be parsed into an integer epoch.
4. Transform fields:
   - Convert `amount_cents` to USD dollars (`amount_usd = amount_cents / 100.0`).
   - Convert `payout_timestamp` (epoch seconds) to UTC format: `YYYY-MM-DD HH:MM:SS`.
5. Write the valid rows to `csv_report_path` using Python's standard `csv` library.
   - Header: `payout_id,merchant_id,amount_usd,payout_date`
6. Return a tuple: `(successful_count, skipped_count)`
   - `successful_count`: Number of records written to the CSV.
   - `skipped_count`: Number of input entries that were skipped due to being malformed, having missing keys, invalid amounts, or failing validation.
"""

import csv
import json
from datetime import datetime, timezone

def convert_payout_logs(json_log_path, csv_report_path):
    # WRITE YOUR CODE HERE
    # 1. Open and parse the JSON input file defensively.
    try:
        with open(json_log_path, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to read or parse input JSON file: {e}")

    if not isinstance(logs, list):
        raise ValueError("Input JSON must be a list of log entries")

    succesful_txs = []
    skipped_count = 0

    # 2. Filter for entries where `status == "completed"`.
    for entry in logs:
        if not isinstance(entry, dict):
            skipped_count += 1
            continue

        if entry.get('status') != 'completed':
            skipped_count += 1
            continue

        payout_id = entry.get('payout_id')
        merchant_id = entry.get('merchant_id')
        amount_cents = entry.get('amount_cents')
        status = entry.get('status')
        payout_timestamp = entry.get('payout_timestamp')

        """
        3. Check and skip any entry that has:
        - Missing required keys (`payout_id`, `merchant_id`, `amount_cents`, `status`, `payout_timestamp`).
        - A non-positive amount (`amount_cents <= 0`).
        - An invalid or corrupted timestamp that cannot be parsed into an integer epoch.
        """
       
        if None in (payout_id, merchant_id, amount_cents, status, payout_timestamp):
            skipped_count += 1
            continue

        if amount_cents <= 0:
            skipped_count += 1
            continue

        amount_usd = amount_cents / 100.0

        try:
            payout_date = datetime.fromtimestamp(int(payout_timestamp), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError, OverflowError) as e:
            print(f"Error handling datetime: {e}")
            skipped_count += 1
            continue

        succesful_txs.append(
            {
                "payout_id": payout_id,
                "merchant_id": merchant_id,
                "amount_usd": amount_usd,
                "payout_date": payout_date
            }
        )

    
    """
    5. Write the valid rows to `csv_report_path` using Python's standard `csv` library.
    - Header: `payout_id,merchant_id,amount_usd,payout_date`
    """
    headers = ["payout_id","merchant_id","amount_usd","payout_date"]
    try:
        with open(csv_report_path, 'w', newline="", encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers) 
            writer.writeheader()
            writer.writerows(succesful_txs)
    except IOError as e:
        raise ValueError(f"Writing file error: {e}")

    return (len(succesful_txs), skipped_count)


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    import os
    
    json_path = "mock_payout_logs.json"
    csv_path = "payout_report.csv"
    
    # Mix of valid, invalid, missing keys, and corrupted datatypes
    mock_data = [
        # 1. Valid completed payout
        {"payout_id": "po_1", "merchant_id": "m1", "amount_cents": 15000, "status": "completed", "payout_timestamp": 1656000000},
        # 2. Skip: status is pending
        {"payout_id": "po_2", "merchant_id": "m1", "amount_cents": 20000, "status": "pending", "payout_timestamp": 1656000100},
        # 3. Skip: missing merchant_id
        {"payout_id": "po_3", "amount_cents": 30000, "status": "completed", "payout_timestamp": 1656000200},
        # 4. Valid completed payout (timestamp is string representation of int, should handle)
        {"payout_id": "po_4", "merchant_id": "m2", "amount_cents": 45050, "status": "completed", "payout_timestamp": "1656000300"},
        # 5. Skip: negative amount
        {"payout_id": "po_5", "merchant_id": "m2", "amount_cents": -500, "status": "completed", "payout_timestamp": 1656000400},
        # 6. Skip: corrupt/non-integer timestamp
        {"payout_id": "po_6", "merchant_id": "m3", "amount_cents": 100, "status": "completed", "payout_timestamp": "invalid_time"},
        # 7. Skip: malformed element (not a dict)
        "malformed_row_string",
        # 8. Valid completed payout
        {"payout_id": "po_7", "merchant_id": "m3", "amount_cents": 500, "status": "completed", "payout_timestamp": 1656000500}
    ]
    
    # Write mock logs
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(mock_data, f)
        
    try:
        success, skipped = convert_payout_logs(json_path, csv_path)
        print(f"Returned -> Success: {success}, Skipped: {skipped}")
        
        # We expect 3 successful payouts (po_1, po_4, po_7) and 5 skipped elements
        if success == 3 and skipped == 5:
            # Verify CSV content
            with open(csv_path, "r", encoding="utf-8") as f:
                lines = f.read().strip().split("\n")
                
            expected_lines = [
                "payout_id,merchant_id,amount_usd,payout_date",
                "po_1,m1,150.0,2022-06-23 16:00:00",
                "po_4,m2,450.5,2022-06-23 16:05:00",
                "po_7,m3,5.0,2022-06-23 16:08:20"
            ]
            
            if lines == expected_lines:
                print("SUCCESS: Integration Problem 01B Passed!")
            else:
                print("FAIL: CSV content does not match expected output.")
                print("Got:")
                for l in lines:
                    print("  ", l)
        else:
            print(f"FAIL: Expected (3, 5), got ({success}, {skipped})")
            
    except Exception as e:
        print("FAIL: Execution raised an error:", e)
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up mock files
        for path in [json_path, csv_path]:
            if os.path.exists(path):
                os.remove(path)
