-- Average discount by category
SELECT c.category_name, AVG(p.discount_percent) AS avg_discount
FROM products p
INNER JOIN categories c 
ON p.category_id = c.category_id
GROUP BY c.category_name;
