import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), "data", "warehouse", "warehouse.db")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

with sqlite3.connect(DB_PATH) as conn:
    # Refresh the view each time
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

    # Queries
    revenue_by_month = pd.read_sql("""
        SELECT strftime('%Y-%m', order_date) AS year_month,
               SUM(calc_revenue) AS total_revenue
        FROM vw_order_lines
        GROUP BY 1 ORDER BY 1
    """, conn)

    top_products = pd.read_sql("""
        SELECT product_id, SUM(calc_revenue) AS revenue
        FROM vw_order_lines
        GROUP BY product_id
        ORDER BY revenue DESC
        LIMIT 10
    """, conn)

    revenue_by_payment = pd.read_sql("""
        SELECT  Payment_Method, SUM(calc_revenue) AS revenue
        FROM vw_order_lines
        GROUP BY  Payment_Method
        ORDER BY revenue DESC
    """, conn)

    revenue_by_category = pd.read_sql("""
    SELECT category, SUM(calc_revenue) AS revenue
    FROM vw_order_lines
    GROUP BY category
    ORDER BY revenue DESC
""", conn)


# Plot 1: Revenue by Month
plt.figure()
plt.plot(revenue_by_month['year_month'], revenue_by_month['total_revenue'], marker='o')
plt.title('Total Revenue by Month')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'revenue_by_month.png'))
plt.close()

# Plot 2: Top 10 Products by Revenue
plt.figure()
plt.barh(top_products['product_id'], top_products['revenue'])
plt.title('Top 10 Products by Revenue')
plt.xlabel('Revenue')
plt.ylabel('Product ID')
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'top_products.png'))
plt.close()

# Plot 3: Revenue by Payment Method
plt.figure()
plt.bar(revenue_by_payment['Payment_Method'], revenue_by_payment['revenue'])
plt.title('Revenue by Payment Method')
plt.xlabel('Payment Method')
plt.ylabel('Revenue')
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'revenue_by_payment.png'))
plt.close()

plt.figure()
plt.bar(revenue_by_category['category'], revenue_by_category['revenue'])
plt.title('Revenue by Category')
plt.xlabel('Category')
plt.ylabel('Revenue')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, 'revenue_by_category.png'))
plt.close()


print("✅ Charts saved in analytics/plots/")
