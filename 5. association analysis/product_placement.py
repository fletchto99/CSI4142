#!/usr/bin/env python3

import psycopg2
import argparse
from apyori import apriori

def product_placement(conn, country):
    cur = conn.cursor()
    cur.execute("""
    SELECT array_agg(p.name)
    FROM product_price pp
    INNER JOIN product p ON
      p.id = pp.product
    INNER JOIN location l ON
      l.id = pp.location
    WHERE l.country = 'Kenya'
    GROUP BY pp.date
    """)

    for x in apriori((set(row[0]) for row in cur), min_support=1.0):
        print(" + ".join(x.items))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--dbname',
                        help='Database name',
                        default='csi4142_project')
    
    parser.add_argument('-u', '--user',
                        help='Database username',
                        default='postgres')

    parser.add_argument('-p', '--password',
                        help='Database password',
                        default=None)

    parser.add_argument('-c', '--country',
                        help='Country to use in query',
                        default='Kenya')

    args = parser.parse_args()
    product_placement(psycopg2.connect(
        dbname=args.dbname,
        user=args.user,
        password=args.password,
    ), args.country)
