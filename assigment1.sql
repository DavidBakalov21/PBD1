CREATE TABLE shop_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product VARCHAR(100),
    price DECIMAL(8, 0),
    raiting INT
);
INSERT INTO shop_list (product, price, raiting) VALUES ('Table', 400, 3), ('Door', 630, 5), ('Mirror', 30, 1);