CREATE DATABASE zomato_analysis;

USE zomato_analysis;

CREATE TABLE zomato_restaurants (
    name VARCHAR(255),
    online_order VARCHAR(10),
    book_table VARCHAR(10),
    rate DECIMAL(3,1),
    votes INT,
    approx_cost INT,
    restaurant_type VARCHAR(100)
);


DESCRIBE zomato_restaurants;

SELECT COUNT(*) 
FROM zomato_restaurants;