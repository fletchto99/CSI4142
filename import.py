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

dates = {}
products = {}
locations = {}
product_prices = {}

gdp = {}
population = {}
life_expectancy = {}
avg_annual_income = {}

def latest_country_data(f):
    reader = csv.reader(f, delimiter=',', quotechar='"')

    # Skip useless header data
    for i in range(4): next(reader)

    head = dict(reversed(field) for field in enumerate(next(reader)))
    data = []

    for row in reader:
        history = (row[head[str(i)]] for i in range(2016, 1959, -1))
        latest = next((latest for latest in history if len(latest)), '')
        data.append((row[head['Country Name']], latest))

    return dict(data)

with open('datasets/gdp.csv') as f:
    gdp = latest_country_data(f)

with open('datasets/population-total.csv') as f:
    population = latest_country_data(f)

with open('datasets/life-expetency.csv') as f:
    life_expectancy = latest_country_data(f)

with open('datasets/avg-annual-income.csv') as f:
    avg_annual_income = latest_country_data(f)

with open('datasets/food-prices.csv') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    head = dict(reversed(field) for field in enumerate(next(reader)))

    for row in reader:
        dates[row[head['Obs Date (yyyy-MM-dd)']]] = {
            'date': row[head['Obs Date (yyyy-MM-dd)']]
        }

        products[row[head['Product Code']]] = {
            'id': row[head['Product Code']],
            'name': row[head['Product Name']]
        }

        locations[row[head['Location Code']]] = {
            'id': row[head['Location Code']],
            'city': row[head['Location Name']],
            'country': row[head['Country']],
            'gdp': gdp[row[head['Country']]],
            'population': population[row[head['Country']]],
            'life_expectancy': life_expectancy[row[head['Country']]],
            'avg_annual_income': avg_annual_income[row[head['Country']]]
        }

        product_prices[(
            row[head['Obs Date (yyyy-MM-dd)']],
            row[head['Product Code']],
            row[head['Location Code']]
        )] = {
            'date': row[head['Obs Date (yyyy-MM-dd)']],
            'product': row[head['Product Code']],
            'location': row[head['Location Code']],
            'price': row[head['Obs Price']]
        }

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

# Insert locations
cur.executemany("""
INSERT INTO location (
  id,
  type,
  city,
  country,
  gdp,
  population,
  life_expectancy,
  avg_annual_income
) VALUES (
  %(id)s,
  0,
  %(city)s,
  %(country)s,
  %(gdp)s,
  %(population)s,
  %(life_expectancy)s,
  %(avg_annual_income)s
)
ON CONFLICT (id) DO
UPDATE SET
  city = %(city)s,
  country = %(country)s,
  gdp = %(gdp)s,
  population = %(population)s,
  life_expectancy = %(life_expectancy)s,
  avg_annual_income = %(avg_annual_income)s
""", locations.values())

conn.commit()
