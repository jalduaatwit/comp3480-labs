-- Products with a discount over 25%
SELECT product_name, discount_percent 
FROM products 
WHERE discount_percent > 25;
