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

-- Create the table 'ingredients'
CREATE TABLE ingredients (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  measure_type VARCHAR(50) NOT NULL,
  calories FLOAT NOT NULL,
  protein FLOAT NOT NULL,
  carbs FLOAT NOT NULL,
  fiber FLOAT NOT NULL,
  saturated_fats FLOAT NOT NULL,
  monounsaturated_fats FLOAT NOT NULL,
  polyunsaturated_fats FLOAT NOT NULL,
  trans_fats FLOAT NOT NULL,
  cholesterol FLOAT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO ingredients (name, measure_type, calories, protein, carbs, fiber, saturated_fats, monounsaturated_fats, polyunsaturated_fats, trans_fats, cholesterol) VALUES
('Pasta cocida', 'gram', 130, 5, 25, 2, 0.2, 0.1, 0.1, 0, 0),
('Crema', 'gram', 350, 2.1, 3, 0, 20, 10, 5, 0, 30),
('Pechuga de pollo', 'gram', 165, 31, 0, 0, 1, 1.2, 0.4, 0, 85),
('Queso parmesano', 'gram', 431, 38, 4, 0, 29, 9, 1, 0, 88),
('Aceite de oliva', 'gram', 884, 0, 0, 0, 14, 73, 11, 0, 0),
('Leche entera', 'gram', 60, 3.2, 5, 0, 1.9, 0.7, 0.1, 0, 14),
('Banana', 'gram', 89, 1.1, 23, 2.6, 0.1, 0, 0, 0, 0),
('Avena', 'gram', 389, 17, 66, 11, 1.2, 3.4, 2.5, 0, 0),
('Miel', 'gram', 304, 0.3, 82, 0.2, 0, 0, 0, 0, 0),
('Frutillas', 'gram', 32, 0.7, 7.7, 2, 0.015, 0.04, 0.05, 0, 0),
('Lechuga', 'gram', 15, 1.4, 2.9, 1.3, 0.02, 0.05, 0.03, 0, 0),
('Tomate', 'gram', 18, 0.9, 3.9, 1.2, 0.03, 0.01, 0.17, 0, 0),
('Jugo de limón', 'gram', 22, 0.4, 7, 0.3, 0, 0, 0, 0, 0),
('Zanahoria', 'gram', 41, 0.9, 10, 2.8, 0.03, 0.02, 0.05, 0, 0),
('Cebolla', 'gram', 40, 1.1, 9.3, 1.7, 0.02, 0.01, 0.03, 0, 0),
('Apio', 'gram', 16, 0.7, 3, 1.6, 0.02, 0.01, 0.04, 0, 0),
('Zapallo', 'gram', 26, 1, 7, 1, 0.02, 0.01, 0.01, 0, 0),
('Agua', 'gram', 0, 0, 0, 0, 0, 0, 0, 0, 0),
('Pescado blanco', 'gram', 90, 20, 0, 0, 1, 2, 0.5, 0, 50),
('Brócoli', 'gram', 34, 2.8, 7, 2.6, 0.04, 0.01, 0.04, 0, 0),
('Atún al agua', 'gram', 116, 26, 0, 0, 0.7, 0.8, 0.3, 0, 50),
('Quinoa cocida', 'gram', 120, 4.1, 21, 2.8, 0.13, 0.43, 0.58, 0, 0),
('Pavo cocido', 'gram', 135, 29, 0, 0, 0.5, 0.6, 0.3, 0, 60),
('Mayonesa light', 'gram', 140, 0, 1, 0, 5, 7, 2, 0, 10),
('Pan integral', 'gram', 250, 9, 43, 7, 0.5, 1.5, 0.7, 0, 0),
('Claras de huevo', 'unit', 17, 3.6, 0, 0, 0, 0, 0, 0, 0),
('Espinaca', 'gram', 23, 2.9, 3.6, 2.2, 0.06, 0.01, 0.02, 0, 0);

-- Create the table 'foods'
CREATE TABLE IF NOT EXISTS foods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO foods (name, description, price, image_url)
VALUES
('Pasta con salsa cremosa', 'Pasta con salsa de crema y pollo, alto en calorías.', 8.50, NULL),
('Batido de frutas y avena', 'Batido energético con frutas, avena y leche entera.', 5.00, NULL),
('Ensalada de pollo', 'Ensalada fresca con pechuga de pollo a la plancha.', 7.00, NULL),
('Sopa de verduras','Sopa ligera de vegetales variados.',4.50, NULL),
('Pechuga de pollo con arroz integral', 'Plato alto en proteínas y carbohidratos complejos.', 9.00, NULL),
('Omelette de claras','Omelette de claras de huevo con espinaca.',6.00, NULL),
('Pescado al vapor con brócoli', 'Pescado magro al vapor acompañado de brócoli.', 10.00, NULL),
('Ensalada de atún', 'Ensalada baja en calorías con atún y vegetales.', 7.50, NULL),
('Pollo grillado con quinoa', 'Pollo grillado acompañado de quinoa y vegetales.', 8.50, NULL),
('Wrap integral de pavo', 'Wrap de pan integral con pavo y vegetales.', 6.50, NULL);

-- Create the table 'food_ingredients'
CREATE TABLE IF NOT EXISTS food_ingredients (
    food_id INT NOT NULL REFERENCES foods(id) ON DELETE CASCADE,
    ingredient_id INT NOT NULL REFERENCES ingredients(id) ON DELETE CASCADE,
    quantity FLOAT NOT NULL, -- en gramos o unidades según measure_type
    PRIMARY KEY(food_id, ingredient_id)
);

-- Pasta con salsa cremosa (food_id=1)
INSERT INTO food_ingredients (food_id, ingredient_id, quantity) VALUES
((SELECT id FROM foods WHERE name = 'Pasta con salsa cremosa'), (SELECT id FROM ingredients WHERE name = 'Pasta cocida'), 100),
((SELECT id FROM foods WHERE name = 'Pasta con salsa cremosa'), (SELECT id FROM ingredients WHERE name = 'Crema'), 50),
((SELECT id FROM foods WHERE name = 'Pasta con salsa cremosa'), (SELECT id FROM ingredients WHERE name = 'Pechuga de pollo'), 150),
((SELECT id FROM foods WHERE name = 'Pasta con salsa cremosa'), (SELECT id FROM ingredients WHERE name = 'Queso parmesano'), 5),
((SELECT id FROM foods WHERE name = 'Pasta con salsa cremosa'), (SELECT id FROM ingredients WHERE name = 'Aceite de oliva'), 5);

-- Batido de frutas y avena (food_id=2)
INSERT INTO food_ingredients (food_id, ingredient_id, quantity) VALUES
((SELECT id FROM foods WHERE name = 'Batido de frutas y avena'), (SELECT id FROM ingredients WHERE name = 'Leche entera'), 100),
((SELECT id FROM foods WHERE name = 'Batido de frutas y avena'), (SELECT id FROM ingredients WHERE name = 'Banana'), 50),
((SELECT id FROM foods WHERE name = 'Batido de frutas y avena'), (SELECT id FROM ingredients WHERE name = 'Avena'), 30),
((SELECT id FROM foods WHERE name = 'Batido de frutas y avena'), (SELECT id FROM ingredients WHERE name = 'Miel'), 10),
((SELECT id FROM foods WHERE name = 'Batido de frutas y avena'), (SELECT id FROM ingredients WHERE name = 'Frutillas'), 50);

-- Ensalada de pollo (food_id=3)
INSERT INTO food_ingredients (food_id, ingredient_id, quantity) VALUES
((SELECT id FROM foods WHERE name = 'Ensalada de pollo'), (SELECT id FROM ingredients WHERE name = 'Pechuga de pollo'), 120),
((SELECT id FROM foods WHERE name = 'Ensalada de pollo'), (SELECT id FROM ingredients WHERE name = 'Lechuga'), 30),
((SELECT id FROM foods WHERE name = 'Ensalada de pollo'), (SELECT id FROM ingredients WHERE name = 'Tomate'), 50),
((SELECT id FROM foods WHERE name = 'Ensalada de pollo'), (SELECT id FROM ingredients WHERE name = 'Aceite de oliva'), 10),
((SELECT id FROM foods WHERE name = 'Ensalada de pollo'), (SELECT id FROM ingredients WHERE name = 'Jugo de limón'), 5);

-- Sopa de verduras (food_id=4)
INSERT INTO food_ingredients (food_id, ingredient_id, quantity) VALUES
((SELECT id FROM foods WHERE name = 'Sopa de verduras'), (SELECT id FROM ingredients WHERE name = 'Zapallo'), 100),
((SELECT id FROM foods WHERE name = 'Sopa de verduras'), (SELECT id FROM ingredients WHERE name = 'Zanahoria'), 50),
((SELECT id FROM foods WHERE name = 'Sopa de verduras'), (SELECT id FROM ingredients WHERE name = 'Cebolla'), 30),
((SELECT id FROM foods WHERE name = 'Sopa de verduras'), (SELECT id FROM ingredients WHERE name = 'Apio'), 20),
((SELECT id FROM foods WHERE name = 'Sopa de verduras'), (SELECT id FROM ingredients WHERE name = 'Agua'), 750);

-- Pechuga de pollo con arroz integral (food_id=5)
INSERT INTO food_ingredients (food_id, ingredient_id, quantity) VALUES
((SELECT id FROM foods WHERE name = 'Pechuga de pollo con arroz integral'), (SELECT id FROM ingredients WHERE name = 'Pechuga de pollo'), 150),
((SELECT id FROM foods WHERE name = 'Pechuga de pollo con arroz integral'), (SELECT id FROM ingredients WHERE name = 'Pan integral'), 100);

-- Omelette de claras (food_id=6)
INSERT INTO food_ingredients (food_id, ingredient_id, quantity) VALUES
((SELECT id FROM foods WHERE name = 'Omelette de claras'), (SELECT id FROM ingredients WHERE name = 'Claras de huevo'), 3),
((SELECT id FROM foods WHERE name = 'Omelette de claras'), (SELECT id FROM ingredients WHERE name = 'Espinaca'), 40);

-- Pescado al vapor con brócoli (food_id=7)
INSERT INTO food_ingredients (food_id, ingredient_id, quantity) VALUES
((SELECT id FROM foods WHERE name = 'Pescado al vapor con brócoli'), (SELECT id FROM ingredients WHERE name = 'Pescado blanco'), 150),
((SELECT id FROM foods WHERE name = 'Pescado al vapor con brócoli'), (SELECT id FROM ingredients WHERE name = 'Brócoli'), 100);

-- Ensalada de atún (food_id=8)
INSERT INTO food_ingredients (food_id, ingredient_id, quantity) VALUES
((SELECT id FROM foods WHERE name = 'Ensalada de atún'), (SELECT id FROM ingredients WHERE name = 'Atún al agua'), 120),
((SELECT id FROM foods WHERE name = 'Ensalada de atún'), (SELECT id FROM ingredients WHERE name = 'Lechuga'), 30),
((SELECT id FROM foods WHERE name = 'Ensalada de atún'), (SELECT id FROM ingredients WHERE name = 'Tomate'), 50),
((SELECT id FROM foods WHERE name = 'Ensalada de atún'), (SELECT id FROM ingredients WHERE name = 'Aceite de oliva'), 10);

-- Pollo grillado con quinoa (food_id=9)
INSERT INTO food_ingredients (food_id, ingredient_id, quantity) VALUES
((SELECT id FROM foods WHERE name = 'Pollo grillado con quinoa'), (SELECT id FROM ingredients WHERE name = 'Pechuga de pollo'), 150),
((SELECT id FROM foods WHERE name = 'Pollo grillado con quinoa'), (SELECT id FROM ingredients WHERE name = 'Quinoa cocida'), 100),
((SELECT id FROM foods WHERE name = 'Pollo grillado con quinoa'), (SELECT id FROM ingredients WHERE name = 'Brócoli'), 50);

-- Wrap integral de pavo (food_id=10)
INSERT INTO food_ingredients (food_id, ingredient_id, quantity) VALUES
((SELECT id FROM foods WHERE name = 'Wrap integral de pavo'), (SELECT id FROM ingredients WHERE name = 'Pan integral'), 80),
((SELECT id FROM foods WHERE name = 'Wrap integral de pavo'), (SELECT id FROM ingredients WHERE name = 'Pavo cocido'), 100),
((SELECT id FROM foods WHERE name = 'Wrap integral de pavo'), (SELECT id FROM ingredients WHERE name = 'Lechuga'), 20),
((SELECT id FROM foods WHERE name = 'Wrap integral de pavo'), (SELECT id FROM ingredients WHERE name = 'Mayonesa light'), 10);


-- Create table 'plans'
CREATE TABLE IF NOT EXISTS plans (
    id_plan SERIAL PRIMARY KEY,
    title VARCHAR(255),
    plan_description VARCHAR(255),
    objetive VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserting mock plans

INSERT INTO 
    plans (title, plan_description, objetive)
VALUES 
    ('Plan Subir de Peso', 'Plan nutricional diseñado para ganar masa.', 'Ganar peso de forma saludable'),
    ('Plan Bajar de Peso', 'Plan balanceado para reducir grasa corporal.', 'Pérdida de peso');

-- Create table 'usuarios'
CREATE TABLE IF NOT EXISTS users (
    id_user VARCHAR(36) PRIMARY KEY,
    id_plan INTEGER REFERENCES plans(id_plan) ON DELETE SET NULL,
    updated_at TIMESTAMP NOT NULL
);

-- Create table for meal moments
CREATE TABLE IF NOT EXISTS meal_moments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Insert standard meal moments
INSERT INTO meal_moments (name) VALUES
('Desayuno'),
('Almuerzo'),
('Merienda'),
('Cena')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS week_days (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO week_days (name) VALUES
('Lunes'), ('Martes'), ('Miércoles'), ('Jueves'), ('Viernes'), ('Sábado'), ('Domingo');

-- Create table 'foodplanlink'
CREATE TABLE IF NOT EXISTS foodplanlink (
    food_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    day_id INTEGER NOT NULL REFERENCES week_days(id),
    meal_moment_id INTEGER NOT NULL REFERENCES meal_moments(id),
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (plan_id, day_id, meal_moment_id),
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES plans(id_plan) ON DELETE CASCADE,
    FOREIGN KEY (day_id) REFERENCES week_days(id) ON DELETE CASCADE,
    FOREIGN KEY (meal_moment_id) REFERENCES meal_moments(id) ON DELETE CASCADE
);

-- Link foods used in Plan 1 (Subir de Peso)
-- INSERT INTO foodplanlink (food_id, plan_id, day_id, meal_moment_id, updated_at) VALUES
-- (1, 1, NOW()),  -- Pasta con salsa cremosa
-- (2, 1, NOW());  -- Batido de frutas y avena

-- -- Link foods used in Plan 2 (Bajar de Peso)
-- INSERT INTO foodplanlink (food_id, plan_id, updated_at) VALUES
-- (3, 2, NOW()),   -- Ensalada de pollo
-- (4, 2, NOW()),   -- Sopa de verduras
-- (6, 2, NOW()),   -- Omelette de claras
-- (10, 2, NOW());  -- Wrap integral de pavo


-- Assign meals to each day

-- Desayuno: Batido de frutas y avena (id=2)
-- Almuerzo: Pasta con salsa cremosa (id=1)
-- Merienda: Batido de frutas y avena (id=2)
-- Cena: Pasta con salsa cremosa (id=1)

DO $$
DECLARE
    day_id INTEGER;
BEGIN
    FOR day_id IN 1..7 LOOP
        INSERT INTO foodplanlink (plan_id, day_id, meal_moment_id, food_id, updated_at)
        VALUES
            (1, day_id, 1, 2, NOW()),  -- Desayuno
            (1, day_id, 2, 1, NOW()),  -- Almuerzo
            (1, day_id, 3, 2, NOW()),  -- Merienda
            (1, day_id, 4, 1, NOW());  -- Cena
    END LOOP;
END$$;

-- Assign meals to each day

-- Desayuno: Omelette de claras (id=6)
-- Almuerzo: Ensalada de pollo (id=3)
-- Merienda: Wrap integral de pavo (id=10)
-- Cena: Sopa de verduras (id=4)

DO $$
DECLARE
    day_id INTEGER;
BEGIN
    FOR day_id IN 1..7 LOOP
        INSERT INTO foodplanlink (plan_id, day_id, meal_moment_id, food_id, updated_at)
        VALUES
            (2, day_id, 1, 6, NOW()),   -- Desayuno
            (2, day_id, 2, 3, NOW()),   -- Almuerzo
            (2, day_id, 3, 10, NOW()),  -- Merienda
            (2, day_id, 4, 4, NOW());   -- Cena
    END LOOP;
END$$;