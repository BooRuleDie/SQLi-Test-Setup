from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class CREDS(BaseSettings):
    HOST: str

    MYSQL_USERNAME: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_PORT: int

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    MSSQL_USERNAME: str
    MSSQL_DATABASE: str
    MSSQL_SA_PASSWORD: str
    MSSQL_PORT: int

    ORACLE_USERNAME: str
    ORACLE_DATABASE: str
    ORACLE_PASSWORD: str
    ORACLE_ROLE: str
    ORACLE_PORT: int

    ADMIN_PASSWORD: str


creds = CREDS()

ALLOWED_DATABASES = ("mysql", "postgresql", "mssql", "oracle")
ALLOWED_CONTEXTS = (
    "where-int",
    "where-string",
    "like-int",
    "like-string",
    "order-by-int",
    "order-by-string",
    "in-int",
    "in-string",
)
CONTEXT_CONFIG = {
    "mysql": {
        "where-int": {
            "database_name": "MySQL",
            "badge": "WHERE-INT",
            "SQL": """SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE user_id = 1;""",
            "json_response": """{
  "user_id": 1,
  "username": "christinajohnson",
  "firstname": "Matthew",
  "lastname": "Marshall",
  "email": "qortiz@example.org",
  "role": "customer",
  "age": 27
}""",
            "backend": '''@mysql_router.get("/where/int")
async def mysql_where_int(user_id: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname,
        lastname, email, role, age
        FROM Users
        WHERE user_id={user_id};""",
    )
    
    if not response:
        return {"message": "invalid user_id"}
    
    if response[0]["role"] == "admin":
        return {"message": "unauthorized action"}
    
    return response[0]''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE user_id = ${userId};</code>`""",
            "api_endpoint": "`/mysql/where/int?user_id=${userId}`",
        },
        "where-string": {},
        "like-int": {},
        "like-string": {},
        "order-by-int": {},
        "order-by-string": {},
        "in-int": {},
        "in-string": {},
    },
    "postgresql": {
        "where-int": {
            "database_name": "MySQL",
        },
        "where-string": {},
        "like-int": {},
        "like-string": {},
        "order-by-int": {},
        "order-by-string": {},
        "in-int": {},
        "in-string": {},
    },
    "mssql": {
        "where-int": {
            "database_name": "MySQL",
        },
        "where-string": {},
        "like-int": {},
        "like-string": {},
        "order-by-int": {},
        "order-by-string": {},
        "in-int": {},
        "in-string": {},
    },
    "oracle": {
        "where-int": {
            "database_name": "MySQL",
        },
        "where-string": {},
        "like-int": {},
        "like-string": {},
        "order-by-int": {},
        "order-by-string": {},
        "in-int": {},
        "in-string": {},
    },
}
