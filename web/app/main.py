from fastapi import FastAPI
from contextlib import asynccontextmanager
from .startup import create_users_tables, insert_into_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup -> create Users table

    # create Users table
    await create_users_tables()

    # insert into Users table
    await insert_into_users()

    yield
    # on shutdown -> do nothing


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return 1
