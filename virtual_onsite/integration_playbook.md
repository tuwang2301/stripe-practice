# Stripe Integration Interview: Step-by-Step Playbook

Đây là cẩm nang từng bước giúp bạn phân bổ thời gian, giao tiếp với người phỏng vấn, và triển khai code một cách bài bản trong 60 phút của buổi phỏng vấn Integration.

---

## ⏱️ Tổng quan phân bổ thời gian (60 Phút)
*   **Phút 00 - 05**: Settling in & kiểm tra kết nối/editor setup.
*   **Phút 05 - 10**: Đọc đề (Step 1) & Làm rõ yêu cầu với interviewer (Step 2).
*   **Phút 10 - 15**: Viết cấu trúc giải thuật bằng bình luận (Step 3).
*   **Phút 15 - 45**: Code & Nói to suy nghĩ của mình (Step 4).
*   **Phút 45 - 55**: Chạy test, bổ sung test case ẩn và xử lý biên (Step 5).
*   **Phút 55 - 60**: Hỏi đáp & kết thúc.

---

## 📘 Step 1: Đọc đề & Xác định các yếu tố cốt lõi (3 - 5 Phút)

Khi nhận đề bài từ người phỏng vấn, bạn không nên gõ code ngay lập tức. Hãy đọc kỹ spec và nháp ra giấy/comment 4 điểm sau:
1.  **Các phương thức HTTP & Endpoints**: Cần gọi endpoint nào? Tham số truyền vào là query params hay JSON body?
2.  **Yêu cầu Phân trang (Pagination)**: Dùng offset hay cursor-based (`starting_after`)? Trạng thái dừng vòng lặp là gì?
3.  **Quy tắc xử lý lỗi**: 
    *   Gặp lỗi Rate Limit (HTTP 429) xử lý thế nào? (Thường là sleep 1 giây và thử lại).
    *   Gặp lỗi thảm họa (4xx/5xx khác) xử lý thế nào? (Bỏ qua bản ghi lỗi chạy tiếp hay dừng hẳn trả về mặc định?).
4.  **Dữ liệu đầu ra**: Ghi ra file CSV, xuất file JSON, hay trả về một tuple/dict?

---

## 🗣️ Step 2: Giải thích hiểu biết & Làm rõ với Interviewer (2 - 3 Phút)

Sau khi đọc đề, hãy tóm tắt lại bài toán cho interviewer nghe để xác nhận bạn không hiểu sai đề.

**Mẫu câu nói tiếng Anh tham khảo:**
> *"To make sure I fully understand the requirements, our goal is to build a sync engine that fetches all pending transactions from the paginated GET `/v1/transactions` endpoint, calculates their sum, and then calls the POST `/v1/payouts` to reconcile them, correct?"*

**Các câu hỏi làm rõ biên (Edge-case clarifying questions) cực điểm cộng:**
*   *"If a single transaction detail lookup fails with a 500 error, should I skip this transaction and process the next ones, or should the whole script fail immediately?"*
*   *"Can I assume the input timestamps are always in UTC, or do I need to normalize them to timezone aware UTC datetimes?"*
*   *"For the CSV output, if the target directory doesn't exist, should I create it automatically or assume it is pre-configured?"*

---

## 📝 Step 3: Xây dựng cấu trúc bằng bình luận (3 - 5 Phút)

Trước khi viết bất kỳ hàm Python nào, hãy tạo cấu trúc sườn bằng comment ngay bên trong hàm. Điều này giúp interviewer thấy được logic của bạn trước khi bạn code và tránh việc bạn bị rối giữa chừng.

**Ví dụ cấu trúc comment:**
```python
def reconcile_payouts(api_url, api_token):
    # 1. Clean base URL and configure auth headers
    
    # 2. Fetch all pending payouts (handle HTTP 429 retries)
    
    # 3. Iterate over each payout defensively
    
    # 4. Fetch associated transactions (handle HTTP 429 and error skips)
    
    # 5. Sum the transaction amounts safely
    
    # 6. Reconcile or Flag the payout based on matching amount
    
    # 7. Return the final reconciled/flagged counts
```

---

## 💻 Step 4: Viết Code & Nói to suy nghĩ (25 - 30 Phút)

Bắt đầu chuyển hóa các bình luận thành code. **Quy tắc quan trọng: Vừa viết vừa nói (Think Out Loud).**

**Ví dụ khi viết khối `try-except` lồng nhau:**
> *"I'm going to wrap this transaction API call in a nested try-except block. This ensures that if a single transaction query fails with a 500 error, we can log it, set a `skip_payout` flag, and use `continue` to proceed to the next payout. This fulfills the requirement of skipping failed records without crashing the whole application."*

**Ví dụ khi xử lý Rate Limit:**
> *"Since Stripe API mock can return 429 rate limit errors, I will implement a `while True` retry loop. If `response.status_code == 429`, we will sleep for 1 second and retry the same request. Otherwise, we break the loop after a successful call."*

**Ví dụ khi parse URL:**
> *"I will use `api_url.rstrip('/')` to clean any trailing slash from the interviewer's host, and join it with the path variables. This avoids double slashes in the request and prevents missing schema errors."*

---

## 🧪 Step 5: Chạy thử & Chứng minh độ chính xác (5 - 10 Phút)

Khi code xong, đừng bảo là đã xong ngay. Hãy chủ động chạy test và tối ưu hóa:
1.  **Chạy test suite có sẵn**: `python solution.py` và chỉ ra kết quả thành công.
2.  **Chủ động bổ sung test case ẩn (Proactive Testing)**:
    *   *"Now that the happy path is passing, I want to write a quick assertion to verify how my code handles an empty list of payouts or a scenario where the API server returns a 500 error."*
3.  **Khẳng định tính đúng đắn**:
    > *"By checking that we filter out non-active items, retry on 429s, skip individual record errors, and normalize all timezone comparisons, I am confident this solution is robust and correct."*
