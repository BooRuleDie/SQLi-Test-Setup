from faker import Faker
import random
from passlib.context import CryptContext
from pprint import pprint

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
        )
        for _ in range(times)
    ]


pprint(get_fake_user_data(20)[:5])
