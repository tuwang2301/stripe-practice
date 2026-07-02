# Stripe Integration Round: Ultimate Cheat Sheet (Python)

Tài liệu này tổng hợp toàn bộ các kiến thức cốt lõi, thư viện chuẩn, bẫy lỗi thường gặp và mã mẫu (templates) mà bạn cần chuẩn bị cho vòng **Integration** của Stripe.

---

## 1. Gọi API bằng thư viện `requests` (GET, POST & Query Params)

### 📌 Mẫu GET Request (Có Phân Trang & Xử Lý Rate Limit)
Bạn cần nắm lòng cấu trúc gọi API có phân trang dựa trên con trỏ (`starting_after`) và tự động retry khi gặp lỗi giới hạn tần suất (HTTP 429).

```python
import time
import requests

def fetch_all_data(api_url, api_token):
    # Luôn làm sạch API URL để tránh lỗi nối chuỗi
    base_url = api_url.rstrip('/')
    endpoint = f"{base_url}/v1/charges"
    headers = {"Authorization": f"Bearer {api_token}"}
    
    results = []
    has_more = True
    starting_after = None
    
    while has_more:
        params = {"limit": 100} # Đề bài thường có limit mặc định hoặc tối đa
        if starting_after:
            params["starting_after"] = starting_after
            
        try:
            response = requests.get(url=endpoint, headers=headers, params=params, timeout=10)
            
            # 1. Bẫy lỗi Rate Limit (HTTP 429)
            if response.status_code == 429:
                time.sleep(1) # Chờ 1 giây theo spec
                continue
                
            response.raise_for_status() # Bẫy các lỗi 4xx/5xx khác
            data = response.json()
            
        except requests.exceptions.RequestException as e:
            # 2. Xử lý lỗi thảm họa (Connection, DNS, Server 500...)
            print(f"Catastrophic failure: {e}")
            return [] # Hoặc return (0, 0) tùy đề bài yêu cầu
            
        if not isinstance(data, dict):
            break
            
        records = data.get("data", [])
        results.extend(records)
        
        # 3. Cập nhật con trỏ phân trang
        if records:
            starting_after = records[-1].get("id")
            has_more = data.get("has_more", False)
        else:
            has_more = False
            
    return results
```

### 📌 Mẫu POST Request (Gửi Payload & Cập Nhật Dữ Liệu)
```python
def update_status(api_url, api_token, resource_id, status_val):
    base_url = api_url.rstrip('/')
    url = f"{base_url}/v1/resources/{resource_id}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {"status": status_val}
    
    while True:
        try:
            res = requests.post(url=url, headers=headers, json=payload, timeout=5)
            if res.status_code == 429:
                time.sleep(1)
                continue
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to update resource {resource_id}: {e}")
            break
    return None
```

---

## 2. Thao tác File I/O (JSON & CSV an toàn)

### 📌 Đọc và Parse JSON defensively
Không bao giờ tin tưởng định dạng của dữ liệu đầu vào. Hãy luôn kiểm tra kiểu dữ liệu sau khi parse.
```python
import json

def load_json_safely(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f) # Tốt hơn loads(f.read()) vì tiết kiệm RAM
            
        if not isinstance(data, list): # Hoặc isinstance(data, dict) tùy đề
            raise ValueError("JSON root is not a list")
        return data
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"JSON error: {e}")
        return []
```

### 📌 Ghi file CSV an toàn (Sử dụng thư viện `csv`)
Không bao giờ dùng chuỗi nội suy `f"{id},{name}\n"` vì nếu `name` chứa dấu phẩy, file CSV của bạn sẽ bị lệch cột.
```python
import csv

def write_csv_safely(output_path, records):
    headers = ["id", "amount_usd", "created_date"]
    
    try:
        # Bắt buộc phải có newline="" trên Windows để tránh dòng trống xen kẽ
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            for item in records:
                # Trích xuất và kiểm tra dữ liệu defensively
                if not isinstance(item, dict):
                    continue
                writer.writerow({
                    "id": item.get("id"),
                    "amount_usd": item.get("amount", 0) / 100.0,
                    "created_date": item.get("created_date")
                })
    except IOError as e:
        print(f"Failed to write CSV: {e}")
```

---

## 3. Quản lý múi giờ và thời gian (Datetime)

Múi giờ mặc định của Stripe luôn là **UTC (GMT+0)**.

### 📌 4 Câu Lệnh Datetime Cần Thuộc Lòng
```python
from datetime import datetime, timezone, timedelta

# 1. Parse chuỗi ngày tháng dạng ISO-8601
dt = datetime.strptime("2022-06-23T16:30:15Z", "%Y-%m-%dT%H:%M:%SZ")

# 2. Định dạng Datetime thành chuỗi hiển thị
date_str = dt.strftime("%Y-%m-%d %H:%M:%S")

# 3. Đổi số giây Epoch sang Datetime UTC (Bắt buộc truyền tz)
dt_utc = datetime.fromtimestamp(1656000000, tz=timezone.utc)

# 4. Kiểm tra time drift 2 chiều (Chống Replay Attack)
if abs(current_time - t_val) > max_drift_seconds:
    print("Yêu cầu quá hạn hoặc lỗi đồng bộ đồng hồ")
```

---

## 4. ⚠️ Bẫy Lỗi Kinh Điển - Cách Phòng Thủ (Defensive Check)

1.  **Lệch múi giờ so sánh (Naive vs Aware)**:
    Không bao giờ so sánh `datetime.now()` (không có múi giờ) với `datetime.now(timezone.utc)`. Luôn chỉ định `tz=timezone.utc` cho toàn bộ các biến thời gian.
2.  **Đường dẫn tương đối (Relative URL crash)**:
    Khi interviewer đưa cho bạn endpoint dạng `/v1/invoices`, nếu bạn truyền trực tiếp vào `requests.get('/v1/invoices')` sẽ bị crash. Hãy kết hợp với `api_url.rstrip('/')` để sinh URL tuyệt đối.
3.  **Lỗi ném exception trong vòng lặp con (raise_for_status)**:
    Khi duyệt qua 100 bản ghi, nếu bạn gọi API con cho từng bản ghi (ví dụ lấy thông tin chi tiết từng khách hàng) và gọi `res.raise_for_status()`, hãy luôn bọc nó trong `try-except` riêng biệt. Nếu không, chỉ cần 1 request lỗi, toàn bộ tiến trình phỏng vấn sẽ bị sập.
4.  **Tập hợp key trùng lặp khi ghi CSV**:
    Khi dùng `csv.DictWriter`, hãy đảm bảo dictionary truyền vào `writerow` chỉ chứa các key khớp chính xác với danh sách `fieldnames` định nghĩa lúc đầu, nếu thừa key, Python sẽ bỏ qua (hoặc ném lỗi nếu cấu hình khắt khe).
