#!/usr/bin/env python3
"""
Run a set of pre-defined SQL queries against a PostgreSQL database (schema: classicmodels),
print results to the terminal, and optionally save each result to CSV.

Requirements:
  - Python 3.8+
  - psycopg2-binary (or psycopg2)
  - (optional) tabulate for pretty CLI tables

Install deps:
  pip install psycopg2-binary tabulate
"""

import argparse
import csv
import sys
import time
from decimal import Decimal

try:
    import psycopg2
    import psycopg2.extras
except Exception as e:
    print("Missing dependency 'psycopg2'. Install with: pip install psycopg2-binary", file=sys.stderr)
    raise

try:
    from tabulate import tabulate
    HAVE_TABULATE = True
except Exception:
    HAVE_TABULATE = False

QUERIES = [
    ("1_total_revenue_by_country",
     "-- Total revenue (sales) by customer country\n"
     "SELECT c.country,\n"
     "       SUM(od.quantityordered * od.priceeach) AS total_revenue\n"
     "FROM classicmodels.orderdetails od\n"
     "JOIN classicmodels.orders o ON od.ordernumber = o.ordernumber\n"
     "JOIN classicmodels.customers c ON o.customernumber = c.customernumber\n"
     "GROUP BY c.country\n"
     "ORDER BY total_revenue DESC;"),
    ("2_top10_products_by_revenue",
     "-- Top 10 products by revenue\n"
     "SELECT p.productcode,\n"
     "       p.productname,\n"
     "       SUM(od.quantityordered * od.priceeach) AS revenue,\n"
     "       SUM(od.quantityordered) AS units_sold\n"
     "FROM classicmodels.orderdetails od\n"
     "JOIN classicmodels.products p ON od.productcode = p.productcode\n"
     "GROUP BY p.productcode, p.productname\n"
     "ORDER BY revenue DESC\n"
     "LIMIT 10;"),
    ("3_monthly_sales_last_12m",
     "-- Monthly sales trend (last 12 months)\n"
     "SELECT date_trunc('month', o.orderdate)::date AS month,\n"
     "       SUM(od.quantityordered * od.priceeach) AS revenue\n"
     "FROM classicmodels.orders o\n"
     "JOIN classicmodels.orderdetails od ON o.ordernumber = od.ordernumber\n"
     "WHERE o.orderdate >= (current_date - INTERVAL '12 months')\n"
     "GROUP BY 1\n"
     "ORDER BY 1;"),
    ("4_avg_order_value_per_customer",
     "-- Average order value per customer (top 20)\n"
     "SELECT c.customernumber,\n"
     "       c.customername,\n"
     "       AVG(order_total) AS avg_order_value\n"
     "FROM (\n"
     "  SELECT o.ordernumber, o.customernumber, SUM(od.quantityordered * od.priceeach) AS order_total\n"
     "  FROM classicmodels.orders o\n"
     "  JOIN classicmodels.orderdetails od USING (ordernumber)\n"
     "  GROUP BY o.ordernumber, o.customernumber\n"
     ") t\n"
     "JOIN classicmodels.customers c ON t.customernumber = c.customernumber\n"
     "GROUP BY c.customernumber, c.customername\n"
     "ORDER BY avg_order_value DESC\n"
     "LIMIT 20;"),
    ("5_orders_by_year_and_status",
     "-- Number of orders by year and status\n"
     "SELECT EXTRACT(YEAR FROM orderdate)::INT AS year,\n"
     "       status,\n"
     "       COUNT(*) AS orders_count\n"
     "FROM classicmodels.orders\n"
     "GROUP BY year, status\n"
     "ORDER BY year DESC, orders_count DESC;"),
    ("6_sales_rep_performance",
     "-- Sales representative performance\n"
     "SELECT e.employeenumber,\n"
     "       (e.firstname || ' ' || e.lastname) AS sales_rep,\n"
     "       COUNT(DISTINCT c.customernumber) AS customers_managed,\n"
     "       COUNT(DISTINCT o.ordernumber) AS orders_count,\n"
     "       SUM(od.quantityordered * od.priceeach) AS total_revenue\n"
     "FROM classicmodels.employees e\n"
     "LEFT JOIN classicmodels.customers c ON c.salesrepemployeenumber = e.employeenumber\n"
     "LEFT JOIN classicmodels.orders o ON o.customernumber = c.customernumber\n"
     "LEFT JOIN classicmodels.orderdetails od ON od.ordernumber = o.ordernumber\n"
     "GROUP BY e.employeenumber, sales_rep\n"
     "ORDER BY total_revenue DESC NULLS LAST\n"
     "LIMIT 20;"),
    ("7_avg_delivery_days_for_shipped_orders",
     "-- Average delivery time (in days) for shipped orders\n"
     "SELECT AVG((shippeddate - orderdate))::NUMERIC(10,2) AS avg_delivery_days\n"
     "FROM classicmodels.orders\n"
     "WHERE shippeddate IS NOT NULL;"),
    ("8_payment_coverage_ratio_per_customer",
     "-- Payment coverage ratio per customer\n"
     "SELECT c.customernumber,\n"
     "       c.customername,\n"
     "       COALESCE(pay.total_payments,0) AS total_payments,\n"
     "       COALESCE(inv.total_invoiced,0) AS total_invoiced,\n"
     "       CASE WHEN COALESCE(inv.total_invoiced,0) = 0 THEN NULL\n"
     "            ELSE ROUND(pay.total_payments / inv.total_invoiced::NUMERIC, 4)\n"
     "       END AS payment_coverage_ratio\n"
     "FROM classicmodels.customers c\n"
     "LEFT JOIN (\n"
     "  SELECT customernumber, SUM(amount) AS total_payments\n"
     "  FROM classicmodels.payments\n"
     "  GROUP BY customernumber\n"
     ") pay ON pay.customernumber = c.customernumber\n"
     "LEFT JOIN (\n"
     "  SELECT o.customernumber, SUM(od.quantityordered * od.priceeach) AS total_invoiced\n"
     "  FROM classicmodels.orders o\n"
     "  JOIN classicmodels.orderdetails od ON o.ordernumber = od.ordernumber\n"
     "  GROUP BY o.customernumber\n"
     ") inv ON inv.customernumber = c.customernumber\n"
     "ORDER BY payment_coverage_ratio ASC NULLS LAST\n"
     "LIMIT 20;"),
    ("9_low_stock_products_with_sales_last_6m",
     "-- Low-stock products with sales in the last 6 months\n"
     "SELECT p.productcode,\n"
     "       p.productname,\n"
     "       p.quantityinstock,\n"
     "       COALESCE(s.units_sold,0) AS units_sold_last_6m\n"
     "FROM classicmodels.products p\n"
     "LEFT JOIN (\n"
     "  SELECT od.productcode, SUM(od.quantityordered) AS units_sold\n"
     "  FROM classicmodels.orderdetails od\n"
     "  JOIN classicmodels.orders o ON od.ordernumber = o.ordernumber\n"
     "  WHERE o.orderdate >= current_date - INTERVAL '6 months'\n"
     "  GROUP BY od.productcode\n"
     ") s ON s.productcode = p.productcode\n"
     "WHERE p.quantityinstock < 20\n"
     "ORDER BY p.quantityinstock ASC, units_sold_last_6m DESC;"),
    ("10_avg_items_and_lines_per_order",
     "-- Average number of items and lines per order\n"
     "SELECT ROUND(AVG(order_lines)::NUMERIC,2) AS avg_lines_per_order,\n"
     "       ROUND(AVG(total_units)::NUMERIC,2) AS avg_units_per_order\n"
     "FROM (\n"
     "  SELECT o.ordernumber,\n"
     "         COUNT(od.productcode) AS order_lines,\n"
     "         SUM(od.quantityordered) AS total_units\n"
     "  FROM classicmodels.orders o\n"
     "  JOIN classicmodels.orderdetails od ON o.ordernumber = od.ordernumber\n"
     "  GROUP BY o.ordernumber\n"
     ") t;"),
]


