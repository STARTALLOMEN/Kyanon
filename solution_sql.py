import sqlite3
import pandas as pd
import json

def process_orders_sql(input_file='orders.csv', output_file='report.csv', db_file='orders.db'):
    """
    Xử lý dữ liệu đơn hàng bằng SQL:
    1. Import dữ liệu từ CSV vào SQLite
    2. Thực hiện query SQL để lọc và tính tổng
    3. Xuất kết quả ra file report.csv
    
    Args:
        input_file (str): Đường dẫn file orders.csv
        output_file (str): Đường dẫn file report.csv
        db_file (str): Đường dẫn file SQLite database
    """
    
    print(f"📖 Import dữ liệu từ {input_file} vào SQLite...")
    conn = sqlite3.connect(db_file)
    
    df = pd.read_csv(input_file)
    df.to_sql('orders', conn, if_exists='replace', index=False)
    print(f"   Đã import {len(df)} đơn hàng vào database")
    
    query = """
    SELECT 
        DATE(order_date) as date,
        ROUND(SUM(amount), 2) as amount
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE(order_date)
    ORDER BY DATE(order_date)
    """
    
    print("\n🔍 Thực hiện SQL query:")
    print(query)
    
    result = pd.read_sql_query(query, conn)
    print(f"   Tìm thấy {len(result)} ngày có đơn hàng completed")
    
    # Chuyển đổi sang định dạng JSON như yêu cầu
    result_json = result.to_dict('records')
    result_json = [{"date": row['date'], "amount": str(row['amount'])} for row in result_json]
    
    print("\n📊 Kết quả (JSON format):")
    print(json.dumps(result_json, indent=2, ensure_ascii=False))
    
    # Bước 4: Xuất ra file report.csv
    result.to_csv(output_file, index=False)
    print(f"\n✅ Đã xuất kết quả ra file {output_file}")
    
    # Đóng kết nối
    conn.close()
    
    return result

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build daily revenue report using SQL")
    parser.add_argument("--input", "-i", default="orders.csv", help="Path to input orders.csv")
    parser.add_argument("--output", "-o", default="report.csv", help="Path to output report.csv")
    parser.add_argument("--db", "-d", default="orders.db", help="Path to SQLite database")
    args = parser.parse_args()
    
    process_orders_sql(args.input, args.output, args.db)
