-- Total order value per order
SELECT o.order_id, SUM(oi.item_price * oi.quantity - oi.discount_amount) AS total_order_value
FROM orders o
INNER JOIN order_items oi 
ON o.order_id = oi.order_id
GROUP BY o.order_id;
