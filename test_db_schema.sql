-- test_db_schema.sql

-- Create the database manually before running this file
-- CREATE DATABASE test_db;
-- \c test_db

-- 1. Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);

INSERT INTO users (name, email) VALUES
('Pulkit Arora', 'pulkit@example.com'),
('Alex Ray', 'alex@example.com');

-- 2. Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    amount NUMERIC
);

INSERT INTO orders (user_id, amount) VALUES
(1, 250.75),
(2, 99.99);

-- 3. Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    price NUMERIC
);

INSERT INTO products (name, price) VALUES
('Keyboard', 49.99),
('Monitor', 129.50);

-- 4. Order Items table (composite key)
CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 2),
(1, 2, 1),
(2, 1, 1);

-- 5. Logs table (anomaly - no primary key)
CREATE TABLE logs (
    event TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO logs (event) VALUES
('Login attempt'),
('Order placed'),
('Password changed');
