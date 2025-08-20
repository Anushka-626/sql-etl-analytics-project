# SQL + ETL + Visualization with Transactions Data

### Pipeline:
1. **ETL**: Load `transactions.csv` → SQLite DB.
2. **SQL**: Create view `vw_order_lines` with calculated revenue.
3. **Visualization**: Charts for revenue trends, top products, and payment methods.

### How to Run
```bash
python etl/load_to_sqlite.py
python analytics/visualize.py
