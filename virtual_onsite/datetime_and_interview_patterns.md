# Stripe Onsite: Datetime Cheat Sheet & Interview Patterns

Trong các vòng phỏng vấn của Stripe (cả Programming và Integration), **xử lý ngày tháng (Datetime)** và **đồng bộ trạng thái thời gian** là một trong những phần cốt lõi được hỏi nhiều nhất. Tài liệu này giúp bạn hệ thống hóa toàn bộ kiến thức về Datetime trong Python và các dạng bài tập thực tế cần ôn luyện.

---

## 📅 PHẦN 1: Datetime trong Python - Định dạng & Các hàm cốt lõi

### 1. 3 Định dạng thời gian phổ biến tại Stripe
*   **Unix / Epoch Timestamp**: Dạng số nguyên/số thực biểu diễn số giây tính từ ngày `01/01/1970` (Ví dụ: `1656000000`). Rất hay gặp trong API hoặc Log File.
*   **ISO-8601 chuẩn**: Dạng chuỗi `'YYYY-MM-DD'` (Ví dụ: `'2022-06-23'`).
*   **ISO-8601 đầy đủ (Múi giờ UTC)**: Dạng chuỗi có chữ `T` ngăn cách và chữ `Z` chỉ múi giờ UTC (Ví dụ: `'2022-06-23T16:00:00Z'`).

---

### 2. Các hàm Datetime cần thuộc lòng trong Python

Để sử dụng thành thạo, bạn cần import thư viện chuẩn:
```python
from datetime import datetime, timezone, timedelta
```

#### A. Parse chuỗi sang đối tượng Datetime (`strptime` - String Parse)
Chữ **`p`** trong `strptime` viết tắt của **Parse** (Phân tích cú pháp chuỗi).
```python
# Cú pháp: datetime.strptime(date_string, format_string)
dt = datetime.strptime("2022-06-23 16:30:15", "%Y-%m-%d %H:%M:%S")
```
**Bảng mã định dạng (Format Codes):**
*   `%Y`: Năm 4 chữ số (Ví dụ: `2022`). *Lưu ý `%y` là năm 2 chữ số (Ví dụ: `22`).*
*   `%m`: Tháng 2 chữ số (`01` đến `12`).
*   `%d`: Ngày 2 chữ số (`01` đến `31`).
*   `%H`: Giờ 24h (`00` đến `23`).
*   `%M`: Phút 2 chữ số (`00` đến `59`).
*   `%S`: Giây 2 chữ số (`00` đến `59`).
*   `%f`: Microseconds (6 chữ số).

*Ví dụ parse ISO-8601 Stripe:*
```python
iso_dt = datetime.strptime("2022-06-23T16:30:15Z", "%Y-%m-%dT%H:%M:%SZ")
```

#### B. Định dạng Datetime thành chuỗi (`strftime` - String Format)
Chữ **`f`** trong `strftime` viết tắt của **Format** (Định dạng).
```python
# Chuyển đối tượng datetime về chuỗi để xuất báo cáo
date_str = dt.strftime("%Y-%m-%d %H:%M:%S") # '2022-06-23 16:30:15'
```

#### C. Chuyển đổi qua lại giữa Epoch và Datetime (Rất quan trọng)
```python
# 1. Từ Epoch (int/float) sang Datetime UTC (Bắt buộc dùng tz=timezone.utc)
dt_utc = datetime.fromtimestamp(1656000000, tz=timezone.utc)

# 2. Từ Datetime sang Epoch (int)
epoch_secs = int(dt_utc.timestamp())
```

#### D. Tính toán khoảng thời gian (`timedelta`)
```python
# Cộng hoặc trừ thời gian
five_minutes_ago = datetime.now(timezone.utc) - timedelta(minutes=5)
three_days_later = datetime.now(timezone.utc) + timedelta(days=3)

# Tính hiệu giữa hai mốc thời gian (Trả về đối tượng timedelta)
diff = dt_2 - dt_1
diff_in_seconds = diff.total_seconds() # Trả về số giây (float)
```

---

### ⚠️ 3 Bẫy lỗi Datetime thường gặp trong phỏng vấn

1.  **Lỗi So sánh Lệch múi giờ (Naive vs Aware)**:
    Nếu bạn so sánh một datetime không có múi giờ (Naive) với một datetime có múi giờ UTC (Aware), Python sẽ ném lỗi:
    `TypeError: can't compare offset-naive and offset-aware datetimes`
    *Cách tránh*: Luôn luôn truyền múi giờ `tz=timezone.utc` khi lấy thời gian hiện tại hoặc parse timestamp:
    ```python
    # Sai:
    now = datetime.now()
    # Đúng:
    now = datetime.now(timezone.utc)
    ```
