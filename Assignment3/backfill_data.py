# backfill_data.py
import psycopg2
import random
from datetime import date, timedelta
import time

# --- Импортируем строку подключения из файла config.py ---
try:
    from config import DATABASE_URI
except ImportError:
    print("❌ Ошибка: Не удалось найти файл config.py или переменную DATABASE_URI.")
    exit()

# --- НАСТРОЙКИ ГЕНЕРАЦИИ ---
START_YEAR = 2006
END_YEAR = 2024 # Мы заполним данные до конца прошлого года

def backfill_historical_data():
    """
    Одноразовый скрипт для генерации исторических данных и заполнения пробелов.
    """
    conn = None
    try:
        db_uri = DATABASE_URI.replace('postgresql+psycopg2', 'postgresql')
        print("Подключение к базе данных...")
        conn = psycopg2.connect(db_uri)
        cur = conn.cursor()

        # --- Получаем начальные данные для генерации ---
        cur.execute("SELECT customerNumber FROM classicmodels.customers;")
        customer_numbers = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT productCode FROM classicmodels.products;")
        product_codes = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT MAX(orderNumber) FROM classicmodels.orders;")
        current_order_number = cur.fetchone()[0]

        print(f"🚀 Начинаем генерацию данных с {START_YEAR} по {END_YEAR} год...")

        # --- Основной цикл по годам и месяцам ---
        for year in range(START_YEAR, END_YEAR + 1):
            for month in range(1, 13):
                # Генерируем случайное количество заказов в этом месяце (например, от 5 до 20)
                orders_this_month = random.randint(5, 20)
                
                print(f"   -> Генерируем {orders_this_month} заказов для {year}-{month:02d}...")

                for _ in range(orders_this_month):
                    current_order_number += 1
                    
                    # Генерируем случайный день в месяце
                    day = random.randint(1, 28) # Используем 28, чтобы избежать проблем с февралем
                    order_date = date(year, month, day)
                    required_date = order_date + timedelta(days=random.randint(7, 21))
                    random_customer = random.choice(customer_numbers)
                    status = 'Shipped' # Все исторические заказы считаем выполненными

                    # 1. Вставляем заказ
                    order_query = "INSERT INTO classicmodels.orders (orderNumber, orderDate, requiredDate, status, customerNumber) VALUES (%s, %s, %s, %s, %s);"
                    cur.execute(order_query, (current_order_number, order_date, required_date, status, random_customer))

                    # 2. Вставляем детали заказа
                    products_in_order = random.sample(product_codes, k=random.randint(1, 4))
                    total_order_amount = 0
                    for i, product_code in enumerate(products_in_order):
                        quantity = random.randint(10, 50)
                        price = round(random.uniform(20.0, 250.0), 2)
                        total_order_amount += quantity * price
                        details_query = "INSERT INTO classicmodels.orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber) VALUES (%s, %s, %s, %s, %s);"
                        cur.execute(details_query, (current_order_number, product_code, quantity, price, i + 1))
                    
                    # 3. Вставляем платеж
                    check_number = f"BKF{random.randint(100000, 999999)}"
                    amount = round(total_order_amount * random.uniform(0.9, 1.0), 2)
                    payment_query = "INSERT INTO classicmodels.payments (customerNumber, checkNumber, paymentDate, amount) VALUES (%s, %s, %s, %s);"
                    cur.execute(payment_query, (random_customer, check_number, order_date, amount))

            # Сохраняем изменения в БД после каждого года, чтобы не перегружать транзакцию
            conn.commit()
            print(f"✅ Данные за {year} год успешно сгенерированы и сохранены.")

        print("\n🎉 Все исторические данные успешно добавлены!")

    except (Exception, psycopg2.Error) as error:
        print(f"❌ Ошибка: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print("Соединение с базой данных закрыто.")


if __name__ == '__main__':
    backfill_historical_data()
