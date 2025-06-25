-- Customers per state
SELECT state, COUNT(*) AS num_customers
FROM addresses
GROUP BY state;
