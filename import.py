#!/usr/bin/env python3

import csv
import psycopg2
from collections import defaultdict
from datetime import datetime

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

# Country specific data
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
        date = datetime.strptime(row[head['Obs Date (yyyy-MM-dd)']], '%Y-%m-%d')

        year, week, day = date.isocalendar()
        dates[date] = {
            'date': date,
            'day': day,
            'week': week,
            'month': date.month,
            'year': year,
            'weekend': day >= 6
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

# Upsert dates
cur.executemany("""
INSERT INTO date (
  date,
  day,
  week,
  month,
  year,
  weekend
) VALUES (
  %(date)s,
  %(day)s,
  %(week)s,
  %(month)s,
  %(year)s,
  %(weekend)s
)
ON CONFLICT (id) DO
UPDATE SET
  date = %(date)s,
  day = %(day)s,
  week = %(week)s,
  month = %(month)s,
  year = %(year)s,
  weekend = %(weekend)s
""", dates.values())

# Upsert products
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

# Upsert locations
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

# Upsert product prices
cur.executemany("""
INSERT INTO product_price (
  date,
  product,
  location,
  price
) VALUES (
  (SELECT id from date WHERE date = %(date)s),
  %(product)s,
  %(location)s,
  %(price)s
)
ON CONFLICT (date, product, location, price) DO
UPDATE SET
  price = %(price)s
""", product_prices.values())

conn.commit()
