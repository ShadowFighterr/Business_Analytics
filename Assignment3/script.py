# data_inserter.py
import psycopg2
import time
import random
from datetime import date, timedelta

# --- ШАГ 1: Импорт строки подключения из файла config.py ---
# Это позволяет нам не хранить пароли и другие секретные данные прямо в коде.
try:
    from config import DATABASE_URI
except ImportError:
    print("❌ Ошибка: Не удалось найти файл config.py или переменную DATABASE_URI.")
    print("Пожалуйста, убедитесь, что файл config.py находится в той же папке и содержит: DATABASE_URI = '...'")
    exit()

def add_new_order():
    """
    Основная функция для добавления нового заказа, его деталей и платежа.
    """
    conn = None
    try:
        # --- ШАГ 2: Подключение к базе данных с использованием URI ---
        # psycopg2 может работать с URI, но ему не нравится часть "+psycopg2",
        # которая используется в SQLAlchemy. Мы ее просто убираем.
        db_uri = DATABASE_URI.replace('postgresql+psycopg2', 'postgresql')
        
        print("Подключение к базе данных...")
        conn = psycopg2.connect(db_uri)
        cur = conn.cursor()

        # --- Получаем существующие данные, чтобы не нарушить внешние ключи (FK) ---
        cur.execute("SELECT customerNumber FROM classicmodels.customers;")
        customer_numbers = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT productCode FROM classicmodels.products;")
        product_codes = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT MAX(orderNumber) FROM classicmodels.orders;")
        new_order_number = cur.fetchone()[0] + 1

        # --- Генерируем данные для нового заказа (таблица orders) ---
        random_customer = random.choice(customer_numbers)
        order_date = date.today()
        required_date = order_date + timedelta(days=random.randint(7, 21))
        order_status = random.choice(['In Process', 'On Hold', 'Shipped']) # Добавим немного разнообразия в статусы

        # --- Вставляем новый заказ в таблицу `orders` ---
        order_query = """
        INSERT INTO classicmodels.orders (orderNumber, orderDate, requiredDate, status, customerNumber)
        VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(order_query, (new_order_number, order_date, required_date, order_status, random_customer))
        print(f"✅ Создан новый заказ #{new_order_number} для клиента #{random_customer} со статусом '{order_status}'.")

        # --- Генерируем и вставляем детали заказа в `orderdetails` ---
        total_order_amount = 0
        products_in_order = random.sample(product_codes, k=random.randint(1, 4)) # Уникальные товары в заказе
        
        for i, product_code in enumerate(products_in_order):
            quantity_ordered = random.randint(10, 50)
            price_each = round(random.uniform(20.0, 250.0), 2)
            order_line_number = i + 1
            total_order_amount += quantity_ordered * price_each

            details_query = """
            INSERT INTO classicmodels.orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
            VALUES (%s, %s, %s, %s, %s);
            """
            cur.execute(details_query, (new_order_number, product_code, quantity_ordered, price_each, order_line_number))
            print(f"   - Добавлен товар {product_code} (x{quantity_ordered}) в заказ.")

        # --- Генерируем и вставляем платеж в `payments` ---
        check_number = f"PY{random.randint(100000, 999999)}"
        payment_date = order_date + timedelta(days=random.randint(0, 3))
        # Сделаем сумму платежа более реалистичной - часть от суммы заказа
        amount = round(total_order_amount * random.uniform(0.8, 1.1), 2) 

        payment_query = """
        INSERT INTO classicmodels.payments (customerNumber, checkNumber, paymentDate, amount)
        VALUES (%s, %s, %s, %s);
        """
        cur.execute(payment_query, (random_customer, check_number, payment_date, amount))
        print(f"✅ Добавлен платеж {check_number} на сумму ${amount:.2f} от клиента #{random_customer}.")

        # --- Фиксируем все изменения в базе данных ---
        conn.commit()
        print("--- Все изменения успешно сохранены. ---")

        cur.close()

    except (Exception, psycopg2.Error) as error:
        print(f"❌ Ошибка при работе с PostgreSQL: {error}")
        if conn:
            conn.rollback() # Откатываем изменения в случае ошибки

    finally:
        if conn is not None:
            conn.close()
            print("Соединение с базой данных закрыто.\n")


if __name__ == '__main__':
    print("🚀 Скрипт для автоматического добавления данных запущен.")
    print("Нажмите Ctrl+C для остановки.")
    while True:
        add_new_order()
        sleep_time = random.uniform(5, 20)
        print(f"⏳ Следующее обновление через {sleep_time:.2f} секунд...")
        time.sleep(sleep_time)
