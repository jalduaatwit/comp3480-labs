-- Most expensive product per category
SELECT c.category_name, MAX(p.list_price) AS max_price
FROM products p
INNER JOIN categories c 
ON p.category_id = c.category_id
GROUP BY c.category_name;
