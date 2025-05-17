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

-- Create table 'plans'
CREATE TABLE IF NOT EXISTS plans (
    id_plan SERIAL PRIMARY KEY,
    title VARCHAR(255),
    plan_description VARCHAR(255),
    objetive VARCHAR(255)
);

-- Load data into 'foods' table
INSERT INTO plans (id_plan, title, plan_description, objetive) VALUES
    (
        1,
        'Plan Subir de Peso',
        'Plan diseñado para personas que desean aumentar su peso corporal de manera saludable, priorizando alimentos calóricos y nutritivos.',
        'Subir de peso'
    ),
    (
        2,
        'Plan Bajar de Peso',
        'Plan enfocado en la reducción de peso corporal mediante un déficit calórico y selección de alimentos bajos en grasas y azúcares.',
        'Bajar de peso'
    ),
    (
        3,
        'Plan Aumentar Masa Muscular',
        'Plan orientado a quienes buscan incrementar su masa muscular, con alto contenido proteico y distribución adecuada de carbohidratos y grasas.',
        'Aumentar masa muscular'
    ),
    (
        4,
        'Plan Bajar Grasa Corporal',
        'Plan para reducir el porcentaje de grasa corporal, priorizando alimentos magros, vegetales y controlando la ingesta calórica.',
        'Bajar grasa corporal'
    ),
    (
        5,
        'Plan Mantenimiento',
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

-- Create table 'usuarios'
CREATE TABLE IF NOT EXISTS users (
    id_user VARCHAR(36) PRIMARY KEY,
    id_plan INTEGER REFERENCES plans(id_plan) ON DELETE SET NULL
);