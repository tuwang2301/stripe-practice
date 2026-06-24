"""
STRIPE INTEGRATION PRACTICE 01: JSON Transaction Log Parser (EASY)
==================================================================

PROBLEM DESCRIPTION:
Stripe systems often output diagnostic log files in JSON format.
Your task is to write a script to parse a JSON log file, extract successful transactions, 
and output a clean CSV report.

You are given:
- `json_log_path`: Path to a file containing a JSON list of transaction logs.
- `csv_report_path`: Path where you should write the formatted CSV report.

Each transaction entry in the JSON file looks like:
```json
{
    "tx_id": "tx_101",
    "merchant_id": "acct_88",
    "amount": 2500,
    "status": "success",
    "created_at_epoch": 1656000000
}
```

Tasks to perform:
1. Read the JSON log file using the `json` library.
2. Filter for transactions where `status == "success"`.
3. Format each transaction's `created_at_epoch` (unix timestamp in seconds) into a readable date string:
   `YYYY-MM-DD HH:MM:SS` (in UTC time) using the `datetime` library.
4. Write the results to `csv_report_path` with a header row:
   `tx_id,merchant_id,amount,created_date`
5. Return the number of successful transactions written to the report.
"""

import csv
import json
from datetime import datetime, timezone

def generate_transaction_report(json_log_path, csv_report_path):
    """
    Parses a JSON transaction log file, filters for successful payments,
    and outputs a clean, well-formatted CSV report.
    
    Ensures safe key access, defensive processing of malformed rows, 
    and standard CSV library usage to handle special characters.
    """
    # 1. Open and load the JSON file defensively
    try:
        with open(json_log_path, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to read/parse input JSON file: {e}")

    if not isinstance(logs, list):
        raise ValueError("Input JSON file must contain a JSON list of transaction logs")

    # 2. Define expected CSV columns and filter records
    csv_fields = ["tx_id", "merchant_id", "amount", "created_date"]
    successful_txs = []

    for entry in logs:
        # Check that entry is a valid JSON object/dictionary
        if not isinstance(entry, dict):
            continue

        # Filter for successful transactions
        if entry.get("status") != "success":
            continue

        # Safely extract mandatory fields
        tx_id = entry.get("tx_id")
        merchant_id = entry.get("merchant_id")
        amount = entry.get("amount")
        epoch_sec = entry.get("created_at_epoch")

        # Skip record if any required field is missing
        if None in (tx_id, merchant_id, amount, epoch_sec):
            continue

        # Safe epoch to human-readable date conversion
        try:
            dt = datetime.fromtimestamp(int(epoch_sec), tz=timezone.utc)
            created_date = dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError, OverflowError):
            continue  # Skip rows with malformed timestamps

        successful_txs.append({
            "tx_id": tx_id,
            "merchant_id": merchant_id,
            "amount": amount,
            "created_date": created_date
        })

    # 3. Write results using standard CSV library
    try:
        with open(csv_report_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
            writer.writeheader()
            writer.writerows(successful_txs)
    except IOError as e:
        raise ValueError(f"Failed to write CSV report: {e}")

    # 4. Return count of successful payments
    return len(successful_txs)



# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    # Setup mock JSON log file
    json_path = "mock_logs.json"
    csv_path = "success_report.csv"
    
    mock_data = [
        {"tx_id": "tx_1", "merchant_id": "m1", "amount": 1000, "status": "success", "created_at_epoch": 1656000000},
        {"tx_id": "tx_2", "merchant_id": "m2", "amount": 500, "status": "failed", "created_at_epoch": 1656000100},
        {"tx_id": "tx_3", "merchant_id": "m1", "amount": 2000, "status": "success", "created_at_epoch": 1656000200}
    ]
    
    # Write mock data to file
    with open(json_path, 'w') as f:
        json.dump(mock_data, f)
        
    # Run user function
    count = generate_transaction_report(json_path, csv_path)
    print("Report count (expected 2):", count)
    
    if count == 2:
        # Check CSV content
        try:
            with open(csv_path, 'r') as f:
                lines = f.read().strip().split('\n')
                print("Generated CSV Content:")
                for l in lines:
                    print("  ", l)
                
                expected_lines = [
                    "tx_id,merchant_id,amount,created_date",
                    "tx_1,m1,1000,2022-06-23 16:00:00",
                    "tx_3,m1,2000,2022-06-23 16:03:20"
                ]
                if lines == expected_lines:
                    print("SUCCESS: Integration Problem 01 Passed!")
                else:
                    print("FAIL: CSV content does not match expected lines.")
        except Exception as e:
            print("FAIL: Could not verify CSV report file:", e)
    else:
        print("FAIL: Incorrect count returned.")
        
    # Clean up temp files
    import os
    for path in [json_path, csv_path]:
        if os.path.exists(path):
            os.remove(path)
