-- Example SQL queries to aggregate sales data

-- Create a simple table
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    date TEXT,
    region TEXT,
    amount REAL
);

-- Example: total sales by region
-- SELECT region, SUM(amount) AS total FROM sales GROUP BY region ORDER BY total DESC;
