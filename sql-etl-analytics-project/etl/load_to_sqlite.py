import os
import pandas as pd
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "raw")
DWH_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "warehouse")
os.makedirs(DWH_DIR, exist_ok=True)
DB_PATH = os.path.join(DWH_DIR, "warehouse.db")

def load_to_sqlite():
    # Load your CSV
    transactions = pd.read_csv(os.path.join(RAW_DIR, "transactions.csv"))

    # Save raw transactions to SQLite
    with sqlite3.connect(DB_PATH) as conn:
        transactions.to_sql("fact_orders", conn, if_exists="replace", index=False)

        # Create a revenue view (recalculate to ensure data consistency)
        conn.executescript("""
        DROP VIEW IF EXISTS vw_order_lines;
        CREATE VIEW vw_order_lines AS
        SELECT
            Transaction_ID AS order_id,
            Customer_ID AS customer_id,
            Product_ID AS product_id,
            Product_Category AS category,
            Product_Price AS unit_price,
            Quantity,
            Total_Amount,
            (Quantity * Product_Price) AS calc_revenue,
            Purchase_Date AS order_date,
            Payment_Method
        FROM fact_orders;
        """)
    print(f"Database created at: {DB_PATH}")

if __name__ == "__main__":
    load_to_sqlite()
