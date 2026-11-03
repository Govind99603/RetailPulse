from pathlib import Path
import pandas as pd

DATA = Path(__file__).parents[1] / "data" / "processed"

def test_derived_artifacts_schema():
    expected = {
        "customer_rfm_segments.csv": {"Customer ID", "Recency", "Frequency", "Monetary", "Segment"},
        "churn_proxy_features.csv": {"Customer ID", "Recency", "Frequency", "Monetary", "ChurnProxy"},
        "daily_total_demand.csv": {"InvoiceDate", "daily_units"},
        "monthly_sales_summary.csv": {"InvoiceMonth", "revenue", "units", "invoices", "customers"},
        "inventory_reorder_recommendations.csv": {"StockCode", "reorder_point", "suggested_order_qty"},
    }
    for name, cols in expected.items():
        p = DATA / name
        assert p.exists(), f"missing artifact {name}"
        df = pd.read_csv(p)
        assert cols.issubset(df.columns), f"schema mismatch in {name}"
