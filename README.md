## Tinh năng nổi bật

- Tư vấn thông minh: Tự động nhận diện điểm đến và nhu cầu của người dùng.
- Quy trình ReAct (Reason + Act): Agent biết suy nghĩ, gọi công cụ, và tổng hợp kết quả.
- Công cụ tùy chỉnh (Custom Tools):
  - search_flights: Tìm kiếm vé máy bay (có hỗ trợ tìm kiếm đảo chiều).
  - search_hotels: Tìm khách sạn theo thành phố và ngân sách, sắp xếp theo điểm đánh giá (rating).
  - calculate_budget: Tự động tính toán số tiền còn lại để tối ưu hóa lựa chọn khách sạn.
- Hệ thống Nhật ký và Dấu vết:
  - logs/: Lưu trữ lịch sử trò chuyện chi tiết.
  - traces/: Chụp lại từng bước suy nghĩ nội bộ của Agent để phục vụ gỡ lỗi (debugging).
- Cơ chế Fallback: Tự động xử lý lỗi API OpenAI và thông báo nhẹ nhàng cho người dùng.

---

## Hướng dẫn cài đặt

### 1. Chuẩn bị môi trường
Tạo môi trường ảo và cài đặt các thư viện cần thiết:
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install langgraph langchain-openai python-dotenv
```

### 2. Cấu hình API Key
Tạo file .env trong thư mục gốc và thêm khóa OpenAI của bạn:
```text
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Khởi chạy Agent
Sử dụng giao diện Terminal để trò chuyện với Agent:
```powershell
python agent.py
```

---

## Cau truc thư mục

- agent.py: File thực thi chính, định nghĩa đồ thị LangGraph và vòng lặp trò chuyện.
- tools.py: Định nghĩa các công cụ (Mock Tools) và cơ sở dữ liệu giả lập.
- system_prompt.txt: Chứa Persona, luật lệ và hướng dẫn cho Agent (định dạng XML).
- logs/: Nơi lưu trữ lịch sử chat hằng ngày.
- traces/: Nơi lưu trữ luồng suy nghĩ chi tiết dưới dạng JSON.
- test_result.md: Báo cáo kết quả kiểm thử các kịch bản thực tế.

---

## Quy tắc hoạt động (System Rules)

Agent tuân thủ nghiêm ngặt các quy tắc:
1. Luôn ưu tiên tra cứu thông tin ngay lập tức thay vì hỏi lại người dùng.
2. Không bao giờ bịa đặt thông tin nếu không có dữ liệu từ công cụ.
3. Chỉ đặt câu hỏi khi thiếu thông tin cốt lõi (như tên thành phố).
4. Phản hồi thân thiện, tự nhiên như một người bạn du lịch.

---
*Dự án được thực hiện trong khuôn khổ Lab 4 - Xây dựng AI Agent với LangGraph.*
