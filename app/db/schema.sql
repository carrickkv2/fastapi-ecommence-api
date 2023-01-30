CREATE TABLE products (
    id SERIAL NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    image VARCHAR NOT NULL,
    price INTEGER NOT NULL,
    currency VARCHAR NOT NULL,
    discount BOOLEAN NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id)
) CREATE TABLE users (
    id SERIAL NOT NULL,
    email VARCHAR NOT NULL,
    phone_number VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id)
) CREATE TABLE orders (
    id SERIAL NOT NULL,
    customer_phone VARCHAR NOT NULL,
    unique_reference_id VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    total_amount INTEGER NOT NULL,
    order_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(customer_phone) REFERENCES users (phone_number)
) CREATE TABLE orderproducts (
    id SERIAL NOT NULL,
    product_id INTEGER NOT NULL,
    product_quantity INTEGER NOT NULL,
    order_id INTEGER,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(product_id) REFERENCES products (id),
    FOREIGN KEY(order_id) REFERENCES orders (id)
)
