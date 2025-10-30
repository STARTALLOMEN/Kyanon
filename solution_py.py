import pandas as pd
import argparse
import json

def build_report(input_csv: str, output_csv: str = "report.csv") -> None:
    """
    Xử lý dữ liệu đơn hàng:
    1. Đọc file orders.csv
    2. Lọc các đơn hàng có status = completed
    3. Tính tổng amount theo ngày
    4. Xuất ra file report.csv và hiển thị JSON format
    
    Args:
        input_csv: Đường dẫn file orders.csv
        output_csv: Đường dẫn file report.csv output
    """
    print(f"📖 Đọc dữ liệu từ {input_csv}...")
    
    df = pd.read_csv(input_csv, parse_dates=["order_date"])
    print(f"   Tổng số đơn hàng: {len(df)}")
    
    df = df[df["status"].eq("completed")].copy()
    print(f"   Đơn hàng completed: {len(df)}")
    
    df['date'] = df['order_date'].dt.date
    report = df.groupby('date', as_index=False)['amount'].sum()
    
    report["amount"] = report["amount"].round(2)
    
    result_json = report.to_dict('records')
    result_json = [{"date": str(row['date']), "amount": str(row['amount'])} for row in result_json]
    
    print("\n📊 Kết quả (JSON format):")
    print(json.dumps(result_json, indent=2, ensure_ascii=False))
    
    report.to_csv(output_csv, index=False)
    print(f"\n✅ Đã xuất kết quả ra file {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build daily revenue report from orders.csv")
    parser.add_argument("--input", "-i", default="orders.csv", help="Path to input orders.csv")
    parser.add_argument("--output", "-o", default="report.csv", help="Path to output report.csv")
    args = parser.parse_args()
    build_report(args.input, args.output)
