"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
from psycopg2 import sql
import csv

# Параметры подключения к базе данных
db_params = {
    "user": "postgres",
    "password": "Qaz123",
    "host": "127.0.0.1",
    "port": "5432",
    "database": "north"
}

# Подключение к базе данных
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

# Открытие файла с данными employees
with open('north_data/employees_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Пропуск заголовка, если он есть

    # Заполнение таблицы employees
    for row in reader:
        cursor.execute(sql.SQL(
            "INSERT INTO employees (employee_id, first_name, last_name, title, birth_date, notes)"
            " VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (employee_id) DO NOTHING"),
            (row[0], row[1], row[2], row[3], row[4], row[5]))

# Подтверждение изменений и закрытие соединения
connection.commit()

# открытие файла с данными customers
with open('north_data/customers_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Пропуск заголовка, если он есть

    # Заполнение таблицы customers
    for row in reader:
        cursor.execute(sql.SQL("INSERT INTO customers VALUES (%s, %s, %s) ON CONFLICT (customer_id) DO NOTHING"),
                       (row[0], row[1], row[2]))

# Подтверждение изменений и закрытие соединения
connection.commit()

# открытие файла с данными orders
with open('north_data/orders_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Пропуск заголовка, если он есть

    # Заполнение таблицы orders
    for row in reader:
        cursor.execute(sql.SQL("INSERT INTO orders VALUES (%s, %s, %s, %s, %s) ON CONFLICT (order_id) DO NOTHING"),
                       (row[0], row[1], row[2], row[3], row[4]))

# Подтверждение изменений и закрытие соединения
connection.commit()
cursor.close()
connection.close()