2.  **Mẹo tối ưu so sánh chuỗi ISO-8601**:
    Nếu chuỗi ngày tháng ở định dạng chuẩn `YYYY-MM-DD` hoặc `YYYY-MM-DDTHH:MM:SS`, bạn **không cần** parse chúng ra datetime bằng `strptime` nếu chỉ để so sánh lớn/nhỏ. Python hỗ trợ so sánh trực tiếp các chuỗi này theo thứ tự từ điển:
    ```python
    # Hoàn toàn hợp lệ và chạy cực nhanh:
    if "2022-06-05" <= "2022-06-10" <= "2022-06-15":
        print("Khớp!")
    ```
3.  **Lỗi tràn/trượt thời gian (Boundary condition)**:
    Khi làm các bài toán sliding window (cửa sổ trượt), hãy chú ý khoảng cách thời gian có bao gồm điểm biên không (inclusive/exclusive). Ví dụ: Trong vòng 60 giây gần nhất tính từ $t$, khoảng thời gian đúng sẽ là `[t - 59, t]` hoặc `t_event > t - 60`.

---

## 🛠️ PHẦN 2: 3 Dạng bài tập nâng cao bạn nên ôn luyện thêm

Ngoài các bài toán bạn đã thực hành, dưới đây là 3 dạng bài Stripe cực kỳ ưa thích:

### Dạng 1: Quản lý Idempotency Key (Tránh trùng lặp webhook/giao dịch)
*   **Đề bài**: Stripe nhận được hàng nghìn Webhook gửi đến. Do lỗi mạng, một webhook có thể bị gửi lặp lại nhiều lần. Hãy thiết kế một Class `IdempotencyTracker` lưu trữ các `idempotency_key` và kết quả xử lý của các giao dịch trước đó. 
*   **Yêu cầu nâng cao**: Các `idempotency_key` chỉ được lưu trữ và có hiệu lực trong vòng **10 giây** (sliding window). Sau 10 giây, key đó phải tự động bị xóa (eviction) để tránh tràn bộ nhớ.
*   **Kỹ năng ôn luyện**: Dùng `collections.deque` để quản lý thời gian hết hạn của các key và `dict` để tra cứu nhanh kết quả giao dịch.

### Dạng 2: Rate Limiter (Token Bucket / Leaky Bucket)
*   **Đề bài**: Triển khai class `RateLimiter` để giới hạn số lượng request API của merchant (ví dụ: tối đa 5 requests mỗi giây).
*   **Yêu cầu**: API `is_allowed(merchant_id, timestamp)` nhận vào ID của merchant và thời điểm thực hiện request. Bạn phải tính toán xem số lượng token còn lại trong bucket của merchant đó là bao nhiêu (số token tự động hồi phục theo thời gian trôi qua) để quyết định cho phép hoặc từ chối request.
*   **Kỹ năng ôn luyện**: Phép toán nhân chia thời gian thực, quản lý trạng thái động của từng merchant mà không cần chạy thread chạy ngầm (chỉ tính toán hồi phục token lười - lazy recovery khi có request gọi tới).

### Dạng 3: Xử lý tiền tệ & Sai số tài chính (Precision Arithmetic)
*   **Đề bài**: Stripe thực hiện chuyển đổi tiền tệ từ USD sang EUR, JPY. Bạn nhận được danh sách giao dịch với số tiền lẻ dạng float và bảng tỷ giá.
*   **Yêu cầu**: Tuyệt đối không dùng kiểu dữ liệu `float` để tính toán tài chính trực tiếp vì lỗi làm tròn của máy tính (ví dụ: `0.1 + 0.2` trong máy tính sẽ ra `0.30000000000000004`). Bạn phải thiết kế chương trình chuyển đổi tất cả số tiền sang đơn vị **Cents (Số nguyên xu)**, thực hiện phép nhân/chia tỷ giá, áp dụng cơ chế làm tròn ngân hàng (Banker's rounding - làm tròn đến số chẵn gần nhất) và chuyển đổi ngược lại.
*   **Kỹ năng ôn luyện**: Sử dụng thư viện `decimal` hoặc nhân số tiền lên `100` để thao tác hoàn toàn trên số nguyên (`int`).
