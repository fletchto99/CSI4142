#!/usr/bin/env python3

import csv
import psycopg2

dbconfig = {
    'dbname': 'postgres',
    'user': 'postgres'
}

conn = psycopg2.connect(**dbconfig)
cur = conn.cursor()

dates = {}
products = {}
locations = {}
product_prices = []

with open('datasets/food-prices.csv') as f:
    reader = csv.DictReader(f)

    for row in reader:
        date = row['Obs Date (yyyy-MM-dd)']
        if not date in dates:
            dates[date] = True

        product = row['Product Code']
        if not product in products:
            products[product] = {
                'id': product,
                'name': row['Product Name']
            }

        location = row['Location Code']
        if not location in locations:
            locations[location] = {
                'id': location,
                'type': None,
                'city': row['Location Name'],
                'country': row['Country'],
                'gdp': None,
                'population': None,
                'life_expectancy': None,
                'average_income': None
            }

        product_prices.append({
            'date': date,
            'product': product,
            'location': location,
            'price': row['Obs Price']
        })

print(product_prices)
