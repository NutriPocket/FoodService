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


INSERT INTO foods (name, description, price) VALUES
    -- Subir de Peso (plan_id = 1)
    ('Pasta con salsa cremosa', 'Pasta con salsa de crema y pollo, alto en calorías.', 8.50),
    ('Batido de frutas y avena', 'Batido energético con frutas, avena y leche entera.', 5.00),
    -- Bajar de Peso (plan_id = 2)
    ('Ensalada de pollo', 'Ensalada fresca con pechuga de pollo a la plancha.', 7.00),
    ('Sopa de verduras', 'Sopa ligera de vegetales variados.', 4.50),
    -- Aumentar Masa Muscular (plan_id = 3)
    ('Pechuga de pollo con arroz integral', 'Plato alto en proteínas y carbohidratos complejos.', 9.00),
    ('Omelette de claras', 'Omelette de claras de huevo con espinaca.', 6.00),
    -- Bajar Grasa Corporal (plan_id = 4)
    ('Pescado al vapor con brócoli', 'Pescado magro al vapor acompañado de brócoli.', 10.00),
    ('Ensalada de atún', 'Ensalada baja en calorías con atún y vegetales.', 7.50),
    -- Mantenimiento (plan_id = 5)
    ('Pollo grillado con quinoa', 'Pollo grillado acompañado de quinoa y vegetales.', 8.50),
    ('Wrap integral de pavo', 'Wrap de pan integral con pavo y vegetales.', 6.50);


-- Create table 'plans'
CREATE TABLE IF NOT EXISTS plans (
    id_plan SERIAL PRIMARY KEY,
    title VARCHAR(255),
    plan_description VARCHAR(255),
    objetive VARCHAR(255)
);

-- Create table 'foodplanlink'
CREATE TABLE IF NOT EXISTS foodplanlink (
    food_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    PRIMARY KEY (food_id, plan_id),
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES plans(id_plan) ON DELETE CASCADE
);

-- Create table 'usuarios'
CREATE TABLE IF NOT EXISTS users (
    id_user VARCHAR(36) PRIMARY KEY,
    id_plan INTEGER REFERENCES plans(id_plan) ON DELETE SET NULL
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

-- Create join table for many-to-many relation between foods and meal moments
CREATE TABLE IF NOT EXISTS food_meal_moments (
    food_id INTEGER NOT NULL REFERENCES foods(id) ON DELETE CASCADE,
    meal_moment_id INTEGER NOT NULL REFERENCES meal_moments(id) ON DELETE CASCADE,
    PRIMARY KEY (food_id, meal_moment_id)
);

CREATE TABLE IF NOT EXISTS week_days (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO week_days (name) VALUES
('Lunes'), ('Martes'), ('Miércoles'), ('Jueves'), ('Viernes'), ('Sábado'), ('Domingo');

CREATE TABLE IF NOT EXISTS weekly_meal_plan_food (
    id SERIAL PRIMARY KEY,
    plan_id INTEGER NOT NULL REFERENCES plans(id_plan) ON DELETE CASCADE,
    day_id INTEGER NOT NULL REFERENCES week_days(id),
    meal_moment_id INTEGER NOT NULL REFERENCES meal_moments(id),
    food_id INTEGER NOT NULL REFERENCES foods(id)
);


-- Table: food_meal_moments (assumes columns: food_id, meal_moment_id)
-- Format: INSERT INTO food_meal_moments (food_id, meal_moment_id) VALUES (..., ...);

INSERT INTO food_meal_moments (food_id, meal_moment_id) VALUES
(1, 2),  -- Pasta con salsa cremosa -> Almuerzo
(1, 4),  -- Pasta con salsa cremosa -> Cena
(2, 1),  -- Batido de frutas y avena -> Desayuno
(2, 3),  -- Batido de frutas y avena -> Merienda
(3, 2),  -- Ensalada de pollo -> Almuerzo
(4, 4),  -- Sopa de verduras -> Cena
(5, 2),  -- Pechuga de pollo con arroz integral -> Almuerzo
(5, 4),  -- Pechuga de pollo con arroz integral -> Cena
(6, 1),  -- Omelette de claras -> Desayuno
(7, 4),  -- Pescado al vapor con brócoli -> Cena
(8, 2),  -- Ensalada de atún -> Almuerzo
(9, 2),  -- Pollo grillado con quinoa -> Almuerzo
(10, 3); -- Wrap integral de pavo -> Merienda

-- Inserting mock plans

INSERT INTO plans (title, plan_description, objetive)
VALUES ('Plan Subir de Peso', 'Plan nutricional diseñado para ganar masa.', 'Ganar peso de forma saludable');

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
        INSERT INTO weekly_meal_plan_food (plan_id, day_id, meal_moment_id, food_id)
        VALUES
            (1, day_id, 1, 2),  -- Desayuno
            (1, day_id, 2, 1),  -- Almuerzo
            (1, day_id, 3, 2),  -- Merienda
            (1, day_id, 4, 1);  -- Cena
    END LOOP;
END$$;

INSERT INTO plans (id_plan, title, plan_description, objetive)
VALUES (2, 'Plan Bajar de Peso', 'Plan balanceado para reducir grasa corporal.', 'Pérdida de peso');

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
        INSERT INTO weekly_meal_plan_food (plan_id, day_id, meal_moment_id, food_id)
        VALUES
            (2, day_id, 1, 6),   -- Desayuno
            (2, day_id, 2, 3),   -- Almuerzo
            (2, day_id, 3, 10),  -- Merienda
            (2, day_id, 4, 4);   -- Cena
    END LOOP;
END$$;

-- Link foods used in Plan 1 (Subir de Peso)
INSERT INTO foodplanlink (food_id, plan_id) VALUES
(1, 1),  -- Pasta con salsa cremosa
(2, 1);  -- Batido de frutas y avena

-- Link foods used in Plan 2 (Bajar de Peso)
INSERT INTO foodplanlink (food_id, plan_id) VALUES
(3, 2),   -- Ensalada de pollo
(4, 2),   -- Sopa de verduras
(6, 2),   -- Omelette de claras
(10, 2);  -- Wrap integral de pavo
