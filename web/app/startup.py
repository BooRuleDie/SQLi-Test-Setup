import asyncio
from .database import run_mysql, run_postgresql, run_mssql, run_oracle
from faker import Faker
from passlib.context import CryptContext
import random
from .config import creds

fake = Faker()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def get_fake_user_data(times: int):
    return [
        (
            (index % 4) + 1,
            fake.user_name(),
            get_password_hash(fake.password()),
            random.choice(["customer", "seller", "agent"]),
            fake.first_name(),
            fake.last_name(),
            fake.email(),
            fake.msisdn(),
            random.randint(17, 60)
        )
        for index in range(times)
    ]


async def create_users_tables():
    await asyncio.gather(
        asyncio.to_thread(
            run_mysql,
            SQL="""CREATE TABLE IF NOT EXISTS Users (
            user_id INT PRIMARY KEY,  
            username VARCHAR(100),
            password VARCHAR(255),
            role ENUM('customer', 'seller', 'agent', 'admin'), 
            firstname VARCHAR(100),
            lastname VARCHAR(100),
            email VARCHAR(100),
            phone_number VARCHAR(100),
            age INT
        );""",
            is_fetch=False,
        ),
        asyncio.to_thread(
            run_postgresql,
            SQL="""CREATE TABLE IF NOT EXISTS Users (
            user_id INT PRIMARY KEY, 
            username VARCHAR(100),
            password VARCHAR(255),
            role VARCHAR(255),
            firstname VARCHAR(100),
            lastname VARCHAR(100),
            email VARCHAR(100),
            phone_number VARCHAR(100),
            age INT
        );""",
            is_fetch=False,
        ),
        asyncio.to_thread(
            run_oracle,
            SQL="""CREATE TABLE Users (
            user_id NUMBER PRIMARY KEY,
            username VARCHAR2(100),
            password VARCHAR2(255),
            role VARCHAR2(10) CHECK (role IN ('customer', 'seller', 'agent', 'admin')),
            firstname VARCHAR2(100),
            lastname VARCHAR2(100),
            email VARCHAR2(100),
            phone_number VARCHAR2(100),
            age NUMBER
        )""",
            is_fetch=False
        ),
        asyncio.to_thread(
            run_mssql,
            SQL="""CREATE TABLE Users (
            user_id INT PRIMARY KEY,
            username VARCHAR(100),
            password VARCHAR(255),
            role VARCHAR(10) CHECK (role IN ('customer', 'seller', 'agent', 'admin')),
            firstname VARCHAR(100),
            lastname VARCHAR(100),
            email VARCHAR(100),
            phone_number VARCHAR(100),
            age INT
        );""",
            is_fetch=False
        ),
    )


async def insert_into_users():
    fake_user_data = get_fake_user_data(16)

    await asyncio.gather(
        asyncio.to_thread(
            run_mysql,
            SQL="""INSERT INTO Users(user_id, username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            is_fetch=False,
            params=fake_user_data[:4],
        ),
        asyncio.to_thread(
            run_mysql,
            SQL="""INSERT INTO Users(user_id, username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            is_fetch=False,
            params=[
                (
                    5,
                    "superadmin",
                    get_password_hash(creds.ADMIN_PASSWORD),
                    "admin",
                    "admin",
                    "admin",
                    "admin@admin.com",
                    "90123456789",
                    23
                )
            ],
        ),
        asyncio.to_thread(
            run_postgresql,
            SQL="""INSERT INTO Users(user_id, username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            is_fetch=False,
            params=fake_user_data[4:8],
        ),
        asyncio.to_thread(
            run_postgresql,
            SQL="""INSERT INTO Users(user_id, username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            is_fetch=False,
            params=[
                (
                    5,
                    "superadmin",
                    get_password_hash(creds.ADMIN_PASSWORD),
                    "admin",
                    "admin",
                    "admin",
                    "admin@admin.com",
                    "90123456789",
                    23
                )
            ],
        ),
        asyncio.to_thread(
            run_oracle,
            SQL="""INSERT INTO Users(user_id, username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9)""",
            is_fetch=False,
            params=fake_user_data[8:12],
        ),
        asyncio.to_thread(
            run_oracle,
            SQL="""INSERT INTO Users(user_id, username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9)""",
            is_fetch=False,
            params=[
                (
                    5,
                    "superadmin",
                    get_password_hash(creds.ADMIN_PASSWORD),
                    "admin",
                    "admin",
                    "admin",
                    "admin@admin.com",
                    "90123456789",
                    23
                )
            ],
        ),
        asyncio.to_thread(
            run_mssql,
            SQL="""INSERT INTO Users(user_id, username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            is_fetch=False,
            params=fake_user_data[12:],
        ),
        asyncio.to_thread(
            run_mssql,
            SQL="""INSERT INTO Users(user_id, username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            is_fetch=False,
            params=[
                (
                    5,
                    "superadmin",
                    get_password_hash(creds.ADMIN_PASSWORD),
                    "admin",
                    "admin",
                    "admin",
                    "admin@admin.com",
                    "90123456789",
                    23
                )
            ],
        ),
    )
