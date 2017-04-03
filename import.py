#!/usr/bin/env python3

import psycopg2
import csv
from collections import defaultdict

dbconfig = {
    'dbname': 'postgres',
    'user': 'postgres'
}

conn = psycopg2.connect(**dbconfig)
cur = conn.cursor()

dates = defaultdict(dict)
products = defaultdict(dict)
locations = defaultdict(dict)
product_prices = defaultdict(dict)

avg_annual_income = defaultdict(dict)
gdp = defaultdict(dict)
life_expectancy = defaultdict(dict)
population = defaultdict(dict)

with open('datasets/food-prices.csv') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    head = dict(reversed(field) for field in enumerate(next(reader)))

    for row in reader:
        date = dates[row[head['Obs Date (yyyy-MM-dd)']]]
        date['date'] = row[head['Obs Date (yyyy-MM-dd)']]

        product = products[row[head['Product Code']]]
        product['id'] = row[head['Product Code']]
        product['name'] = row[head['Product Name']]

        location = locations[row[head['Location Code']]]
        location['id'] = row[head['Location Code']]
        location['name'] = row[head['Location Name']]
        location['country'] = row[head['Country']]

        price = product_prices[(
            row[head['Obs Date (yyyy-MM-dd)']],
            row[head['Product Code']],
            row[head['Location Code']]
        )]

        price['date'] = row[head['Obs Date (yyyy-MM-dd)']];
        price['product'] = row[head['Product Code']];
        price['location'] = row[head['Location Code']];
        price['price'] = row[head['Obs Price']];

# Insert products
cur.executemany("""
INSERT INTO product (
  id,
  name,
  category,
  energy,
  carbohydrates,
  fat,
  protein
) VALUES (
  %(id)s,
  %(name)s,
  '',
  0,
  0,
  0,
  0
)
ON CONFLICT (id) DO
UPDATE SET
  name = %(name)s
""", products.values())

conn.commit()
