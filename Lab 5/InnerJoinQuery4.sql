-- Shipping address for each order
SELECT o.order_id, a.line1, a.city, a.state
FROM orders o
INNER JOIN addresses a 
ON o.ship_address_id = a.address_id;
