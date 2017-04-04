/*
 * Query 1  - COMPLETE
 *
 * Explore the data in order to get “a feel of” the prices of the various products in a
 * country. The user should be able to drill down from 1 year, to one month, to a
 * specific day, and roll up again.
 *
 * Line graph, each line being an individual product within the specified country, city or location
 * X axis: Date (by month)
 * Y axis: Price
 */

-- Year drilldown
SELECT  d.year, p.name, avg(pp.price)
FROM product_price pp
  INNER JOIN location l
    ON pp.location = l.id
  INNER JOIN date d
    ON d.id = pp.date
  INNER JOIN  product p
    ON p.id = pp.product
WHERE l.country='India'
GROUP BY d.year, p.name;

-- Month drilldown
SELECT  d.month, p.name, avg(pp.price)
FROM product_price pp
  INNER JOIN location l
    ON pp.location = l.id
  INNER JOIN date d
    ON d.id = pp.date
  INNER JOIN  product p
    ON p.id = pp.product
WHERE l.country='India'
GROUP BY d.month, p.name;

-- Day drilldown
SELECT  d.day, p.name, avg(pp.price)
FROM product_price pp
  INNER JOIN location l
    ON pp.location = l.id
  INNER JOIN date d
    ON d.id = pp.date
  INNER JOIN  product p
    ON p.id = pp.product
WHERE l.country='India'
GROUP BY d.day, p.name;

/*
 * Query 2 - COMPLETE
 *
 * Explore the data in order to get “a feel of” the price differences of the products when
 * considering more than one country. For example, one may want to contrast the price
 * of tuna steaks in Kenya with that in India. The user should be able to drill down
 * from 6 months, to one month, to a specific day, and roll up again.
 */

-- Year drilldown
SELECT l.country, avg(pp.price), d.year
FROM product_price pp
  INNER JOIN location l
    ON pp.location = l.id
  INNER JOIN date d
    ON d.id = pp.date
  INNER JOIN  product p
    ON p.id = pp.product
WHERE p.name='Tuna steaks'
GROUP BY l.country, d.year;

-- month drilldown
SELECT l.country, avg(pp.price), d.month
FROM product_price pp
  INNER JOIN location l
    ON pp.location = l.id
  INNER JOIN date d
    ON d.id = pp.date
  INNER JOIN  product p
    ON p.id = pp.product
WHERE p.name='Tuna steaks'
GROUP BY l.country, d.month;

-- day drilldown
SELECT l.country, avg(pp.price), d.day
FROM product_price pp
  INNER JOIN location l
    ON pp.location = l.id
  INNER JOIN date d
    ON d.id = pp.date
  INNER JOIN  product p
    ON p.id = pp.product
WHERE p.name='Tuna steaks'
GROUP BY l.country, d.day;

/*
 * Query 3  - COMPLETE
 *
 * Explore the data by considering the prices of categories of products. That is, we wish
 * to roll up from product to category. For example, the sales of apples, bananas and
 * oranges are grouped into fruits while minced beef and chicken legs are grouped into
 * fresh meat.
 *
 * Bar graph
 * X axis: category
 * Y axis: price
 */

SELECT p.category, avg(price)
FROM product_price pp
  INNER JOIN location l
    ON pp.location = l.id
  INNER JOIN date d
    ON d.id = pp.date
  INNER JOIN  product p
    ON p.id = pp.product
GROUP BY p.category;

/*
 * Query 4  - COMPLETE
 *
 * Explore the data by considering the prices of categories of products, on a specific day
 * of the week (e.g. the prices of fruits on Monday versus Saturday; weekend versus
 * weekday, and so on).
 *
 * Bar graph
 * X axis: day
 * Y axis: price
 */

SELECT d.day, p.category, AVG(pp.price)
FROM product_price pp
  INNER JOIN date d
    ON d.id = pp.date
  INNER JOIN  product p
    ON p.id = pp.product
GROUP BY d.day, p.name
ORDER BY p.name DESC;

/*
 * Query 5  - COMPLETE
 *
 * Explore the fluctuations in individual product prices, per country, per city and per location.
 *
 * Line graph, each line being an individual item within the specified country, city or location
 * X axis: Date (by month)
 * Y axis: Price
 */


-- Per country
SELECT l.country, p.name, AVG(pp.price), d.date
FROM product_price pp
  INNER JOIN location l
    ON pp.location = l.id
  INNER JOIN date d
    ON d.id = pp.date
  INNER JOIN  product p
    ON p.id = pp.product
where p.name = 'Apple' -- we chose to look at apples, but it could have been any food
GROUP BY l.country, p.name, d.date;

-- Per city, per location
SELECT l.city, p.name, AVG(pp.price), d.date
FROM product_price pp
  INNER JOIN location l
    ON pp.location = l.id
  INNER JOIN date d
    ON d.id = pp.date
  INNER JOIN  product p
    ON p.id = pp.product
where p.name = 'Apple' -- we chose to look at apples, but it could have been any food
GROUP BY l.city, p.name, d.date;

/*
 * Query 6  - COMPLETE
 *
 * Explore the prices of a specific product (e.g. apples) in terms of socio-economic
 * factors, such as the average income of a country.
 *
 * Not sure how to represent in dashboard...
 */

SELECT p.name, AVG(pp.price), l.country, l.avg_annual_income, l.life_expectancy, l.population
FROM product_price pp
  INNER JOIN location l
    ON pp.location = l.id
  INNER JOIN  product p
    ON p.id = pp.product
where p.name='Apple'
GROUP BY p.name, l.country, l.avg_annual_income, l.life_expectancy, l.population;

/*
 * Query 7 -- TODO: not working, takes forever?
 *
 * Compare the prices of two complementary products (e.g. white rice and long-grain rice).
 *
 * Line graph, 2 lines, 1 for each product
 * X axis: Date (by month)
 * Y axis: Price
 */

SELECT p.name, AVG(pp.price), p2.name, AVG(pp.price)
FROM product_price pp
  CROSS JOIN product_price pp2
  INNER JOIN  product p
    ON p.id = pp.product
  INNER JOIN  product p2
    ON p2.id = pp2.product
WHERE
  p.id != p2.id
GROUP BY p.name, p2.name;

/*
 * Query 8
 *
 * Compare the prices of two complementary products (e.g. white rice and long-grain rice),
 * within a specific country. Next, drill down by city and location.
 */