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
    ingredients TEXT[],
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO foods ( name, description, price, calories_per_100g, protein_per_100g, carbs_per_100g, fiber_per_100g, saturated_fats_per_100g, monounsaturated_fats_per_100g,
    polyunsaturated_fats_per_100g, trans_fats_per_100g, cholesterol_per_100g, ingredients) VALUES
    
    -- Subir de Peso (plan_id = 1)
    ('Pasta con salsa cremosa', 'Pasta con salsa de crema y pollo, alto en calorías.', 8.50, 180, 7, 28, 2, 3, 2, 1, 0, 25,
    ARRAY['100g pasta cocida (¾ taza)', '50g crema (3 cucharadas)', '150g pechuga de pollo (1 unidad pequeña)', '5g queso parmesano (1 cucharada)', '5ml aceite de oliva (1 cucharadita)']),
    
    ('Batido de frutas y avena', 'Batido energético con frutas, avena y leche entera.', 5.00, 110, 5, 18, 2, 1, 1, 0, 0, 10,
    ARRAY['100ml leche entera (½ taza)', '50g banana (½ unidad)', '30g avena (3 cucharadas)', '10g miel (1 cucharada)', '50g frutillas (3 unidades medianas)']),

    -- Bajar de Peso (plan_id = 2)
    ('Ensalada de pollo', 'Ensalada fresca con pechuga de pollo a la plancha.', 7.00, 90, 12, 4, 2, 1, 1, 0, 0, 30,
    ARRAY['120g pechuga de pollo (1 unidad mediana)', '30g lechuga (1 taza picada)', '50g tomate (½ unidad)', '10ml aceite de oliva (1 cucharada)', '5ml jugo de limón (1 cucharadita)']),
    
    ('Sopa de verduras','Sopa ligera de vegetales variados.',4.50, 45, 2, 8, 2, 0, 0, 0, 0, 0,
    ARRAY['100g zapallo (½ taza en cubos)', '50g zanahoria (½ unidad)', '30g cebolla (2 cucharadas picadas)', '20g apio (2 ramitas)', '750ml agua (3 tazas)']),

    -- Aumentar Masa Muscular (plan_id = 3)
    ('Pechuga de pollo con arroz integral', 'Plato alto en proteínas y carbohidratos complejos.', 9.00, 140, 16, 16, 2, 1, 1, 0, 0, 40,
    ARRAY['150g pechuga de pollo (1 unidad grande)', '100g arroz integral cocido (½ taza)', '50g brócoli (½ taza)', '5ml aceite de oliva (1 cucharadita)', '1 pizca de sal y pimienta']),
    
    ('Omelette de claras','Omelette de claras de huevo con espinaca.',6.00, 70, 11, 2, 1, 0, 1, 0, 0, 0,
    ARRAY['4 claras de huevo (120g)', '30g espinaca (1 taza cruda)', '10g cebolla (1 cucharada picada)', '5ml aceite de oliva (1 cucharadita)', '1 pizca de sal']),

    -- Bajar Grasa Corporal (plan_id = 4)
    ('Pescado al vapor con brócoli', 'Pescado magro al vapor acompañado de brócoli.', 10.00, 90, 13, 3, 2, 0, 1, 0, 0, 35,
    ARRAY['150g pescado blanco (1 filete mediano)', '100g brócoli cocido (1 taza)', '5ml aceite de oliva (1 cucharadita)', '1 pizca de sal y limón al gusto']),
    
    ('Ensalada de atún', 'Ensalada baja en calorías con atún y vegetales.', 7.50, 100, 12, 4, 2, 1, 1, 0, 0, 25,
    ARRAY['80g atún al agua (½ lata)', '30g lechuga (1 taza picada)', '50g tomate (½ unidad)', '20g zanahoria rallada (2 cucharadas)', '10ml aceite de oliva (1 cucharada)']),

    -- Mantenimiento (plan_id = 5)
    ('Pollo grillado con quinoa', 'Pollo grillado acompañado de quinoa y vegetales.', 8.50, 130, 14, 12, 2, 1, 1, 0, 0, 35,
    ARRAY['150g pollo grillado (1 unidad)','100g quinoa cocida (½ taza)','50g zanahoria (½ unidad)','30g pimiento rojo (3 cucharadas picadas)','10ml aceite de oliva (1 cucharada)']),
    
    ('Wrap integral de pavo', 'Wrap de pan integral con pavo y vegetales.', 6.50, 160, 10, 22, 3, 2, 2, 0, 0, 20,
    ARRAY['1 wrap de pan integral (60g)','80g pavo cocido (2 fetas gruesas)','30g lechuga (1 taza picada)','30g tomate (2 rodajas)','10g mayonesa light (1 cucharada)']);


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

-- Table 'Extra Foods'
CREATE TABLE IF NOT EXISTS extra_foods (
    id_extra_food SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    ingredients TEXT[] NOT NULL,
    image_url VARCHAR(255),
    day VARCHAR(255) NOT NULL,
    moment VARCHAR(255) NOT NULL,
    date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS extrafood_user_link (
    id_extra_food INTEGER NOT NULL,
    id_user VARCHAR(36) NOT NULL,
    PRIMARY KEY (id_extra_food, id_user),
    FOREIGN KEY (id_extra_food) REFERENCES extra_foods(id_extra_food) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
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