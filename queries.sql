-- 1) Total revenue (sales) by customer country
-- Shows total revenue grouped by the customer's country (orders -> orderdetails -> customers)
SELECT c.country,
       SUM(od.quantityordered * od.priceeach) AS total_revenue
FROM classicmodels.orderdetails od
JOIN classicmodels.orders o ON od.ordernumber = o.ordernumber
JOIN classicmodels.customers c ON o.customernumber = c.customernumber
GROUP BY c.country
ORDER BY total_revenue DESC;

-- 2) Top 10 products by revenue
-- For each product, compute total revenue and units sold, return top 10 by revenue
SELECT p.productcode,
       p.productname,
       SUM(od.quantityordered * od.priceeach) AS revenue,
       SUM(od.quantityordered) AS units_sold
FROM classicmodels.orderdetails od
JOIN classicmodels.products p ON od.productcode = p.productcode
GROUP BY p.productcode, p.productname
ORDER BY revenue DESC
LIMIT 10;

-- 3) Monthly sales trend (last 12 months)
-- Aggregates revenue per month for the last 12 months
SELECT date_trunc('month', o.orderdate)::date AS month,
       SUM(od.quantityordered * od.priceeach) AS revenue
FROM classicmodels.orders o
JOIN classicmodels.orderdetails od ON o.ordernumber = od.ordernumber
WHERE o.orderdate >= (current_date - INTERVAL '12 months')
GROUP BY 1
ORDER BY 1;

-- 4) Average order value per customer
-- For each customer compute average order total (sum of orderdetails per order) and list top 20
SELECT c.customernumber,
       c.customername,
       AVG(order_total) AS avg_order_value
FROM (
  SELECT o.ordernumber, o.customernumber, SUM(od.quantityordered * od.priceeach) AS order_total
  FROM classicmodels.orders o
  JOIN classicmodels.orderdetails od USING (ordernumber)
  GROUP BY o.ordernumber, o.customernumber
) t
JOIN classicmodels.customers c ON t.customernumber = c.customernumber
GROUP BY c.customernumber, c.customername
ORDER BY avg_order_value DESC
LIMIT 20;

-- 5) Number of orders by year and status
-- Counts orders grouped by calendar year and order status
SELECT EXTRACT(YEAR FROM orderdate)::INT AS year,
       status,
       COUNT(*) AS orders_count
FROM classicmodels.orders
GROUP BY year, status
ORDER BY year DESC, orders_count DESC;

-- 6) Sales representative performance
-- For each employee (as sales rep), show number of distinct customers, number of orders, and total revenue
SELECT e.employeenumber,
       (e.firstname || ' ' || e.lastname) AS sales_rep,
       COUNT(DISTINCT c.customernumber) AS customers_managed,
       COUNT(DISTINCT o.ordernumber) AS orders_count,
       SUM(od.quantityordered * od.priceeach) AS total_revenue
FROM classicmodels.employees e
LEFT JOIN classicmodels.customers c ON c.salesrepemployeenumber = e.employeenumber
LEFT JOIN classicmodels.orders o ON o.customernumber = c.customernumber
LEFT JOIN classicmodels.orderdetails od ON od.ordernumber = o.ordernumber
GROUP BY e.employeenumber, sales_rep
ORDER BY total_revenue DESC NULLS LAST
LIMIT 20;

-- 7) Average delivery time (in days) for shipped orders
-- Calculates average (shippeddate - orderdate) for orders that have been shipped
SELECT AVG((shippeddate - orderdate))::NUMERIC(10,2) AS avg_delivery_days
FROM classicmodels.orders
WHERE shippeddate IS NOT NULL;

-- 8) Payment coverage ratio per customer
-- For each customer: total payments, total invoiced (orders), and ratio payments/invoiced
SELECT c.customernumber,
       c.customername,
       COALESCE(pay.total_payments,0) AS total_payments,
       COALESCE(inv.total_invoiced,0) AS total_invoiced,
       CASE WHEN COALESCE(inv.total_invoiced,0) = 0 THEN NULL
            ELSE ROUND(pay.total_payments / inv.total_invoiced::NUMERIC, 4)
       END AS payment_coverage_ratio
FROM classicmodels.customers c
LEFT JOIN (
  SELECT customernumber, SUM(amount) AS total_payments
  FROM classicmodels.payments
  GROUP BY customernumber
) pay ON pay.customernumber = c.customernumber
LEFT JOIN (
  SELECT o.customernumber, SUM(od.quantityordered * od.priceeach) AS total_invoiced
  FROM classicmodels.orders o
  JOIN classicmodels.orderdetails od ON o.ordernumber = od.ordernumber
  GROUP BY o.customernumber
) inv ON inv.customernumber = c.customernumber
ORDER BY payment_coverage_ratio ASC NULLS LAST
LIMIT 20;

-- 9) Low-stock products with sales in the last 6 months
-- Find products with quantityinstock < 20 and show units sold in last 6 months
SELECT p.productcode,
       p.productname,
       p.quantityinstock,
       COALESCE(s.units_sold,0) AS units_sold_last_6m
FROM classicmodels.products p
LEFT JOIN (
  SELECT od.productcode, SUM(od.quantityordered) AS units_sold
  FROM classicmodels.orderdetails od
  JOIN classicmodels.orders o ON od.ordernumber = o.ordernumber
  WHERE o.orderdate >= current_date - INTERVAL '6 months'
  GROUP BY od.productcode
) s ON s.productcode = p.productcode
WHERE p.quantityinstock < 20
ORDER BY p.quantityinstock ASC, units_sold_last_6m DESC;

-- 10) Average number of items and lines per order
-- Computes average number of distinct product lines per order and average total units per order
SELECT ROUND(AVG(order_lines)::NUMERIC,2) AS avg_lines_per_order,
       ROUND(AVG(total_units)::NUMERIC,2) AS avg_units_per_order
FROM (
  SELECT o.ordernumber,
         COUNT(od.productcode) AS order_lines,
         SUM(od.quantityordered) AS total_units
  FROM classicmodels.orders o
  JOIN classicmodels.orderdetails od ON o.ordernumber = od.ordernumber
  GROUP BY o.ordernumber
) t;
