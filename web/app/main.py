from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from .startup import create_users_tables, insert_into_users
from ..routes.mysql import mysql_router
from ..routes.postgresql import postgresql_router
from .config import ALLOWED_DATABASES, ALLOWED_CONTEXTS, CONTEXT_CONFIG
from .database import run_mysql, run_postgresql

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

    if db == "mysql":
        response = run_mysql(
            "SELECT user_id, role, username, password, firstname, lastname, email, phone_number, age FROM Users;",
            is_fetch=True,
        )
    elif db == "postgresql":
        response = run_postgresql(
            "SELECT user_id, role, username, password, firstname, lastname, email, phone_number, age FROM Users;",
            is_fetch=True,
        )

    template_context = CONTEXT_CONFIG[db][context]
    template_context["users_table_content"] = response

    return templates.TemplateResponse(
        f"index.html", {"request": request, "context": template_context}
    )
