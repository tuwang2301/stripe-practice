# Hướng Dẫn Chi Tiết: Kỹ Năng Prompt AI, Lập Kế Hoạch & Thư Viện Tích Hợp (API & I/O)

Tài liệu này cung cấp các hướng dẫn cụ thể, chiến thuật tương tác và các đoạn mã mẫu (cheat sheet) để bạn ôn luyện trực tiếp cho hai phần cốt lõi của vòng Virtual Onsite: **Lập trình cùng AI (Programming Exercise)** và **Tích hợp hệ thống (Integration)**.

---

## PHẦN 1: Chiến Thuật Lập Kế Hoạch & Prompt AI (Programming Exercise)

Trong bài thi này, Stripe không chỉ đánh giá bạn có viết được code hay không, mà đánh giá **cách bạn tương tác và hợp tác với AI** (giống như bạn đang quản lý một Junior Engineer). 

> [!IMPORTANT]
> **Cập Nhật Mới Nhất 2026**: Vòng Programming Exercise truyền thống đã được thay thế bằng **AI Programming Exercise**. 
> * Bạn sẽ làm việc trực tiếp trong môi trường tích hợp sẵn một AI Assistant (thường là một model có hiệu năng trung bình/cùi hơn các model thương mại lớn như Claude Opus hay GPT-4o).
> * Mục tiêu của vòng này là kiểm tra **cách bạn dẫn dắt AI giải quyết vấn đề**. Việc copy-paste toàn bộ đề bài hoặc đưa code lỗi rồi bảo *"Sửa hộ tôi"* (raw debugging) được coi là một điểm trừ lớn. Thay vào đó, hãy coi AI là một cộng tác viên để cùng xây dựng giải pháp.

### 1. Quy Trình 3 Bước Tương Tác Hợp Tác (Collaborative Prompting)
*   **Bước 1: Sử dụng AI để làm rõ yêu cầu & Thuật toán (Understand & Verify)**: Đọc kỹ đề bài, tự suy nghĩ và đề xuất hướng giải quyết (Data Structures, Time/Space Complexity). Sau đó, viết prompt bảo AI xác nhận xem hướng đi đó có đúng đắn không, có lỗ hổng logic nào hay không.
*   **Bước 2: Lập kế hoạch từng bước (Step-by-Step Blueprint)**: Yêu cầu AI cùng bạn xây dựng các bước triển khai cụ thể (ví dụ: bước 1 parse dữ liệu, bước 2 tracking state, bước 3 xử lý dispute). Xác nhận cấu trúc khung (Skeleton) trước khi code.
*   **Bước 3: Gọi AI viết từng phần nhỏ & Kiểm soát chất lượng (Incremental Execution)**: Chỉ cho AI viết từng hàm helper nhỏ hoặc đoạn code logic cốt lõi. Luôn tự tay kiểm tra, tinh chỉnh và chạy thử unit test cục bộ sau mỗi hàm để đảm bảo tính chính xác cao nhất.


### 2. Bộ Mẫu Prompt (Prompt Templates) Nên Dùng

#### Prompt Xác Nhận & Đánh Giá Hướng Giải Quyết (Verify Approach):
> *"Tôi đang giải bài toán theo dõi rủi ro giao dịch của các merchant. Ý tưởng của tôi là sử dụng một hash map (`defaultdict`) để quản lý số lượng dispute của từng merchant, và một double-ended queue (`deque`) để lưu trữ timestamps của các sự kiện trong vòng 60 giây gần nhất nhằm kiểm tra giới hạn tần suất. Theo bạn, hướng đi này có tối ưu về mặt Time/Space Complexity không? Có trường hợp đặc biệt (edge case) nào mà tôi cần lưu ý trước khi triển khai không?"*

#### Prompt Thiết Kế Bộ Khung (Skeleton):
> *"Dựa trên thuật toán ở trên, tôi muốn tự code phần xử lý chính. Hãy viết giúp tôi cấu trúc khung (boilerplate/skeleton) của class `TransactionEngine` bao gồm các hàm `__init__`, `process_transaction(tx_string)`, và `get_risk_score(merchant_id)`. Vui lòng chỉ cung cấp khung class, khai báo các biến lưu trữ state và chú thích docstring, chưa cần triển khai logic chi tiết bên trong các hàm."*

#### Prompt Nhờ Viết Hàm Trợ Giúp (Helper Function):
> *"Hãy viết một hàm helper nhận vào chuỗi CSV giao dịch dạng `'merchant_id,amount,customer_id,hour'` và parse nó thành một Python dictionary với các trường dữ liệu được ép kiểu chính xác (ví dụ: `amount` và `hour` phải là kiểu `int`). Hãy viết code thật đơn giản và tường minh."*

