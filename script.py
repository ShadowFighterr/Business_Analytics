import random
import decimal
import datetime
import psycopg2
from faker import Faker
import traceback

# --- CONFIG ---
DB = {"host":"localhost", "port":5432, "dbname":"postgres", "user":"postgres", "password":"Azamat06"}
NUM_PRODUCTLINES = 6
NUM_OFFICES = 6
NUM_EMPLOYEES = 30
NUM_PRODUCTS = 120
NUM_CUSTOMERS = 150
NUM_ORDERS = 400
# ----------------

fake = Faker()

# column length constants taken from your CREATE TABLEs
MAX = {
    "customername": 50,
    "contactlastname": 50,
    "contactfirstname": 50,
    "phone": 50,
    "addressline1": 50,
    "addressline2": 50,
    "city": 50,
    "state": 50,
    "postalcode": 15,
    "country": 50,
    "extension": 10,
    "email": 100,
    "officecode": 10,
    "jobtitle": 50,
    "productcode": 15,
    "productname": 70,
    "productline": 50,
    "productscale": 10,
    "productvendor": 50,
    "territory": 10,
    "checknumber": 50,
}

def safe_str(val, col_name):
    """Convert to str and truncate to column limit. Return None if val is None."""
    if val is None:
        return None
    s = str(val)
    m = MAX.get(col_name)
    if m is None:
        return s  # no limit known
    if len(s) > m:
        # log truncation (could be noisy) - you can change to saving to a file
        print(f"[TRUNCATE] {col_name}: {len(s)} -> {m} chars. Original start: {s[:40]!r}")
        return s[:m]
    return s

def safe_smallint(n):
    """Ensure value fits in SQL smallint (-32768..32767). We use non-negative domain here."""
    if n is None:
        return None
    return max(0, min(32767, int(n)))

def connect():
    d = DB
    conn = psycopg2.connect(host=d["host"], port=d["port"], dbname=d["dbname"],
                            user=d["user"], password=d["password"])
    conn.autocommit = False
    return conn

def insert_productlines(cur):
    lines = [
        ("Motorcycles","Two-wheeled motor vehicles"),
        ("Classic Cars","Classic and antique cars"),
        ("Trucks and Buses","Heavier vehicles"),
        ("Vintage Cars","Collectible old models"),
        ("Planes","Model aircraft"),
        ("Ships","Model ships"),
    ]
    for pl, desc in lines[:NUM_PRODUCTLINES]:
        cur.execute("""
            INSERT INTO productlines (productline, textdescription)
            VALUES (%s, %s)
            ON CONFLICT (productline) DO NOTHING
        """, (safe_str(pl, "productline"), desc))
    return [pl for pl,_ in lines[:NUM_PRODUCTLINES]]

def insert_offices(cur):
    offices = []
    for i in range(1, NUM_OFFICES+1):
        code = safe_str(str(100 + i), "officecode")
        city = safe_str(fake.city(), "city")
        phone = safe_str(fake.phone_number(), "phone")
        addr = safe_str(fake.street_address(), "addressline1")
        country = safe_str(fake.country(), "country")
        postal = safe_str(fake.postcode(), "postalcode")
        territory = safe_str(fake.bothify(text='T??')[:MAX["territory"]], "territory")
        cur.execute("""
            INSERT INTO offices (officecode, city, phone, addressline1, country, postalcode, territory)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (officecode) DO NOTHING
        """, (code, city, phone, addr, country, postal, territory))
        offices.append(code)
    return offices

def insert_employees(cur, office_codes):
    employees = []
    for i in range(1, NUM_EMPLOYEES+1):
        emp_no = 1000 + i
        first = safe_str(fake.first_name(), "firstname")
        last = safe_str(fake.last_name(), "lastname")
        ext = safe_str(f"x{random.randint(100,999)}", "extension")
        email = safe_str(f"{first.lower()}.{last.lower()}@example.com", "email")
        office = random.choice(office_codes)
        job = safe_str(random.choice(["Sales Rep", "Manager", "VP", "Engineer", "Clerk"]), "jobtitle")
        reports_to = None
        if i > 5:
            reports_to = 1001 + random.randint(0, min(4, NUM_EMPLOYEES-1))
        cur.execute("""
            INSERT INTO employees (employeenumber, lastname, firstname, extension, email, officecode, reportsto, jobtitle)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (employeenumber) DO NOTHING
        """, (emp_no, last, first, ext, email, office, reports_to, job))
        employees.append(emp_no)
    return employees

