-- Connect to the default 'postgres' database
\c postgres;

-- Check if the database exists, if not, create it
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'database') THEN
      CREATE DATABASE database;
   END IF;
END
$do$;

-- Connect to the newly created database
\c database

-- Create the table 'foods'
CREATE TABLE IF NOT EXISTS foods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO foods (name, description, price)
VALUES 
  ('Grilled Chicken', 'Lean protein with herbs', 7.99),
  ('Brown Rice', 'Whole grain rice', 2.50),
  ('Broccoli', 'Steamed green broccoli', 1.75);


-- Create table 'plans'
CREATE TABLE IF NOT EXISTS plans (
    id_plan SERIAL PRIMARY KEY,
    title VARCHAR(255),
    plan_description VARCHAR(255),
    objetive VARCHAR(255)
);

INSERT INTO plans (title, plan_description, objetive)
VALUES
  ('Weight Loss Plan', 'Low-calorie meals', 'Lose weight'),
  ('Muscle Gain Plan', 'High protein meals', 'Gain muscle');

-- Create table 'usuarios'
CREATE TABLE IF NOT EXISTS users (
    id_user SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    id_plan INTEGER REFERENCES plans(id_plan) ON DELETE SET NULL
);

INSERT INTO users (name, id_plan)
VALUES
  ('Alice', 1),
  ('Bob', 2);


-- Create table 'foodplanlink'
CREATE TABLE IF NOT EXISTS foodplanlink (
    food_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    PRIMARY KEY (food_id, plan_id),
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES plans(id_plan) ON DELETE CASCADE
);

