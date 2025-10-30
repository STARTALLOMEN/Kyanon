-- Standard SQL (MySQL/PostgreSQL) when order_date is DATETIME/TIMESTAMP
SELECT DATE(order_date) AS date, SUM(amount) AS amount
FROM orders
WHERE status = 'completed'
GROUP BY DATE(order_date)
ORDER BY DATE(order_date);

-- SQL Server variant
SELECT CAST(order_date AS date) AS date, SUM(amount) AS amount
FROM dbo.orders
WHERE status = 'completed'
GROUP BY CAST(order_date AS date)
ORDER BY CAST(order_date AS date);

-- SQLite variant (if order_date is stored as text)
SELECT strftime('%Y-%m-%d', order_date) AS date, SUM(amount) AS amount
FROM orders
WHERE status = 'completed'
GROUP BY strftime('%Y-%m-%d', order_date)
ORDER BY date;