#### Prompt Sửa Lỗi Hợp Tác (Collaborative Debugging):
Nếu code chạy test bị lỗi, thay vì bảo AI sửa tất cả, hãy cùng phân tích:
> *"Tôi đang gặp lỗi `[Copy Traceback Lỗi]` tại dòng xử lý tính toán. Tôi nghi ngờ nguyên nhân là do kiểu dữ liệu truyền vào đang là String thay vì Integer. Hãy phân tích và đề xuất 2 phương án khắc phục lỗi này mà không làm ảnh hưởng đến các hàm khác."*


#### Prompt Sửa Lỗi (Debugging):
Nếu code bị lỗi khi chạy test, hãy copy toàn bộ thông tin lỗi (Traceback) đưa cho AI kèm yêu cầu:
> *"Unit test của tôi bị lỗi sau: `[Copy Traceback Lỗi]`. Hãy phân tích lỗi này trong hàm `process_transaction`, giải thích nguyên nhân và sửa lại hàm đó cho tôi."*

#### Prompt Yêu Cầu Tối Giản Code (Simplify):
Stripe ghét code quá phức tạp. Nếu AI viết code khó đọc, hãy prompt:
> *"Code này quá phức tạp và khó bảo trì. Hãy tối giản nó bằng cách sử dụng các vòng lặp `for` thông thường và các thư viện chuẩn của Python. Không sử dụng các hàm lambda phức tạp hoặc các thư viện ngoài."*

---

## PHẦN 2: Thư Viện Tích Hợp API & File I/O Cheat Sheet (Integration)

Trong vòng **Integration**, bạn sẽ phải đọc ghi file dữ liệu và gọi API ngoài. Dưới đây là các đoạn code Python chuẩn, tối giản và chạy cực kỳ ổn định mà bạn nên thuộc lòng hoặc chuẩn bị sẵn:

### 1. Gọi API Với Thư Viện `requests`

#### Đoạn Code Gửi GET Request (Có Authorization & Query Params & Phân Trang)
Stripe sử dụng **Cursor-based pagination** (phân trang dựa trên con trỏ). Bạn cần lấy `id` của phần tử cuối cùng ở trang hiện tại để làm con trỏ `starting_after` cho trang sau:

```python
import requests
import time

def fetch_all_payments(api_url, api_key):
    all_payments = []
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    next_page_cursor = None
    
    while True:
        # Thiết lập tham số phân trang
        params = {"limit": 100}
        if next_page_cursor:
            params["starting_after"] = next_page_cursor
            
        try:
            # Gửi request có timeout để tránh treo hệ thống
            response = requests.get(api_url, headers=headers, params=params, timeout=5)
            
            # Xử lý khi bị Rate Limit (HTTP 429)
            if response.status_code == 429:
                print("Bị giới hạn tần suất (Rate limited). Đang chờ 1 giây trước khi thử lại...")
                time.sleep(1)
                continue
                
            # Kiểm tra các lỗi HTTP khác (4xx, 5xx)
            response.raise_for_status()
            payload = response.json()
            
            data_list = payload.get("data", [])
            all_payments.extend(data_list)
            
            # Kiểm tra xem còn trang tiếp theo hay không
            if payload.get("has_more") and data_list:
                # Con trỏ là ID của phần tử cuối cùng trong trang này
                next_page_cursor = data_list[-1]["id"]
            else:
                break
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối API: {e}")
            break
            
    return all_payments
```

#### Đoạn Code Gửi POST Request (Tạo Tài Khoản/Giao Dịch Mới)
```python
def create_customer(api_url, api_key, email, name):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "name": name
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Lỗi HTTP: {http_err} - Chi tiết: {response.text}")
    except Exception as err:
        print(f"Lỗi hệ thống khác: {err}")
    return None
```

---

### 2. Đọc Ghi File I/O (Không Dùng Thư Viện Ngoài)

Trong phỏng vấn, bạn nên thao tác trực tiếp bằng các hàm dựng sẵn của Python để thể hiện kỹ năng nền tảng vững chắc.

#### Đọc File Line-by-Line (Tránh Tràn Bộ Nhớ Với File Lớn)
```python
def process_log_file(file_path):
    transactions = []
    try:
        # Dùng 'with' để tự động đóng file sau khi đọc xong
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Loại bỏ khoảng trắng và dòng trống
                line_content = line.strip()
                if not line_content:
                    continue
                
                # Parse dòng CSV thủ công
                parts = [p.strip() for p in line_content.split(',')]
                transactions.append(parts)
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
    return transactions
```

#### Ghi Báo Cáo Ra File CSV Mới (Dùng Thư Viện csv Chuẩn)
```python
import csv

def write_report(file_path, data_list):
    headers = ["merchant_id", "total_amount", "status"]
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data_list)
        print(f"Ghi báo cáo thành công ra file: {file_path}")
    except IOError as e:
        print(f"Lỗi ghi file: {e}")
```

