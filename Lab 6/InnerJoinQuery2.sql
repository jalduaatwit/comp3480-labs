-- List customers and their order
SELECT o.order_id, o.order_date, c.first_name, c.last_name
FROM orders o
INNER JOIN customers c 
ON o.customer_id = c.customer_id;
