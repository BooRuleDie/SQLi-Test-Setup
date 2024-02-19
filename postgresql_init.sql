-- create role enum type
CREATE TYPE user_roles AS ENUM ('customer', 'seller', 'agent', 'admin');

-- create Users table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,  -- SERIAL for auto-incrementing integer
    username VARCHAR(100),
    password VARCHAR(255),
    role user_roles,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(100)
);

-- insert 5 users into the Users table
INSERT INTO Users (firstname, lastname, username, role, password, email, phone_number)
VALUES
    ('Alice', 'Smith', 'asmith', 'customer', 'securepassword1', 'alice@example.com', '555-1234'),
    ('Bob', 'Johnson', 'bjohnson', 'seller', 'strongpassword2', 'bob@example.com', '555-5678'),
    ('Jane', 'Doe', 'jdoe', 'agent', 'complexpassword3', 'jane@example.com', '555-9012'),
    ('Charlie', 'Wilson', 'cwilson', 'customer', 'securepassword4', 'charlie@example.com', '555-3456'),
    ('Emily', 'Davis', 'edavis', 'admin', 'verystrongpassword5', 'emily@example.com', '555-7890');
