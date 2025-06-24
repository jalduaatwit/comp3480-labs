-- Order with Product Names
SELECT oi.order_id, p.product_name, oi.quantity
FROM order_items oi
INNER JOIN products p 
ON oi.product_id = p.product_id;
