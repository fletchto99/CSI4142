CREATE TABLE date (
  id SERIAL PRIMARY KEY,
  date date NOT NULL,
  day int NOT NULL CHECK (day >= 0 AND day <= 6),
  week int NOT NULL CHECK (week >= 0 AND week <= 52),
  month int NOT NULL CHECK (month > 0 AND month <= 12),
  year int NOT NULL,
  weekend boolean NOT NULL
);

CREATE TABLE product (
  id SERIAL PRIMARY KEY,
  name text NOT NULL,
  category text NOT NULL,
  energy int NOT NULL,
  carbohydrates int NOT NULL,
  fat int NOT NULL,
  protein int NOT NULL
);

CREATE TABLE location (
  id SERIAL PRIMARY KEY,
  type int NOT NULL,
  city text NOT NULL,
  country text NOT NULL,
  gdp int NOT NULL,
  population int NOT NULL,
  life_expectancy int NOT NULL,
  average_income numeric(2) NOT NULL
);

CREATE TABLE product_price (
  date int NOT NULL REFERENCES date (id),
  product int NOT NULL REFERENCES product (id),
  location int NOT NULL REFERENCES location (id),
  price numeric(2) NOT NULL
);
