

# Câu 2: Bài tập Kỹ thuật - Data Aggregation

## 📋 Đề bài

**Dữ liệu đầu vào:** `orders.csv` với cấu trúc:
```csv
order_id,order_date,customer_id,amount,status
1,2025-09-01,1001,250,completed
2,2025-09-01,1002,300,pending
3,2025-09-02,1001,100,completed
```

**Yêu cầu:**
- Sử dụng **Python** hoặc **SQL** thực hiện:
  1. Đọc hoặc import dữ liệu từ `orders.csv`
  2. Lọc các đơn hàng có `status = completed`
  3. Tính tổng `amount` theo ngày và xuất ra file `report.csv`

**Output mong muốn:**
```json
[
  {"date": "2025-09-01", "amount": "250"},
  {"date": "2025-09-02", "amount": "100"}
]
```

---

## 🚀 Cài đặt

### 1. Clone hoặc tải project

```bash
cd d:\Kyanon
```

### 2. Cài đặt dependencies

```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt environment (Windows PowerShell)
venv\Scripts\activate

# Cài đặt thư viện
pip install -r requirements.txt
```

---

## 1) Python solution (pandas)

### Chạy chương trình

```bash
# Cách 1: Sử dụng file mặc định (orders.csv -> report.csv)
python solution_py.py

# Cách 2: Chỉ định file input/output
python solution_py.py --input orders.csv --output report.csv

# Cách 3: Rút gọn
python solution_py.py -i orders.csv -o report.csv
```

### Output

Chương trình sẽ hiển thị:
```
📖 Đọc dữ liệu từ orders.csv...
   Tổng số đơn hàng: 12
   Đơn hàng completed: 7

📊 Kết quả (JSON format):
[
  {
    "date": "2025-01-05",
    "amount": "330.5"
  },
  {
    "date": "2025-01-06",
    "amount": "75.25"
  },
  {
    "date": "2025-01-07",
    "amount": "389.99"
  },
  {
    "date": "2025-01-08",
    "amount": "59.98"
  },
  {
    "date": "2025-01-09",
    "amount": "500.0"
  }
]

✅ Đã xuất kết quả ra file report.csv
```

File `report.csv` sẽ có nội dung:
```csv
date,amount
2025-01-05,330.5
2025-01-06,75.25
2025-01-07,389.99
2025-01-08,59.98
2025-01-09,500.0
```

### Giải thích code

File `solution_py.py` thực hiện:
1. **Đọc CSV:** Sử dụng `pd.read_csv()` với `parse_dates=["order_date"]`
2. **Lọc dữ liệu:** Giữ lại các đơn hàng có `status == "completed"`
3. **Group by ngày:** Sử dụng `df["order_date"].dt.date` để bỏ phần giờ
4. **Tính tổng:** Dùng `.sum()` để tính tổng `amount` theo ngày
5. **Round số:** `.round(2)` để tránh lỗi floating point
6. **Xuất JSON:** Hiển thị kết quả theo format yêu cầu
7. **Xuất CSV:** Lưu thành file với `index=False`

## 2) SQL solution

### Các SQL queries thuần túy

File [`queries.sql`](queries.sql) chứa các SQL queries cho nhiều loại database:
- **MySQL/PostgreSQL:** `DATE(order_date)` → `GROUP BY` date
- **SQL Server:** `CAST(order_date AS date)`
- **SQLite:** `strftime('%Y-%m-%d', order_date)` for text-based datetime

### Chạy SQL solution với Python + SQLite

```bash
# Chạy với file mặc định
python solution_sql.py

# Hoặc chỉ định file
python solution_sql.py --input orders.csv --output report.csv
```

### Output

```
📖 Import dữ liệu từ orders.csv vào SQLite...
   Đã import 12 đơn hàng vào database

🔍 Thực hiện SQL query:

    SELECT 
        DATE(order_date) as date,
        ROUND(SUM(amount), 2) as amount
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE(order_date)
    ORDER BY DATE(order_date)
    
   Tìm thấy 5 ngày có đơn hàng completed

📊 Kết quả (JSON format):
[
  {
    "date": "2025-01-05",
    "amount": "330.5"
  },
  {
    "date": "2025-01-06",
    "amount": "75.25"
  },
  ...
]

✅ Đã xuất kết quả ra file report.csv
```

### Giải thích SQL

```sql
SELECT 
    DATE(order_date) as date,        -- Lấy phần DATE (bỏ giờ)
    ROUND(SUM(amount), 2) as amount  -- Tính tổng và làm tròn
FROM orders
WHERE status = 'completed'           -- Lọc chỉ completed
GROUP BY DATE(order_date)            -- Nhóm theo ngày
ORDER BY DATE(order_date)            -- Sắp xếp theo ngày
```

## 3) Testing

### Cài đặt pytest

```bash
pip install pytest
```

### Chạy test

```bash
# Chạy tất cả test
pytest test_report.py -v

# Chạy test cụ thể
pytest test_report.py::test_totals -v
```

### Các test case

File `test_report.py` bao gồm:
1. **test_totals:** Kiểm tra tổng amount tính đúng
2. **test_filter_completed_only:** Kiểm tra lọc chỉ status = completed
3. **test_group_by_date:** Kiểm tra group by theo ngày (bỏ giờ)

---


## 📁 Cấu trúc file

```
d:\Kyanon\
├── orders.csv              # Dữ liệu đầu vào (12 đơn hàng)
├── report.csv              # Kết quả output
├── solution_py.py          # Giải pháp Python (Pandas)
├── solution_sql.py         # Giải pháp SQL (SQLite)
├── queries.sql             # SQL queries thuần túy
├── test_report.py          # Unit tests
├── requirements.txt        # Dependencies
├── orders.db              # SQLite database (tự động tạo)
└── README.md              # Hướng dẫn này
```

---

## ✅ Kết quả

**Dữ liệu mẫu:** 12 đơn hàng trong `orders.csv`
- 7 đơn completed
- 2 đơn pending
- 1 đơn cancelled
- 1 đơn refunded
- 1 đơn không có thời gian cụ thể

**Kết quả báo cáo:** 5 ngày có doanh thu
- 2025-01-05: 330.5 (= 120.5 + 210.0)
- 2025-01-06: 75.25
- 2025-01-07: 389.99 (= 340.0 + 49.99)
- 2025-01-08: 59.98 (= 19.99 + 39.99)
- 2025-01-09: 500.0

**Tổng doanh thu:** 1,355.72

---

## 👤 Tác giả

**Dinh Trieu Bui**

Bài làm cho Câu 2 - Bài tập Kỹ thuật Data Aggregation

*Ngày hoàn thành: Tháng 10, 2025*
