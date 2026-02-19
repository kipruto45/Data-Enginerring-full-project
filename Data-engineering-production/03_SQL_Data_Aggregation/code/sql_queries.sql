-- SQL Data Aggregation Examples
-- This file contains sample queries for analyzing sales data.
-- Load data first: SQLite will create tables on INSERT or use existing ones.

-- Create sales table (if not exists - handled by Python wrapper)
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    region TEXT NOT NULL,
    product TEXT,
    amount REAL NOT NULL,
    quantity INTEGER DEFAULT 1
);

-- Total sales by region
SELECT region, SUM(amount) as total_sales, COUNT(*) as num_transactions
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

-- Average sale amount by region
SELECT region, AVG(amount) as avg_sale, MIN(amount) as min_sale, MAX(amount) as max_sale
FROM sales
GROUP BY region;

-- Sales by product
SELECT product, SUM(amount) as total_sales, SUM(quantity) as total_qty, COUNT(*) as num_sales
FROM sales
WHERE product IS NOT NULL
GROUP BY product
ORDER BY total_sales DESC;

-- Daily sales trend
SELECT date, SUM(amount) as daily_total, COUNT(*) as num_transactions
FROM sales
GROUP BY date
ORDER BY date;

-- Top regions by sales
SELECT region, SUM(amount) as total, COUNT(*) as count
FROM sales
GROUP BY region
HAVING SUM(amount) > 0
ORDER BY total DESC
LIMIT 5;

