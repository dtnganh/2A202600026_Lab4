from langchain_core.tools import tool

# ==============================================================================
# HÀM BỔ TRỢ: CHUẨN HÓA TÊN THÀNH PHỐ
# Giúp xử lý các cách gọi khác nhau: Sài Gòn -> Hồ Chí Minh, hn -> Hà Nội, v.v.
# ==============================================================================
def normalize_city(name: str) -> str:
    if not name:
        return name
    name = name.strip().lower()
    
    mapping = {
        "hồ chí minh": ["hồ chí minh", "ho chi minh", "sài gòn", "sai gon", "hcm", "tphcm", "tp hcm", "tp.hcm", "tp. hcm"],
        "hà nội": ["hà nội", "ha noi", "hn", "hanoi"],
        "đà nẵng": ["đà nẵng", "da nang", "dn", "danang"],
        "phú quốc": ["phú quốc", "phu quoc", "pq", "phuquoc"]
    }
    
    for canonical_name, synonyms in mapping.items():
        if name in synonyms:
            # Trả về định dạng chuẩn (Viết hoa chữ cái đầu cho đẹp)
            return canonical_name.title() if canonical_name != "hồ chí minh" else "Hồ Chí Minh"
            
    return name.title() # Nếu không tìm thấy, trả về dạng viết hoa chữ cái đầu

# ==============================================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# ==============================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ]
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ]
}

def format_currency(amount):
    return f"{amount:,}".replace(",", ".") + "đ"

@tool
def search_flights(origin: str, destination: str) -> str:
    """Tra cứu thông tin chuyến bay và giá vé giữa hai thành phố."""
    # Chuẩn hóa tên thành phố trước khi tra cứu
    origin = normalize_city(origin)
    destination = normalize_city(destination)
    
    flights = FLIGHTS_DB.get((origin, destination))
    
    # Logic: Nếu không thấy, thử tra ngược chiều (như yêu cầu trong ảnh)
    if not flights:
        reverse_flights = FLIGHTS_DB.get((destination, origin))
        if reverse_flights:
            flights = reverse_flights
            origin, destination = destination, origin 
            
    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."
    
    result = f"Danh sách chuyến bay từ {origin} đến {destination}:\n"
    for f in flights:
        result += f"- {f['airline']} ({f['class']}): {f['departure']} -> {f['arrival']} - Giá: {format_currency(f['price'])}\n"
    return result

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tra cứu danh sách khách sạn tại một thành phố (có thể lọc theo giá nếu có)."""
    # Chuẩn hóa tên thành phố trước khi tra cứu
    city = normalize_city(city)
    
    hotels = HOTELS_DB.get(city)
    
    if not hotels:
        return f"Không tìm thấy dữ liệu khách sạn tại {city}. Hiện tại hệ thống chỉ hỗ trợ: {', '.join(HOTELS_DB.keys())}"
    
    # Lọc theo giá và sắp xếp theo rating giảm dần
    filtered_hotels = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
    filtered_hotels.sort(key=lambda x: x['rating'], reverse=True)
    
    if not filtered_hotels:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {format_currency(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
    
    result = f"Danh sách khách sạn tại {city} (Giá tối đa {format_currency(max_price_per_night)}), sắp xếp theo đánh giá:\n"
    for h in filtered_hotels:
        result += f"- {h['name']} ({h['stars']}*): {format_currency(h['price_per_night'])}/đêm - Khu vực: {h['area']} - Đánh giá: {h['rating']}/5\n"
    return result

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi định dạng 'tên_khoản:số_tiền,tên_khoản:số_tiền'
    """
    try:
        expense_items = {}
        for item in expenses.split(","):
            item = item.strip()
            if not item: continue
            
            parts = item.split(":")
            if len(parts) != 2:
                return f"Lỗi định dạng khoản chi '{item}'. Vui lòng dùng format 'tên:số_tiền' (VD: vé_máy_bay:1200000)."
            
            name, amount = parts
            expense_items[name.strip()] = int(amount.strip())
            
        total_spent = sum(expense_items.values())
        remaining = total_budget - total_spent
        
        result = "Bảng chi phí:\n"
        for name, amount in expense_items.items():
            display_name = name.replace("_", " ").capitalize()
            result += f"- {display_name}: {format_currency(amount)}\n"
        
        result += "---\n"
        result += f"Tổng chi: {format_currency(total_spent)}\n"
        result += f"Ngân sách: {format_currency(total_budget)}\n"
        
        if remaining >= 0:
            result += f"Còn lại: {format_currency(remaining)}"
        else:
            result += f"Vượt ngân sách {format_currency(abs(remaining))}! Cần điều chỉnh."
            
        return result
    except ValueError:
        return "Lỗi: Số tiền chi phí phải là số nguyên (VD: khách_sạn:500000)."
    except Exception as e:
        return f"Lỗi hệ thống khi tính ngân sách: {str(e)}"
