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
    calories_per_100g INT,
    protein_per_100g SMALLINT,
    carbs_per_100g SMALLINT,
    fiber_per_100g SMALLINT,
    saturated_fats_per_100g SMALLINT,
    monounsaturated_fats_per_100g SMALLINT,
    polyunsaturated_fats_per_100g SMALLINT,
    trans_fats_per_100g SMALLINT,
    cholesterol_per_100g SMALLINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO foods (name, description, price, calories_per_100g, protein_per_100g, carbs_per_100g, fiber_per_100g, saturated_fats_per_100g, monounsaturated_fats_per_100g, polyunsaturated_fats_per_100g, trans_fats_per_100g, cholesterol_per_100g) VALUES
    -- Subir de Peso (plan_id = 1)
    ('Pasta con salsa cremosa', 'Pasta con salsa de crema y pollo, alto en calorías.', 8.50, 180, 7, 28, 2, 3, 2, 1, 0, 25),
    ('Batido de frutas y avena', 'Batido energético con frutas, avena y leche entera.', 5.00, 110, 5, 18, 2, 1, 1, 0, 0, 10),
    -- Bajar de Peso (plan_id = 2)
    ('Ensalada de pollo', 'Ensalada fresca con pechuga de pollo a la plancha.', 7.00, 90, 12, 4, 2, 1, 1, 0, 0, 30),
    ('Sopa de verduras', 'Sopa ligera de vegetales variados.', 4.50, 45, 2, 8, 2, 0, 0, 0, 0, 0),
    -- Aumentar Masa Muscular (plan_id = 3)
    ('Pechuga de pollo con arroz integral', 'Plato alto en proteínas y carbohidratos complejos.', 9.00, 140, 16, 16, 2, 1, 1, 0, 0, 40),
    ('Omelette de claras', 'Omelette de claras de huevo con espinaca.', 6.00, 70, 11, 2, 1, 0, 1, 0, 0, 0),
    -- Bajar Grasa Corporal (plan_id = 4)
    ('Pescado al vapor con brócoli', 'Pescado magro al vapor acompañado de brócoli.', 10.00, 90, 13, 3, 2, 0, 1, 0, 0, 35),
    ('Ensalada de atún', 'Ensalada baja en calorías con atún y vegetales.', 7.50, 100, 12, 4, 2, 1, 1, 0, 0, 25),
    -- Mantenimiento (plan_id = 5)
    ('Pollo grillado con quinoa', 'Pollo grillado acompañado de quinoa y vegetales.', 8.50, 130, 14, 12, 2, 1, 1, 0, 0, 35),
    ('Wrap integral de pavo', 'Wrap de pan integral con pavo y vegetales.', 6.50, 160, 10, 22, 3, 2, 2, 0, 0, 20);


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