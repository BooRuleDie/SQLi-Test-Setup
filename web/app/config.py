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
