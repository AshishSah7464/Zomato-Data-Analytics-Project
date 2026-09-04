-- Query 1 — View all restaurants
SELECT *
FROM zomato_restaurants;

-- Query 2 — Total number of restaurants
SELECT COUNT(*) AS total_restaurants
FROM zomato_restaurants;

-- Query 3 — Average rating
SELECT 
    ROUND(AVG(rate), 2) AS average_rating
FROM
    zomato_restaurants;
    
-- Query 4 — Average cost
SELECT 
    ROUND(AVG(approx_cost), 2) AS average_cost
FROM zomato_restaurants;

-- Query 5 — Total votes
SELECT 
    SUM(votes) AS total_votes
FROM zomato_restaurants;

-- ---------------------------------------
-- Restaurant Type Analysis
-- ---------------------------------------

-- Query 6 — Number of restaurants by type
SELECT 
    restaurant_type,
    COUNT(*) AS restaurant_count
FROM zomato_restaurants
GROUP BY restaurant_type
ORDER BY restaurant_count DESC;

-- Query 7 — Average rating by restaurant type
SELECT 
    restaurant_type,
    ROUND(AVG(rate), 2) AS average_rating
FROM zomato_restaurants
GROUP BY restaurant_type
ORDER BY average_rating DESC;

-- Query 8 — Average cost by restaurant type
SELECT 
    restaurant_type,
    ROUND(AVG(approx_cost), 2) AS average_cost
FROM zomato_restaurants
GROUP BY restaurant_type
ORDER BY average_cost DESC;

-- -----------------------------------
-- Online Ordering Analysis
-- -----------------------------------

-- Query 9 — Restaurants offering online ordering
SELECT 
    online_order,
    COUNT(*) AS restaurant_count
FROM zomato_restaurants
GROUP BY online_order;

-- Query 10 — Average rating by online ordering
SELECT 
    online_order,
    ROUND(AVG(rate), 2) AS average_rating
FROM zomato_restaurants
GROUP BY online_order
ORDER BY average_rating DESC;


-- --------------------------------------------
-- Table Booking Analysis
-- --------------------------------------------

-- Query 11 — Table booking availability
SELECT 
    book_table,
    COUNT(*) AS restaurant_count
FROM zomato_restaurants
GROUP BY book_table;

-- Query 12 — Average rating by table booking
SELECT 
    book_table,
    ROUND(AVG(rate), 2) AS average_rating
FROM zomato_restaurants
GROUP BY book_table
ORDER BY average_rating DESC;

-- --------------------------------------------
-- Top Restaurants
-- --------------------------------------------

-- Query 13 — Top 10 highest-rated restaurants
SELECT 
    name,
    rate,
    votes
FROM zomato_restaurants
ORDER BY rate DESC
LIMIT 10;

-- Query 14 — Top 10 most-voted restaurants
 SELECT 
    name,
    rate,
    votes
FROM zomato_restaurants
ORDER BY votes DESC
LIMIT 10;


-- --------------------------------------------------
-- High-Rated Restaurants with Strong Engagement
-- Let's find restaurants with:
-- Rating ≥ 4.0
-- Votes ≥ 100
-- --------------------------------------------------
SELECT 
    name,
    rate,
    votes,
    approx_cost
FROM zomato_restaurants
WHERE rate >= 4.0
AND votes >= 100
ORDER BY rate DESC, votes DESC;

-- Query 15 — Top 10 most expensive restaurants
SELECT 
    name,
    approx_cost,
    rate,
    votes
FROM zomato_restaurants
ORDER BY approx_cost DESC
LIMIT 10;

-- Query 16 — Restaurants costing ₹500 or less
SELECT 
    name,
    approx_cost,
    rate,
    votes
FROM zomato_restaurants
WHERE approx_cost <= 500
ORDER BY rate DESC;

-- Highly Rated Budget Restaurants
SELECT 
    name,
    rate,
    votes,
    approx_cost
FROM zomato_restaurants
WHERE rate >= 4.0
AND approx_cost <= 500
ORDER BY rate DESC, votes DESC;

-- Find restaurant categories with at least 50 restaurants
SELECT 
    restaurant_type,
    COUNT(*) AS restaurant_count
FROM zomato_restaurants
GROUP BY restaurant_type
HAVING COUNT(*) >= 50
ORDER BY restaurant_count DESC;

-- Find restaurants costing more than the average cost
SELECT 
    name,
    approx_cost,
    rate
FROM zomato_restaurants
WHERE approx_cost > (
    SELECT AVG(approx_cost)
    FROM zomato_restaurants
)
ORDER BY rate DESC;