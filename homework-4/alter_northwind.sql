-- Подключиться к БД Northwind и сделать следующие изменения:
-- 1. Добавить ограничение на поле unit_price таблицы products (цена должна быть больше 0)

ALTER TABLE products
ADD CONSTRAINT chk_products_unit_price CHECK (unit_price > 0)

-- 2. Добавить ограничение, что поле discontinued таблицы products может содержать только значения 0 или 1

ALTER TABLE products
ADD CONSTRAINT chk_products_discontinued CHECK (discontinued IN (0, 1))

-- 3. Создать новую таблицу, содержащую все продукты, снятые с продажи (discontinued = 1)

SELECT *
FROM products
WHERE discontinued = 1;

-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)
-- Для 4-го пункта может потребоваться удаление ограничения, связанного с foreign_key. Подумайте, как это можно решить, чтобы связь с таблицей order_details все же осталась.

-- Шаг 1: Удаляем связанные строки из order_details
DELETE FROM order_details WHERE product_id IN (SELECT product_id FROM products WHERE discontinued = 1);

-- Шаг 2: Удаляем из основной таблицы продукты, снятые с продажи

DELETE FROM products WHERE discontinued = 1;

CREATE TEMPORARY TABLE temp_products AS
SELECT *
FROM products
WHERE discontinued = 0;

-- Вставляем данные из временной таблицы в основную таблицу, игнорируя конфликты по ключу

INSERT INTO products SELECT * FROM temp_products
ON CONFLICT (product_id) DO NOTHING;

-- Удаляем временную таблицу

DROP TABLE IF EXISTS temp_products;