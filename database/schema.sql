-- TODO: Definir las tablas del sistema

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    -- TODO: Agregar campos para id, username, email, password_hash, created_at
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    create_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tabla de productos  
CREATE TABLE IF NOT EXISTS products (
    -- TODO: Agregar campos para id, name, description, price, stock, image_url, created_at
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL DEFAULT 0.00,
    stock INTEGER NOT NULL DEFAULT 0,
    image_url TEXT,
    create_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tabla de carritos
CREATE TABLE IF NOT EXISTS carts (
    -- TODO: Agregar campos para id, user_id, created_at, updated_at
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    create_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tabla de items del carrito
CREATE TABLE IF NOT EXISTS cart_items (
    -- TODO: Agregar campos para id, cart_id, product_id, quantity, added_at
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL DEFAULT 1,
    added_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_cart_product UNIQUE (cart_id, product_id)
);

-- TODO: Agregar índices y restricciones de clave foránea

CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_carts_user_id ON carts(user_id);

-- TODO: Insertar datos de prueba
-- Usuarios
INSERT INTO users (username, email, password_hash) VALUES
  ('juan_perez',  'juan@example.com',  '$2b$12$abc123hashejemplo1'),
  ('maria_lopez', 'maria@example.com', '$2b$12$abc123hashejemplo2'),
  ('carlos_dev',  'carlos@example.com','$2b$12$abc123hashejemplo3');

-- Productos
INSERT INTO products (name, description, price, stock, image_url) VALUES
  ('Laptop Pro 15',    'Laptop de alto rendimiento con 16GB RAM',        1299.99, 10, 'https://example.com/laptop.jpg'),
  ('Mouse Inalámbrico','Mouse ergonómico con batería recargable',           29.99, 50, 'https://example.com/mouse.jpg'),
  ('Teclado Mecánico', 'Teclado con switches azules retroiluminado',        89.99, 25, 'https://example.com/teclado.jpg'),
  ('Monitor 27"',      'Monitor 4K con panel IPS',                        399.99,  8, 'https://example.com/monitor.jpg'),
  ('Auriculares BT',   'Auriculares bluetooth con cancelación de ruido',  149.99, 15, NULL);

-- Carritos (uno por usuario)
INSERT INTO carts (user_id) VALUES
  (1),
  (2),
  (3);

-- Items del carrito
INSERT INTO cart_items (cart_id, product_id, quantity) VALUES
  ((SELECT id FROM carts WHERE user_id = 1), 1, 1),  -- juan tiene una Laptop
  ((SELECT id FROM carts WHERE user_id = 1), 2, 2),  -- juan tiene 2 mouses
  ((SELECT id FROM carts WHERE user_id = 1), 3, 1),  -- juan tiene un teclado
  ((SELECT id FROM carts WHERE user_id = 2), 4, 1),  -- maria tiene un monitor
  ((SELECT id FROM carts WHERE user_id = 2), 5, 1),  -- maria tiene auriculares
  ((SELECT id FROM carts WHERE user_id = 3), 5, 1),  -- carlos tiene auriculares
  ((SELECT id FROM carts WHERE user_id = 3), 2, 1);  -- carlos tiene un mouse