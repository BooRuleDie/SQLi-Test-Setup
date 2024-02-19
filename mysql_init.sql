-- create users table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,  
    username VARCHAR(100),
    password VARCHAR(255),
    role ENUM('customer', 'seller', 'agent', 'admin'), 
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(100)
);

-- Insert your 5 example users
INSERT INTO Users (firstname, lastname, username, role, password, email, phone_number)
VALUES
    ('Alice', 'Smith', 'asmith', 'customer', 'securepassword1', 'alice@example.com', '555-1234'),
    ('Bob', 'Johnson', 'bjohnson', 'seller', 'strongpassword2', 'bob@example.com', '555-5678'),
    ('Jane', 'Doe', 'jdoe', 'agent', 'complexpassword3', 'jane@example.com', '555-9012'),
    ('Charlie', 'Wilson', 'cwilson', 'customer', 'securepassword4', 'charlie@example.com', '555-3456'),
    ('Emily', 'Davis', 'edavis', 'admin', 'verystrongpassword5', 'emily@example.com', '555-7890');
