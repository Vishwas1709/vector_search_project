CREATE TABLE products_vectors (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    vector JSON
);

CREATE INDEX idx_product_name ON products_vectors(product_name);
