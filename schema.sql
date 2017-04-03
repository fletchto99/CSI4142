CREATE TABLE date (
  id SERIAL PRIMARY KEY,
  date date NOT NULL,
  day int NOT NULL CHECK (day >= 1 AND day <= 7),
  week int NOT NULL CHECK (week >= 1 AND week <= 53),
  month int NOT NULL CHECK (month >= 1 AND month <= 12),
  year int NOT NULL,
  weekend boolean NOT NULL
);

CREATE TABLE product (
  id int PRIMARY KEY,
  name text NOT NULL,
  category text NOT NULL,
  energy int NOT NULL,
  carbohydrates int NOT NULL,
  fat int NOT NULL,
  protein int NOT NULL
);

CREATE TABLE location (
  id int PRIMARY KEY,
  type int NOT NULL,
  city text NOT NULL,
  country text NOT NULL,
  gdp numeric NOT NULL,
  population int NOT NULL,
  life_expectancy numeric NOT NULL,
  avg_annual_income numeric NOT NULL
);

CREATE TABLE product_price (
  date int NOT NULL REFERENCES date (id),
  product int NOT NULL REFERENCES product (id),
  location int NOT NULL REFERENCES location (id),
  price numeric NOT NULL,
  PRIMARY KEY (date, product, location, price)
);
