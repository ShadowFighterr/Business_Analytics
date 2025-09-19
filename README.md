# 📊 Business Analytics

### A Comprehensive Sales & Order Management Database

🔗 [Dataset on Kaggle](https://www.kaggle.com/datasets/himelsarder/business-database)

This project provides a **relational database schema** for a sales and order management system.
It tracks **customers, employees, products, orders, and payments**, enabling advanced business analytics and reporting.

---

## 🚀 Stage 1 — Dataset Preprocessing

### 🔄 MySQL → PostgreSQL Migration (pgAdmin)

I used **pgloader** to migrate the dataset from MySQL to PostgreSQL.

```bash
pgloader mysql://user:password@host/source_db \
         postgresql://pguser:pgpass@host/target_db
```

👉 This command automatically converts MySQL schema and data into PostgreSQL format.

---

## 🗂️ Dataset Completion

Since the dataset wasn’t large enough for further research, I created a **Python script (`script.py`)** to generate additional synthetic data and enrich the database.

---

## ✅ Verifying the Database

You can check the row counts in all tables by running:

```sql
SELECT 'customers' AS table_name, count(*) FROM customers
UNION ALL
SELECT 'employees' AS table_name, count(*) FROM employees
UNION ALL
SELECT 'offices' AS table_name, count(*) FROM offices
UNION ALL
SELECT 'orderdetails' AS table_name, count(*) FROM orderdetails
UNION ALL
SELECT 'orders' AS table_name, count(*) FROM orders
UNION ALL
SELECT 'payments' AS table_name, count(*) FROM payments
UNION ALL
SELECT 'productlines' AS table_name, count(*) FROM productlines
UNION ALL
SELECT 'products' AS table_name, count(*) FROM products;
```

---

## 📸 Database Example

<img width="1045" height="761" alt="database preview" src="https://github.com/user-attachments/assets/2e52e001-968d-4664-a371-76260de9436b" />

---

## 📌 Tech Stack

* **Database:** PostgreSQL (migrated from MySQL)
* **Migration Tool:** pgloader
* **Data Completion:** Python (script.py)
* **Management:** pgAdmin

````markdown
# 10 Analytical Topics

The main.py script runs a set of **10 analytical SQL queries** against a PostgreSQL database 
containing the schema on the image above. It connects to the database, executes each query, 
prints the results in a readable CLI table, and (optionally) saves them to CSV files.

## Features

- Runs **10 pre-defined queries**:
  1. Total revenue by customer country  
  2. Top 10 products by revenue  
  3. Monthly sales trend (last 12 months)  
  4. Average order value per customer  
  5. Orders by year and status  
  6. Sales representative performance  
  7. Average delivery time for shipped orders  
  8. Payment coverage ratio per customer  
  9. Low-stock products with sales in the last 6 months  
  10. Average items and lines per order  

- Pretty CLI output (via [`tabulate`](https://pypi.org/project/tabulate/)), with fallback to plain text  
- Optionally export results as `.csv` files  
- Configurable connection settings (host, port, dbname, user, password)  
- Safe execution with per-query error handling  

## Requirements

- Python 3.8+
- Connection with PostgreSQL database   
- Python libraries:
  ```bash
  pip install psycopg2-binary tabulate
````

## Usage

```bash
python main.py \
  --host localhost \
  --port 5432 \
  --dbname mydb \
  --user myuser \
  --password mypass
```

Optional flags:

* `--save-csv` → Save each query’s output to a CSV file
* `--csv-dir ./results` → Directory for CSV exports (default: current directory)
* `--timeout 60` → Statement timeout in seconds (default: 60)

Example:

```bash
python main.py --host localhost --dbname classicmodels --user postgres --password secret --save-csv --csv-dir ./out
```

This will run all queries, display results in the terminal, and save them to `./out/`.

---

## Notes

* If `tabulate` is not installed, output falls back to a simpler table format.
* The script continues even if some queries fail (so you still get partial results).
* Output files are named after the query (e.g., `1_total_revenue_by_country.csv`).

---


---

✨ *This repository sets up the foundation for further analytics, machine learning, and BI exploration.*

---


