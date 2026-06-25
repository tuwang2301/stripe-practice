# Lộ Trình Ôn Tập Virtual Onsite Stripe Cấp Tốc (7 Ngày)

Lộ trình này được thiết kế tối ưu nhất để giúp bạn sẵn sàng cho vòng **Virtual Onsite** trong vòng **7 ngày**, tập trung 100% vào những kỹ năng thực tế mà Stripe sẽ đánh giá (Correctness, Clean Code, Testing, và Communication) thay vì luyện thuật toán thuần túy.

---

## 📅 Tổng Quan Lộ Trình 7 Ngày

```mermaid
gantt
    title Lộ trình ôn tập 7 ngày
    dateFormat  D
    axisFormat %d
    
    section Lý thuyết & Công cụ
    Ngày 1: Chiến thuật & AI Tools       :active, d1, 0, 1d
    
    section Luyện Code Thực Tế
    Ngày 2: Stateful API & LRU           :d2, after d1, 1d
    Ngày 3: Graph & BFS                  :d3, after d2, 1d
    Ngày 4: Sliding Window & Deque       :d4, after d3, 1d
    Ngày 5: Business Matching & Date     :d5, after d4, 1d
    
    section Gỡ lỗi & Hội nhập
    Ngày 6: Bug Squashing & Integration  :d6, after d5, 1d
    
    section Vòng Hành Vi & Mock
    Ngày 7: STAR Framework & Phỏng vấn thử:d7, after d6, 1d
```

---

## 🎯 Chi Tiết Từng Ngày

