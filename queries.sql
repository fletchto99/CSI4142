/*
 * Query 1
 *
 * Explore the data in order to get “a feel of” the prices of the various products in a
 * country. The user should be able to drill down from 6 months, to one month, to a
 * specific day, and roll up again.
 */

SELECT  l.country, pp.price, p.name, d.year, d.month, d.day
FROM product_price pp
  INNER JOIN location l on pp.location = l.id
  INNER JOIN date d on d.id = pp.date
  INNER JOIN  product p on p.id = pp.product
GROUP BY l.country, p.name, pp.price, d.year, d.month, d.day;

/*
 * Query 2
 *
 * Explore the data in order to get “a feel of” the price differences of the products when
 * considering more than one country. For example, one may want to contrast the price
 * of tuna steaks in Kenya with that in India. The user should be able to drill down
 * from 6 months, to one month, to a specific day, and roll up again.
 */

SELECT price
FROM product_price pp
  INNER JOIN date d on pp.date=date.id
WHERE

/*
 * Query 3
 *
 * Explore the data by considering the prices of categories of products. That is, we wish
 * to roll up from product to category. For example, the sales of apples, bananas and
 * oranges are grouped into fruits while minced beef and chicken legs are grouped into
 * fresh meat.
 */

SELECT p.category, avg(price), d.year, d.month, d.day
FROM product_price pp
  INNER JOIN location l on pp.location = l.id
  INNER JOIN date d on d.id = pp.date
  INNER JOIN  product p on p.id = pp.product
group by p.category

/*
 * Query 4
 *
 * Explore the data by considering the prices of categories of products, on a specific day
 * of the week (e.g. the prices of fruits on Monday versus Saturday; weekend versus
 * weekday, and so on).
 */

/*
 * Query 5
 *
 * Explore the fluctuations in individual product prices, per country, per city and per location.
 */

/*
 * Query 6
 *
 * Explore the prices of a specific product (e.g. apples) in terms of socio-economic
 * factors, such as the average income of a country.
 */

SELECT pp.price, l.avg_annual_income, l.life_expectancy, l.population
FROM product_price pp
  INNER JOIN location l on pp.location = l.id
  INNER JOIN date d on d.id = pp.date
  INNER JOIN  product p on p.id = pp.product
group by l.country, d.year, d.month, d.day, pp.price, l.avg_annual_income, l.life_expectancy, l.population

/*
 * Query 7
 *
 * Compare the prices of two complementary products (e.g. white rice and long-grain rice).
 */

/*
 * Query 8
 *
 * Compare the prices of two complementary products (e.g. white rice and long-grain rice),
 * within a specific country. Next, drill down by city and location.
 */