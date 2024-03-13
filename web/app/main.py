from fastapi import FastAPI
from contextlib import asynccontextmanager
from .startup import create_users_tables, insert_into_users
from ..routes.mysql import mysql_router


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

# include db routes
app.include_router(mysql_router)
