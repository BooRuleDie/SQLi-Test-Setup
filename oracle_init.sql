CREATE TABLE Users (
    user_id NUMBER PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(255),
    role VARCHAR2(10) CHECK (role IN ('customer', 'seller', 'agent', 'admin')),
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(100)
);

INSERT INTO Users (user_id, firstname, lastname, username, role, password, email, phone_number)
VALUES
    (1, 'Alice', 'Smith', 'asmith', 'customer', 'securepassword1', 'alice@example.com', '555-1234'),
    (2, 'Bob', 'Johnson', 'bjohnson', 'seller', 'strongpassword2', 'bob@example.com', '555-5678'),
    (3, 'Jane', 'Doe', 'jdoe', 'agent', 'complexpassword3', 'jane@example.com', '555-9012'),
    (4, 'Charlie', 'Wilson', 'cwilson', 'customer', 'securepassword4', 'charlie@example.com', '555-3456'),
    (5, 'Emily', 'Davis', 'edavis', 'admin', 'verystrongpassword5', 'emily@example.com', '555-7890');