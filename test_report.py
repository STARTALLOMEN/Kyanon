import pandas as pd
import pytest
from solution_py import build_report

def test_totals(tmp_path):
    """Test tính tổng amount theo ngày cho các đơn hàng completed"""
    # Arrange
    input_csv = tmp_path / "orders.csv"
    # minimal data
    df = pd.DataFrame({
        "order_id": [1, 2, 3],
        "order_date": ["2025-01-01 10:00:00", "2025-01-01 11:00:00", "2025-01-02 08:00:00"],
        "status": ["completed", "pending", "completed"],
        "amount": [100.0, 200.0, 50.0],
        "customer_id": [1, 2, 1]
    })
    df.to_csv(input_csv, index=False)
    output_csv = tmp_path / "report.csv"
    
    # Act
    build_report(str(input_csv), str(output_csv))
    
    # Assert
    out = pd.read_csv(output_csv)
    assert out["amount"].sum() == 150.0 
    assert len(out) == 2  # 2 ngày
    assert "date" in out.columns
    assert "amount" in out.columns

def test_filter_completed_only(tmp_path):
    """Test lọc chỉ các đơn hàng có status = completed"""
    # Arrange
    input_csv = tmp_path / "orders.csv"
    df = pd.DataFrame({
        "order_id": [1, 2, 3, 4],
        "order_date": ["2025-01-01 10:00:00"] * 4,
        "status": ["completed", "pending", "cancelled", "completed"],
        "amount": [100.0, 200.0, 300.0, 150.0],
        "customer_id": [1, 2, 3, 4]
    })
    df.to_csv(input_csv, index=False)
    output_csv = tmp_path / "report.csv"
    
    # Act
    build_report(str(input_csv), str(output_csv))
    
    # Assert
    out = pd.read_csv(output_csv)
    assert out["amount"].sum() == 250.0  
    assert len(out) == 1  # 1 ngày

def test_group_by_date(tmp_path):
    """Test group by theo ngày"""
    # Arrange
    input_csv = tmp_path / "orders.csv"
    df = pd.DataFrame({
        "order_id": [1, 2, 3],
        "order_date": ["2025-01-01 09:00:00", "2025-01-01 18:00:00", "2025-01-02 12:00:00"],
        "status": ["completed", "completed", "completed"],
        "amount": [100.0, 50.0, 200.0],
        "customer_id": [1, 2, 3]
    })
    df.to_csv(input_csv, index=False)
    output_csv = tmp_path / "report.csv"
    
    # Act
    build_report(str(input_csv), str(output_csv))
    
    # Assert
    out = pd.read_csv(output_csv)
    assert len(out) == 2 
    assert out.loc[out["date"] == "2025-01-01", "amount"].values[0] == 150.0  # 100 + 50
