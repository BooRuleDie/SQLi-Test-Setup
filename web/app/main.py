from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from .startup import create_users_tables, insert_into_users
from ..routes.mysql import mysql_router
from ..routes.postgresql import postgresql_router
from .config import ALLOWED_DATABASES, ALLOWED_CONTEXTS

templates = Jinja2Templates(directory="web/templates")


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

# staticfile mounting
app.mount("/static", StaticFiles(directory="./web/static"), name="static")

# include db routes
app.include_router(mysql_router)
app.include_router(postgresql_router)


@app.get("/")
async def home(request: Request, context: str = "where-int", db: str = "mysql"):
    """
    ## Possible context values
    * where-int
    * where-string
    * like-int
    * like-string
    * order-by-int
    * order-by-string
    * in-int
    * in-string

    ## Possible db values
    * mysql
    * postgresql
    * mssql
    * oracle
    """

    if db not in ALLOWED_DATABASES:
        return {
            "msg": "invalid database type",
            "allowed_databases": ALLOWED_DATABASES,
        }

    if context not in ALLOWED_CONTEXTS:
        return {
            "msg": "invalid context type",
            "allowed_contexts": ALLOWED_CONTEXTS,
        }
    
    return templates.TemplateResponse(f"{context}.html", {"request": request, "db": db})

   
