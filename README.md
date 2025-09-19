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
### 🔒 Environment Variables

Before running the script, set the following environment variables for database connection:

```bash
export DB_HOST=localhost        # Database host (default: localhost)
export DB_PORT=5432            # Database port (default: 5432)
export DB_NAME=postgres        # Database name (default: postgres)
export DB_USER=postgres        # Database user (default: postgres)
export DB_PASSWORD=your_password_here  # Database password (required)
```

### 🚀 Running the Script

```bash
# Set your database password
export DB_PASSWORD=your_actual_password

# Run the data generation script
python3 script.py
```

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

---

✨ *This repository sets up the foundation for further analytics, machine learning, and BI exploration.*

---
