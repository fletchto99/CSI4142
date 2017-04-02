CREATE TABLE ProductPrice (
  date int references Date,
  product int references Product,
  location int references Location,
  price numeric(2),
);

CREATE TABLE Product (
  id int PRIMARY KEY,
  name text,
  category text,
  energy int,
  carbohydrates int,
  fat int,
  protein int,
);

CREATE TABLE Date (
  id int PRIMARY KEY,
  date date,
  day int, -- 0-6
  week int, -- 0-52
  month int, -- 0-12
  year int,
  weekend boolean,
);

CREATE TABLE Location (
  id int PRIMARY KEY,
  type int,
  city text,
  country text,
  gdp int,
  population int,
  life_expectancy int,
  average_income numeric(2),
);
