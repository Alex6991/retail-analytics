-- =====================================================
-- SQL-запросы для Retail Analytics
-- =====================================================

-- 1. Общая статистика
SELECT COUNT(*) as total_orders,
       ROUND(SUM(sales), 2) as total_sales,
       ROUND(SUM(profit), 2) as total_profit
FROM orders;

-- 2. Продажи по годам
SELECT year,
       ROUND(SUM(sales), 2) as total_sales,
       ROUND(SUM(profit), 2) as total_profit,
       COUNT(*) as orders_count
FROM orders
GROUP BY year
ORDER BY year;

-- 3. Топ-10 больших заказов
SELECT order_id, customer_name, category, product_name, sales
FROM orders
WHERE sales > 1000
ORDER BY sales DESC
LIMIT 10;

-- 4. Топ-3 товара в каждой категории (оконная функция)
SELECT category, product_name, sales, rank_in_category
FROM (
    SELECT category,
           product_name,
           ROUND(SUM(sales), 2) as sales,
           RANK() OVER (PARTITION BY category ORDER BY SUM(sales) DESC) as rank_in_category
    FROM orders
    GROUP BY category, product_name
)
WHERE rank_in_category <= 3
ORDER BY category, rank_in_category;

-- 5. Накопительный итог продаж по годам
SELECT year,
       ROUND(SUM(sales), 2) as yearly_sales,
       ROUND(SUM(SUM(sales)) OVER (ORDER BY year), 2) as cumulative_sales
FROM orders
GROUP BY year
ORDER BY year;

-- 6. Выполнение целей по годам (JOIN)
SELECT o.year,
       ROUND(SUM(o.sales), 2) as actual_sales,
       t.target_sales,
       ROUND(SUM(o.sales) - t.target_sales, 2) as difference,
       ROUND(SUM(o.sales) * 100.0 / t.target_sales, 2) as percent_of_target
FROM orders o
JOIN targets t ON o.year = t.year
GROUP BY o.year, t.target_sales
ORDER BY o.year;