### 🟢 Ngày 1: Nắm Vững Chiến Thuật & Làm Quen Vòng AI Programming Exercise (Mới 2026)
*   **Mục tiêu:** Hiểu rõ tiêu chí chấm điểm của Stripe, cơ chế phỏng vấn mới và cách hợp tác chặt chẽ với AI.
*   **Nhiệm vụ:**
    1.  Đọc kỹ [stripe_prep_guide.md](file:///D:/Projects/stripe-practice/theory_and_playbooks/stripe_prep_guide.md) và [virtual_onsite_strategy.md](file:///D:/Projects/stripe-practice/virtual_onsite/virtual_onsite_strategy.md).
    2.  Đọc tài liệu phỏng vấn chính thức của Stripe: [virtual_onsite_what_to_expect.md](file:///D:/Projects/stripe-practice/theory_and_playbooks/virtual_onsite_what_to_expect.md) và [api_and_ai_guide.md](file:///D:/Projects/stripe-practice/virtual_onsite/api_and_ai_guide.md).
    3.  Luyện tập quy trình "Collaborative Prompting": Tự nghĩ ra cấu trúc dữ liệu, dùng AI kiểm tra tính đúng đắn của thiết kế (Verify Approach), yêu cầu AI tạo khung code (Skeleton), sau đó mới viết các logic chi tiết. Tránh việc dán toàn bộ code lỗi và bảo AI tự sửa.
*   **Kỹ năng cần luyện:** Prompting để đối thoại và kiểm chứng logic thay vì phó mặc hoàn toàn cho AI, cùng với kỹ năng Think Out Loud.


### 🔵 Ngày 2: Thiết Kế Stateful API & Thuật Toán Trực Quan (LRU Cache)
*   **Mục tiêu:** Luyện tập thiết kế Class, quản lý trạng thái thời gian và cơ chế lưu trữ đệm.
*   **Nhiệm vụ:**
    1.  Đọc đề bài tại [01_account_scheduler/README.md](file:///D:/Projects/stripe-practice/virtual_onsite/01_account_scheduler/README.md).
    2.  Tự code lại Class `AccountScheduler` trong [01_account_scheduler/solution.py](file:///D:/Projects/stripe-practice/virtual_onsite/01_account_scheduler/solution.py) mà không nhìn code mẫu.
    3.  Chạy unit test để kiểm tra tính đúng đắn:
        ```powershell
        python virtual_onsite/01_account_scheduler/test_solution.py
        ```
*   **Kiến thức cốt lõi:** Nắm vững cách sử dụng `collections.OrderedDict` để quản lý thứ tự LRU một cách hiệu quả trong Python.

### 🔵 Ngày 3: Giải Quyết Bài Toán Đồ Thị & BFS
*   **Mục tiêu:** Làm quen với các bài toán liên kết thực thể (Entity Resolution) sử dụng cấu trúc đồ thị.
*   **Nhiệm vụ:**
    1.  Xem đề bài tại [02_find_linked_users/README.md](file:///D:/Projects/stripe-practice/virtual_onsite/02_find_linked_users/README.md).
    2.  Tự triển khai các thuật toán tìm kiếm liên kết trực tiếp, liên kết 2 bước (2-hop), và tìm toàn bộ thành phần liên thông (connected component).
    3.  Chạy unit test để đảm bảo bạn không mắc phải lỗi đè trạng thái `visited` trong đồ thị có chu trình.
*   **Kiến thức cốt lõi:** Sử dụng `collections.deque` để viết thuật toán BFS tìm kiếm khoảng cách ngắn nhất trên đồ thị không trọng số.

### 🔵 Ngày 4: Xử Lý Dòng Dữ Liệu Thời Gian Thực & Sliding Window
*   **Mục tiêu:** Quản lý dữ liệu thời gian trượt (sliding window) phục vụ cho giám sát dịch vụ (telemetry) hoặc giới hạn tần suất (rate limiting).
*   **Nhiệm vụ:**
    1.  Xem đề bài tại [03_detect_trigger_resolve/README.md](file:///D:/Projects/stripe-practice/virtual_onsite/03_detect_trigger_resolve/README.md).
    2.  Tự code lại cơ chế phát hiện sự kiện TRIGGER và RESOLVE.
    3.  Luyện tập cách gom nhóm theo khóa phụ và đảm bảo đầu ra được sắp xếp đúng thứ tự thời gian tuyến tính.
*   **Kiến thức cốt lõi:** Sử dụng Queue hai đầu (`collections.deque`) để loại bỏ các phần tử hết hạn (eviction) khỏi cửa sổ thời gian một cách tối ưu.

### 🔵 Ngày 5: Hệ Thống Khớp Hóa Đơn & Logic Nghiệp Vụ Phức Tạp
*   **Mục tiêu:** Thực hành viết code xử lý logic nghiệp vụ tài chính với nhiều thứ tự ưu tiên và cơ chế dung sai (forgiveness).
*   **Nhiệm vụ:**
    1.  Xem đề bài tại [04_payment_to_invoice/README.md](file:///D:/Projects/stripe-practice/virtual_onsite/04_payment_to_invoice/README.md).
    2.  Code cơ chế so khớp hóa đơn dựa trên số tiền chính xác, ngày tháng, mã định danh, và phạm vi sai số cho phép.
*   **Kiến thức cốt lõi:** Cách xử lý chuỗi CSV thô (không dùng thư viện ngoài), định dạng thời gian (`datetime.strptime`) và tại sao nên dùng số nguyên xu (`cents`) thay vì số thực (`float`) trong lập trình tài chính.

### 🟡 Ngày 6: Thực Hành Kỹ Năng Đọc Mã Nguồn (Bug Squash) & Tích Hợp (Integration)
*   **Mục tiêu:** Sẵn sàng cho bài phỏng vấn tìm lỗi (Bug Squash) và tích hợp thư viện.
*   **Nhiệm vụ:**
    1.  Tải về một thư viện mã nguồn mở nhỏ bằng Python trên GitHub (ví dụ: một phiên bản rút gọn của `requests` hoặc `flask`).
    2.  Luyện tập cách tìm kiếm nhanh một hàm hoặc một biến bằng các lệnh Shell (`grep` hoặc tính năng tìm kiếm của VS Code).
    3.  Tập viết thêm các ca kiểm thử mới (unit tests) để kiểm tra một đoạn mã nguồn lạ và sửa các lỗi nhỏ trong đó.
*   **Kỹ năng cần luyện:** Đọc hiểu nhanh cấu trúc thư mục của một dự án lớn, cách định vị code thông qua lỗi từ unit test.

### 🔴 Ngày 7: Chuẩn Bị Câu Hỏi Hành Vi (STAR) & Phỏng Vấn Thử (Mock Interview)
*   **Mục tiêu:** Tự tin vượt qua buổi phỏng vấn hành vi và làm quen với áp lực phòng thi.
*   **Nhiệm vụ:**
    1.  Chuẩn bị **3-4 câu chuyện thực tế** từ các dự án trước đây của bạn. Mỗi câu chuyện phải được viết sẵn theo cấu trúc **STAR** (Situation - Task - Action - Result).
    2.  Xem lại bảng [Operating Principles của Stripe](file:///D:/Projects/stripe-practice/theory_and_playbooks/virtual_onsite_what_to_expect.md#L195) để lồng ghép các nguyên tắc này vào câu trả lời của bạn.
    3.  Làm một bài thi thử (Mock Test): Chọn một bài tập bất kỳ trong 4 bài tập trên, đặt đồng hồ đếm ngược 45 phút, vừa code vừa tự nói to giải thích hướng đi của mình.
*   **Mẹo quan trọng:** Luôn chuẩn bị sẵn 2-3 câu hỏi thông minh để hỏi lại người quản lý ở cuối buổi (ví dụ: về định hướng phát triển sản phẩm của Stripe, văn hóa làm việc của team).

---

## 💡 Quy Tắc Vàng Khi Đi Phỏng Vấn
*   **Đọc kỹ đề bài (5 phút đầu):** Tuyệt đối không code ngay khi mới đọc dòng đầu tiên. Hãy hỏi làm rõ (clarify) các giả định: *"Đầu vào có bị null không?"*, *"Thời gian có luôn tăng dần không?"*, *"Có cần sắp xếp kết quả đầu ra không?"*.
*   **Ưu tiên code chạy được hơn code tối ưu:** Viết một giải thuật đơn giản (dù độ phức tạp là $O(N^2)$) nhưng chạy đúng 100% luôn tốt hơn viết giải thuật $O(N)$ phức tạp nhưng bị lỗi crash giữa chừng.
*   **Viết test liên tục:** Sau khi viết xong mỗi hàm nhỏ, hãy tự tạo test case đơn giản để chạy thử và chỉ ra lỗi trước khi người phỏng vấn phát hiện ra.
*   **Giữ thái độ hợp tác:** Đừng coi người phỏng vấn là người chấm thi, hãy coi họ là đồng nghiệp cùng giải quyết dự án.
