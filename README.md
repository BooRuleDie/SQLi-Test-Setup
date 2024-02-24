# SQLi Test Set Up for Following Databases

1. PostgreSQL ✅
2. MySQL ✅
3. MSSQL ✅
4. ORACLE ✅

### Users Table

There is a **`Users`** table in each database so you can perform tests on that table.
```SQL
-- MySQL example
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
```

### Commands

```bash
# deploy database containers -> docker compose up -d 
make up
	
# shutdown deployed containers -> docker compose down
make down

# show current container status -> docker container ls -a
make status
```

### Details

I recommend using DBeaver as it's compatible with all these databases. If that's the case, you should use the following URL value to be able to connect MySQL properly:
```URL
jdbc:mysql://localhost:3306/test_db?allowPublicKeyRetrieval=true&useSSL=false
```

In order to connect ORACLE database, you can use following data:
* database name: `FREEPDB1`
* username: `SYS`
* role: `SYSDBA`
* password: `password you specified in the docker-compose file`
