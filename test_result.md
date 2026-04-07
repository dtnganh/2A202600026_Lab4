# Kết quả Kiểm thử - Smart Travel Assistant

Bản báo cáo này tổng hợp các kịch bản kiểm thử (Test Cases) để đánh giá khả năng phản hồi, gọi công cụ và tuân thủ Persona của Agent TravelBuddy.

---

## Test Case 1: Khởi động và Gợi ý điểm đến
**Mục tiêu:** Kiểm tra khả năng chào hỏi và đưa ra gợi ý khi người dùng chưa có kế hoạch cụ thể.

> **Người dùng (15:00:50):**  
> Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.
>
> **TravelBuddy:**  
> Chào bạn! Có rất nhiều địa điểm tuyệt vời ở Việt Nam để khám phá. Bạn thích biển, núi, hay văn hóa lịch sử? Một số gợi ý như:
> 
> 1. Đà Nẵng - với bãi biển tuyệt đẹp và Bà Nà Hills.
> 2. Hội An - thành phố cổ xinh đẹp với ánh đèn lồng lung linh.
> 3. Nha Trang - nổi tiếng với bãi biển và các khu nghỉ dưỡng.
> 4. Hà Nội - mang đậm văn hóa và lịch sử.
> 5. Phú Quốc - đảo thiên đường với nước biển trong xanh.
> 
> Hãy cho mình biết bạn có ý tưởng nào trong đầu hoặc bạn thích khám phá phong cách nào nhé!

---

## Test Case 2: Tra cứu Chuyến bay (Single Tool)
**Mục tiêu:** Kiểm tra khả năng gọi search_flights và trình bày danh sách chuyến bay.

> **Người dùng (15:02:31):**  
> Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng
>
> **TravelBuddy:**  
> Dưới đây là các chuyến bay từ Hà Nội đi Đà Nẵng mà tôi tìm được:
> 
> 1. Vietnam Airlines (economy): 06:00 -> 07:20 - Giá: 1.450.000đ
> 2. Vietnam Airlines (business): 14:00 -> 15:20 - Giá: 2.800.000đ
> 3. VietJet Air (economy): 08:30 -> 09:50 - Giá: 890.000đ
> 4. Bamboo Airways (economy): 11:00 -> 12:20 - Giá: 1.200.000đ
> 
> Bạn muốn đặt chuyến bay nào hay cần thêm thông tin gì khác không?

---

## Test Case 3: Tư vấn trọn gói (Complex Workflow)
**Mục tiêu:** Kiểm tra khả năng kết hợp 3 công cụ: Chuyến bay -> Ngân sách -> Khách sạn.

> **Người dùng (15:03:36):**  
> Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!
>
> **TravelBuddy:**  
> Dưới đây là thông tin chuyến đi đến Phú Quốc cho bạn:
> 
> *   Chuyến bay: VietJet Air (economy) - 1.350.000đ
> *   Khách sạn:
>     *   9Station Hostel (2*): 200.000đ/đêm x 2 đêm = 400.000đ
>     *   Hoặc bạn có thể chọn Sol by Meliá (4*): 1.500.000đ/đêm x 2 đêm = 3.000.000đ
> 
> **Tổng chi phí ước tính:**
> - Với hostel: 1.350.000đ + 400.000đ = 1.750.000đ 
> - Với resort: 1.350.000đ + 3.000.000đ = 4.350.000đ
> 
> **Gợi ý thêm:** Nếu bạn muốn tiết kiệm, 9Station Hostel là một lựa chọn tốt. Ngoài ra, bạn nên thử các món hải sản tươi ngon trên đảo nhé!

---

## Test Case 4: Xử lý thông tin thiếu
**Mục tiêu:** Kiểm tra khả năng hỏi lại người dùng khi thiếu điểm đến/ngân sách cho khách sạn.

> **Người dùng (15:04:43):**  
> Tôi muốn đặt khách sạn
>
> **TravelBuddy:**  
> Để giúp bạn đặt khách sạn, mình cần biết bạn muốn thuê khách sạn ở thành phố nào và ngân sách mỗi đêm của bạn là bao nhiêu?

---

## Test Case 5: Ràng buộc Persona (Constraints)
**Mục tiêu:** Đảm bảo Agent từ chối các yêu cầu ngoài phạm vi du lịch.

> **Người dùng (15:05:19):**  
> Giải giúp tôi bài tập Python về Linkedlist.
>
> **TravelBuddy:**  
> Xin lỗi, mình không thể giúp bạn với bài tập Python hay lập trình cụ thể. Nhưng nếu bạn cần tư vấn về du lịch hoặc đặt vé, khách sạn, mình rất sẵn lòng hỗ trợ!

---

