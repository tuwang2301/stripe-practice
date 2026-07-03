"""
STRIPE PRACTICE: CSV & File I/O Practice Challenges
==================================================

Hãy tự gõ code vào các hàm trống dưới đây để luyện tay cú pháp.
Chạy file này bằng lệnh: `python virtual_onsite/csv_practice_challenges.py` để chạy bộ test tự động.

YÊU CẦU: Không sử dụng bất kỳ AI Assistant nào trong lúc gõ để quen phản xạ phòng thi!
"""

import csv
import io
from datetime import datetime, timezone

# ===================================================================
# CHALLENGE 1: Parse CSV String defensively
# ===================================================================
def parse_csv_string(csv_data):
    """
    Đề bài: Cho một chuỗi CSV thô (có thể chứa ký tự \r\n, dòng trống ở cuối,
    và cột chứa dấu phẩy lồng trong ngoặc kép).
    Hãy parse chuỗi này và trả về danh sách các dictionary đại diện cho từng dòng.
    
    Đầu vào:
        csv_data (str): Chuỗi CSV
        
    Trả về:
        list of dict: Danh sách các dòng dạng dictionary. Ví dụ: [{'id': '1', 'name': 'Stripe, Inc.'}]
    """
    # Gõ code của bạn ở đây
    pass


# ===================================================================
# CHALLENGE 2: Filter and Write transactions to CSV
# ===================================================================
def filter_and_write_transactions(transactions, output_filepath):
    """
    Đề bài: Cho danh sách các giao dịch dạng dictionary.
    1. Lọc ra các giao dịch có trạng thái "success".
    2. Ghi kết quả vào một file CSV tại đường dẫn output_filepath.
    3. File CSV xuất ra phải có header gồm: "id", "amount_in_cents", "currency".
    4. Yêu cầu ghi file an toàn, tránh lỗi dòng trống trên Windows.
    
    Đầu vào:
        transactions (list of dict): Giao dịch đầu vào
        output_filepath (str): Đường dẫn file xuất ra (.csv)
    """
    # Gõ code của bạn ở đây
    pass


# ===================================================================
# CHALLENGE 3: Daily Sales Aggregator (Datetime + Parsing)
# ===================================================================
def aggregate_daily_sales(csv_string):
    """
    Đề bài: Cho chuỗi CSV chứa các cột: "timestamp", "amount_cents", "status".
    1. Parse dữ liệu đầu vào.
    2. Lọc ra các dòng có status là "paid".
    3. Đối với cột timestamp (dạng ISO-8601 "YYYY-MM-DDTHH:MM:SSZ"), hãy chuyển đổi 
       hoặc nhóm (group by) theo Ngày dạng "YYYY-MM-DD" (múi giờ UTC).
    4. Tính tổng amount_cents của từng ngày.
    5. Trả về một dictionary chứa thông tin tổng hợp: {"YYYY-MM-DD": tong_tien}.
    
    Đầu vào:
        csv_string (str): Chuỗi dữ liệu CSV
        
    Trả về:
        dict: Kết quả tổng hợp ngày -> tổng tiền (int)
    """
    # Gõ code của bạn ở đây
    pass


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    print("--- RUNNING TESTS ---")
    
    # Test Challenge 1
    c1_input = """id,company,country\r
1,"Stripe, Inc.",US\r
2,"Google, LLC",US\r
\r
"""
    try:
        c1_res = parse_csv_string(c1_input)
        assert isinstance(c1_res, list), "Challenge 1: Kết quả trả về phải là một list"
        assert len(c1_res) == 2, f"Challenge 1: Kỳ vọng 2 dòng nhưng nhận được {len(c1_res)}"
        assert c1_res[0].get("company") == "Stripe, Inc.", "Challenge 1: Không parse đúng dấu phẩy lồng trong ngoặc kép"
        assert c1_res[1].get("country") == "US", "Challenge 1: Lỗi dính ký tự xuống dòng \\r ở trường cuối cùng"
        print("✅ Challenge 1: PASSED!")
    except Exception as e:
        print("❌ Challenge 1: FAILED ->", e)

    # Test Challenge 2
    c2_input = [
        {"id": "tx_101", "status": "success", "amount_in_cents": 5000, "currency": "usd"},
        {"id": "tx_102", "status": "failed", "amount_in_cents": 3000, "currency": "eur"},
        {"id": "tx_103", "status": "success", "amount_in_cents": 2500, "currency": "usd"},
    ]
    c2_output_path = "virtual_onsite/scratch/temp_output.csv"
    try:
        import os
        os.makedirs("virtual_onsite/scratch", exist_ok=True)
        if os.path.exists(c2_output_path):
            os.remove(c2_output_path)
            
        filter_and_write_transactions(c2_input, c2_output_path)
        
        # Verify file contents
        assert os.path.exists(c2_output_path), "Challenge 2: File xuất ra không được tạo"
        with open(c2_output_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        
        assert len(lines) == 3, f"Challenge 2: File CSV phải có 3 dòng (1 header + 2 data), nhận được {len(lines)}"
        assert lines[0] == "id,amount_in_cents,currency", f"Challenge 2: Header sai: {lines[0]}"
        assert lines[1] == "tx_101,5000,usd", f"Challenge 2: Giao dịch 1 sai: {lines[1]}"
        assert lines[2] == "tx_103,2500,usd", f"Challenge 2: Giao dịch 3 sai: {lines[2]}"
        print("✅ Challenge 2: PASSED!")
    except Exception as e:
        print("❌ Challenge 2: FAILED ->", e)

    # Test Challenge 3
    c3_input = """timestamp,amount_cents,status
2022-06-23T10:15:30Z,1000,paid
2022-06-23T22:45:00Z,500,paid
2022-06-24T05:30:00Z,2500,paid
2022-06-24T18:00:00Z,1200,failed
"""
    try:
        c3_res = aggregate_daily_sales(c3_input)
        assert isinstance(c3_res, dict), "Challenge 3: Kết quả trả về phải là một dict"
        assert c3_res.get("2022-06-23") == 1500, f"Challenge 3: Nhóm ngày 2022-06-23 sai: {c3_res.get('2022-06-23')}"
        assert c3_res.get("2022-06-24") == 2500, f"Challenge 3: Nhóm ngày 2022-06-24 sai (phải lọc bỏ 'failed'): {c3_res.get('2022-06-24')}"
        print("✅ Challenge 3: PASSED!")
    except Exception as e:
        print("❌ Challenge 3: FAILED ->", e)
