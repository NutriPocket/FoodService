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

-- Load data into 'plans' table
INSERT INTO plans (title, plan_description, objetive) VALUES
    (
        'Subir de Peso',
        'Plan diseñado para personas que desean aumentar su peso corporal de manera saludable, priorizando alimentos calóricos y nutritivos.',
        'Subir de peso'
    ),
    (
        'Bajar de Peso',
        'Plan enfocado en la reducción de peso corporal mediante un déficit calórico y selección de alimentos bajos en grasas y azúcares.',
        'Bajar de peso'
    ),
    (
        'Aumentar Masa Muscular',
        'Plan orientado a quienes buscan incrementar su masa muscular, con alto contenido proteico y distribución adecuada de carbohidratos y grasas.',
        'Aumentar masa muscular'
    ),
    (
        'Bajar Grasa Corporal',
        'Plan para reducir el porcentaje de grasa corporal, priorizando alimentos magros, vegetales y controlando la ingesta calórica.',
        'Bajar grasa corporal'
    ),
    (
        'Mantenimiento',
        'Plan equilibrado para mantener el peso y la composición corporal actual, con variedad de alimentos y control de porciones.',
        'Mantener peso'
    );
    

-- Create table 'foodplanlink'
CREATE TABLE IF NOT EXISTS foodplanlink (
    food_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    PRIMARY KEY (food_id, plan_id),
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES plans(id_plan) ON DELETE CASCADE
);

-- Relacionar comidas con planes
INSERT INTO foodplanlink (food_id, plan_id) VALUES
    -- Subir de Peso
    (1, 1), (2, 1),
    -- Bajar de Peso
    (3, 2), (4, 2),
    -- Aumentar Masa Muscular
    (5, 3), (6, 3),
    -- Bajar Grasa Corporal
    (7, 4), (8, 4),
    -- Mantenimiento
    (9, 5), (10, 5); 

-- Create table 'usuarios'
CREATE TABLE IF NOT EXISTS users (
    id_user VARCHAR(36) PRIMARY KEY,
    id_plan INTEGER REFERENCES plans(id_plan) ON DELETE SET NULL
);