def insert_products(cur, productlines):
    product_codes = []
    vendors = ["Min Lin Diecast", "Highway 66", "AutoArt Studio", "ClassicVendor", "VendorCo"]
    for i in range(1, NUM_PRODUCTS+1):
        code = safe_str(f"P{2000+i}", "productcode")
        name = safe_str((fake.word().capitalize() + " " + random.choice(["Model","Replica","Series","Edition"])) , "productname")
        line = safe_str(random.choice(productlines), "productline")
        scale = safe_str(random.choice(["1:10","1:12","1:18","1:24"]), "productscale")
        vendor = safe_str(random.choice(vendors), "productvendor")
        desc = fake.sentence(nb_words=12)
        qty = safe_smallint(random.randint(0,1000))
        buy = round(decimal.Decimal(random.uniform(10,500)),2)
        msrp = round(buy * decimal.Decimal(random.uniform(1.1,2.5)), 2)
        cur.execute("""
            INSERT INTO products (productcode, productname, productline, productscale, productvendor, productdescription, quantityinstock, buyprice, msrp)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (productcode) DO NOTHING
        """, (code, name, line, scale, vendor, desc, qty, buy, msrp))
        product_codes.append((code, float(msrp)))
    return product_codes

def insert_customers(cur, employees):
    customers = []
    for i in range(1, NUM_CUSTOMERS+1):
        cust_no = 3000 + i
        name = safe_str(fake.company(), "customername")
        contact_last = safe_str(fake.last_name(), "contactlastname")
        contact_first = safe_str(fake.first_name(), "contactfirstname")
        phone = safe_str(fake.phone_number(), "phone")
        addr = safe_str(fake.street_address(), "addressline1")
        city = safe_str(fake.city(), "city")
        country = safe_str(fake.country(), "country")
        sales_rep = random.choice(employees + [None]*5)
        credit = round(decimal.Decimal(random.uniform(1000,50000)),2)
        cur.execute("""
            INSERT INTO customers (customernumber, customername, contactlastname, contactfirstname, phone, addressline1, city, country, salesrepemployeenumber, creditlimit)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (customernumber) DO NOTHING
        """, (cust_no, name, contact_last, contact_first, phone, addr, city, country, sales_rep, credit))
        customers.append(cust_no)
    return customers

def insert_orders_and_details(cur, customers, products):
    orders = []
    order_id = 5000
    for i in range(NUM_ORDERS):
        order_id += 1
        cust = random.choice(customers)
        order_date = fake.date_between(start_date='-2y', end_date='today')
        req_date = order_date + datetime.timedelta(days=random.randint(7,30))
        ship_date = order_date + datetime.timedelta(days=random.randint(1,10)) if random.random() < 0.9 else None
        status = safe_str(random.choice(["Shipped","Resolved","In Process","On Hold"]), "status")
        cur.execute("""
            INSERT INTO orders (ordernumber, orderdate, requireddate, shippeddate, status, comments, customernumber)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (ordernumber) DO NOTHING
        """, (order_id, order_date, req_date, ship_date, status, None, cust))
        # orderdetails: 1..5 lines
        lines = random.randint(1,5)
        line_no = 1
        for _ in range(lines):
            product, msrp = random.choice(products)
            qty = int(random.randint(1,50))
            price_each = round(random.uniform(max(0.01, msrp*0.7), msrp),2)
            cur.execute("""
                INSERT INTO orderdetails (ordernumber, productcode, quantityordered, priceeach, orderlinenumber)
                VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
            """, (order_id, safe_str(product, "productcode"), qty, price_each, line_no))
            line_no += 1
        orders.append(order_id)
    return orders

def insert_payments(cur, customers):
    for c in customers:
        for _ in range(random.randint(0,3)):
            check = safe_str(f"CHK{random.randint(100000,999999)}", "checknumber")
            pay_date = fake.date_between(start_date='-2y', end_date='today')
            amount = round(decimal.Decimal(random.uniform(50, 20000)),2)
            try:
                cur.execute("""
                    INSERT INTO payments (customernumber, checknumber, paymentdate, amount)
                    VALUES (%s,%s,%s,%s)
                    ON CONFLICT DO NOTHING
                """, (c, check, pay_date, amount))
            except Exception as e:
                # log but continue
                print(f"[PAYMENT ERROR] cust {c} check {check}: {e}")

def main():
    conn = connect()
    cur = conn.cursor()
    try:
        productlines = insert_productlines(cur)
        offices = insert_offices(cur)
        employees = insert_employees(cur, offices)
        products = insert_products(cur, productlines)
        customers = insert_customers(cur, employees)
        orders = insert_orders_and_details(cur, customers, products)
        insert_payments(cur, customers)
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()
