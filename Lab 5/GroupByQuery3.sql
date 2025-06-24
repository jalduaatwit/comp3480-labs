-- Total number of orders per customer
SELECT c.first_name, c.last_name, COUNT(o.order_id) AS order_count
FROM customers c
INNER JOIN orders o 
ON c.customer_id = o.customer_id
GROUP BY c.customer_id;
