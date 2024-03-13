import asyncio
from .database import run_mysql, run_postgresql
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
            fake.user_name(),
            get_password_hash(fake.password()),
            random.choice(["customer", "seller", "agent"]),
            fake.first_name(),
            fake.last_name(),
            fake.email(),
            fake.msisdn(),
            random.randint(17, 60)
        )
        for _ in range(times)
    ]


async def create_users_tables():
    await asyncio.gather(
        asyncio.to_thread(
            run_mysql,
            SQL="""CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,  
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
            user_id SERIAL PRIMARY KEY, 
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
    )


async def insert_into_users():
    fake_user_data = get_fake_user_data(16)

    await asyncio.gather(
        asyncio.to_thread(
            run_mysql,
            SQL="""INSERT INTO Users(username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);""",
            is_fetch=False,
            params=fake_user_data[:4],
        ),
        asyncio.to_thread(
            run_mysql,
            SQL="""INSERT INTO Users(username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);""",
            is_fetch=False,
            params=[
                (
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
            SQL="""INSERT INTO Users(username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);""",
            is_fetch=False,
            params=fake_user_data[5:9],
        ),
        asyncio.to_thread(
            run_postgresql,
            SQL="""INSERT INTO Users(username, password, role, firstname, lastname, email, phone_number, age)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);""",
            is_fetch=False,
            params=[
                (
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
