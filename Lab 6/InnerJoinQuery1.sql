-- List products with their category name
SELECT p.product_name, c.category_name
FROM products p
INNER JOIN categories c 
ON p.category_id = c.category_id;
