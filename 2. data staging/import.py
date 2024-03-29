#!/usr/bin/env python3

import csv
import psycopg2
from collections import defaultdict
from datetime import datetime

dbconfig = {
    'dbname': 'csi4142_project',
    'user': 'postgres'
}

def latest_country_data(path):
    data = []

    print('Reading country data from: {}'.format(path))
    with open(path) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        # Skip useless header data
        for i in range(4): next(reader)

        head = dict(reversed(field) for field in enumerate(next(reader)))

        for row in reader:
            history = (row[head[str(i)]] for i in range(2016, 1959, -1))
            latest = next((latest for latest in history if len(latest)), '')
            data.append((row[head['Country Name']], latest))

    return dict(data)

def nutrition_facts(path):
    print ('Reading nutrition facts from: {}'.format(path))
    with open(path) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        head = dict(reversed(field) for field in enumerate(next(reader)))
        return dict((row[head['id']], {
            'category': row[head['category']],
            'energy': row[head['energy_100g']],
            'carbohydrates': row[head['carbohydrates_100g']],
            'fat': row[head['fat_100g']],
            'protein': row[head['proteins_100g']]
        }) for row in reader)

dates = {}
products = {}
locations = {}
product_prices = []

# Obtain latest country statistics
gdp = latest_country_data('datasets/gdp.csv')
population = latest_country_data('datasets/population-total.csv')
life_expectancy = latest_country_data('datasets/life-expetency.csv')
avg_annual_income = latest_country_data('datasets/avg-annual-income.csv')

# Obtain nutrition facts
nutrition_facts = nutrition_facts('datasets/nutrition-facts.csv')

with open('datasets/food-prices.csv') as f:
    print('Importing food prices from: {}'.format(f.name))

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

        nutrition = nutrition_facts[row[head['Product Code']]]
        products[row[head['Product Code']]] = {
            'id': row[head['Product Code']],
            'name': row[head['Product Name']],
            'category': nutrition['category'],
            'energy': nutrition['energy'],
            'carbohydrates': nutrition['carbohydrates'],
            'fat': nutrition['fat'],
            'protein': nutrition['protein']
        }

        locations[row[head['Location Code']]] = {
            'id': row[head['Location Code']],
            'type': row[head['Outlet Type']],
            'city': row[head['Location Name']],
            'country': row[head['Country']],
            'gdp': gdp[row[head['Country']]],
            'population': population[row[head['Country']]],
            'life_expectancy': life_expectancy[row[head['Country']]],
            'avg_annual_income': avg_annual_income[row[head['Country']]]
        }

        product_prices.append({
            'date': row[head['Obs Date (yyyy-MM-dd)']],
            'product': row[head['Product Code']],
            'location': row[head['Location Code']],
            'price': row[head['Conv. Price']]
        })

print('Connecting to database')
conn = psycopg2.connect(**dbconfig)
cur = conn.cursor()

print('Inserting records into date dimension')
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
ON CONFLICT (date) DO
UPDATE SET
  date = %(date)s,
  day = %(day)s,
  week = %(week)s,
  month = %(month)s,
  year = %(year)s,
  weekend = %(weekend)s
""", dates.values())

print('Inserting records into product dimension')
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
  %(category)s,
  %(energy)s,
  %(carbohydrates)s,
  %(fat)s,
  %(protein)s
)
ON CONFLICT (id) DO
UPDATE SET
  name = %(name)s,
  category = %(category)s,
  energy = %(energy)s,
  carbohydrates = %(carbohydrates)s,
  fat = %(fat)s,
  protein = %(protein)s
""", products.values())

print('Inserting records into location dimension')
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
  %(type)s,
  %(city)s,
  %(country)s,
  %(gdp)s,
  %(population)s,
  %(life_expectancy)s,
  %(avg_annual_income)s
)
ON CONFLICT (id) DO
UPDATE SET
  type = %(type)s,
  city = %(city)s,
  country = %(country)s,
  gdp = %(gdp)s,
  population = %(population)s,
  life_expectancy = %(life_expectancy)s,
  avg_annual_income = %(avg_annual_income)s
""", locations.values())

print('Inserting records into product_price fact table')
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
""", product_prices)

conn.commit()