def normalize_value(v):
    """Convert Decimal and other non-serializable types to str for printing/csv."""
    if isinstance(v, Decimal):
        return str(v)
    if v is None:
        return ""
    return v


def print_table(title, columns, rows):
    print("\n" + "=" * 80)
    print(title)
    print("-" * 80)
    if not rows:
        print("(no rows)")
        return
    headers = columns
    printable_rows = [[normalize_value(col) for col in row] for row in rows]
    if HAVE_TABULATE:
        print(tabulate(printable_rows, headers=headers, tablefmt="grid", stralign="left", numalign="right"))
    else:
        # simple fallback
        col_widths = [max(len(str(h)), max((len(str(r[i])) for r in printable_rows), default=0)) for i, h in enumerate(headers)]
        fmt = " | ".join("{:%d}" % w for w in col_widths)
        print(fmt.format(*headers))
        print("-" * (sum(col_widths) + 3 * (len(col_widths)-1)))
        for r in printable_rows:
            print(fmt.format(*r))


def save_csv(path, columns, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(columns)
        for row in rows:
            w.writerow([normalize_value(col) for col in row])


def run_all(conn, args):
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    for key, sql in QUERIES:
        print(f"\nRunning [{key}] ...")
        start = time.time()
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            elapsed = time.time() - start
            # convert RealDict rows to list of tuples to preserve column order
            columns = list(rows[0].keys()) if rows else []
            row_tuples = [tuple(r[col] for col in columns) for r in rows] if rows else []
            print(f"Query finished in {elapsed:.3f}s — {len(row_tuples)} rows")
            print_table(f"{key} — {sql.splitlines()[0]}", columns, row_tuples)
            if args.save_csv:
                fname = f"{key}.csv" if not args.csv_dir else f"{args.csv_dir.rstrip('/')}/{key}.csv"
                save_csv(fname, columns, row_tuples)
                print(f"Saved CSV -> {fname}")
        except Exception as e:
            print(f"Error running query [{key}]: {e}", file=sys.stderr)
            # don't stop: continue to next query
    cur.close()


def main():
    parser = argparse.ArgumentParser(description="Run the 10 classicmodels queries and display/save results.")
    parser.add_argument("--host", default="localhost", help="DB host (default: localhost)")
    parser.add_argument("--port", default="5432", help="DB port (default: 5432)")
    parser.add_argument("--dbname", default="postgres", help="Database name")
    parser.add_argument("--user", default=None, help="DB user")
    parser.add_argument("--password", default=None, help="DB password")
    parser.add_argument("--save-csv", dest="save_csv", action="store_true", help="Save each result to CSV files")
    parser.add_argument("--csv-dir", dest="csv_dir", default="", help="Directory to save CSVs to (default: current dir)")
    parser.add_argument("--timeout", type=int, default=60, help="Statement timeout in seconds")
    args = parser.parse_args()

    conn_info = {
        "host": args.host,
        "port": args.port,
        "dbname": args.dbname,
    }
    if args.user:
        conn_info["user"] = args.user
    if args.password:
        conn_info["password"] = args.password

    print("Connecting to PostgreSQL with:", {k: conn_info[k] for k in ("host", "port", "dbname", "user")})
    try:
        conn = psycopg2.connect(**conn_info)
        # set statement timeout (ms)
        cur = conn.cursor()
        cur.execute("SET statement_timeout = %s;", (args.timeout * 1000,))
        conn.commit()
        cur.close()

        run_all(conn, args)
        conn.close()
        print("\nAll queries completed.")
    except Exception as e:
        print("Connection or execution failed:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
