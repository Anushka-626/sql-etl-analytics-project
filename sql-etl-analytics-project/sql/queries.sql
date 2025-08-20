-- 1. Total revenue by month
SELECT
    strftime('%Y-%m', order_date) AS year_month,
    ROUND(SUM(calc_revenue), 2) AS total_revenue
FROM vw_order_lines
GROUP BY strftime('%Y-%m', order_date)
ORDER BY year_month;

-- 2. Top 10 products by revenue
SELECT
    product_id,
    category,
    ROUND(SUM(calc_revenue), 2) AS revenue
FROM vw_order_lines
GROUP BY product_id, category
ORDER BY revenue DESC
LIMIT 10;

-- 3. Revenue by product category and payment method
SELECT
    category,
    payment_method,
    ROUND(SUM(calc_revenue), 2) AS revenue
FROM vw_order_lines
GROUP BY category, payment_method
ORDER BY revenue DESC;
