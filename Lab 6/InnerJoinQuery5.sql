-- Customer's addresses
SELECT a.address_id, a.line1, c.first_name, c.last_name
FROM addresses a
INNER JOIN customers c
ON a.customer_id = c.customer_id;
