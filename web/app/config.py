from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import json

load_dotenv()


class CREDS(BaseSettings):
    HOST: str

    MYSQL_USERNAME: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_PORT: int
    MYSQL_HOSTNAME: str

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRESQL_HOSTNAME: str

    MSSQL_USERNAME: str
    MSSQL_DATABASE: str
    MSSQL_SA_PASSWORD: str
    MSSQL_PORT: int
    MSSQL_HOSTNAME: str

    ORACLE_USERNAME: str
    ORACLE_DATABASE: str
    ORACLE_PASSWORD: str
    ORACLE_ROLE: str
    ORACLE_PORT: int
    ORACLE_HOSTNAME: str

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
            "placeholder": "user_id -> 1",
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
WHERE user_id = ${user_input};</code>`""",
            "api_endpoint": "`/mysql/where/int?user_id=${user_input}`",
        },
        "where-string": {
            "database_name": "MySQL",
            "badge": "WHERE-STRING",
            "placeholder": "username -> christinajohnson",
            "SQL": """SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE username = 'christinajohnson';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 27
}""",
            "backend": '''@mysql_router.get("/where/string")
async def mysql_where_string(username: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        WHERE username='{username}';""",
    )

    if not response:
        return {"message": "invalid username"}

    if response[0]["role"] == "admin":
        return {"message": "unauthorized action"}

    return response[0]''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE username = '${user_input}';</code>`""",
            "api_endpoint": "`/mysql/where/string?username=${user_input}`",
        },
        "like-int": {
            "database_name": "MySQL",
            "badge": "LIKE-INT",
            "placeholder": "age -> 18",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE age LIKE '%18%';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": '''@mysql_router.get("/like/int")
async def mysql_like_int(age: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        WHERE age LIKE '%{age}%';""",
    )

    if not response:
        return {"message": "invalid age"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE age LIKE '%${user_input}%';</code>`""",
            "api_endpoint": "`/mysql/like/int?age=${user_input}`",
        },
        "like-string": {
            "database_name": "MySQL",
            "badge": "LIKE-STRING",
            "placeholder": "username -> 'christinajohnson'",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE username LIKE '%christinajohnson%';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@mysql_router.get("/like/string")
async def mysql_like_string(username: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        WHERE username LIKE '%{username}%';""",
    )

    if not response:
        return {"message": "invalid username"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE username LIKE '%${user_input}%';</code>`""",
            "api_endpoint": "`/mysql/like/string?username=${user_input}`",
        },
        "order-by-int": {
            "database_name": "MySQL",
            "badge": "ORDER-BY-INT",
            "placeholder": "index -> 1",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY 1;""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@mysql_router.get("/order-by/int")
async def mysql_order_by_int(index: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        ORDER BY {index};""",
    )

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY ${user_input};</code>`""",
            "api_endpoint": "`/mysql/order-by/int?index=${user_input}`",
        },
        "order-by-string": {
            "database_name": "MySQL",
            "badge": "ORDER-BY-STRING",
            "placeholder": "field_name -> firstname",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY firstname;""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@mysql_router.get("/order-by/string")
async def mysql_order_by_string(field_name: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, 
        lastname, email, role, age 
        FROM Users 
        ORDER BY {field_name};""",
    )

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users ORDER BY ${user_input};</code>`""",
            "api_endpoint": "`/mysql/order-by/string?field_name=${user_input}`",
        },
        "in-int": {
            "database_name": "MySQL",
            "badge": "IN-INT",
            "placeholder": "user_ids -> 1,2,3",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE user_id IN(1,2,3);""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@mysql_router.get("/in/int")
async def mysql_in_int(user_ids: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, 
        lastname, email, role, age 
        FROM Users 
        WHERE user_id IN({user_ids});""",
    )

    if not response:
        return {"message": "invalid user_ids"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE user_id IN(${user_input});</code>`""",
            "api_endpoint": "`/mysql/in/int?user_ids=${user_input}`",
        },
    },
    "postgresql": {
        "where-int": {
            "database_name": "PostgreSQL",
            "badge": "WHERE-INT",
            "placeholder": "user_id -> 1",
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
            "backend": '''@postgresql_router.get("/where/int")
async def postgresql_where_int(user_id: str):
    response = await asyncio.to_thread(
        run_postgresql,
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
WHERE user_id = ${user_input};</code>`""",
            "api_endpoint": "`/postgresql/where/int?user_id=${user_input}`",
        },
        "where-string": {
            "database_name": "PostgreSQL",
            "badge": "WHERE-STRING",
            "placeholder": "username -> christinajohnson",
            "SQL": """SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE username = 'christinajohnson';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 27
}""",
            "backend": '''@postgresql_router.get("/where/string")
async def postgresql_where_string(username: str):
    response = await asyncio.to_thread(
        run_postgresql,
        SQL=f"""SELECT user_id, username, firstname, 
        lastname, email, role, age 
        FROM Users 
        WHERE username='{username}';""",
    )

    if not response:
        return {"message": "invalid username"}

    if response[0]["role"] == "admin":
        return {"message": "unauthorized action"}

    return response[0]''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE username = '${user_input}';</code>`""",
            "api_endpoint": "`/postgresql/where/string?username=${user_input}`",
        },
        "like-string": {
            "database_name": "PostgreSQL",
            "badge": "LIKE-STRING",
            "placeholder": "username -> 'christinajohnson'",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE username LIKE '%christinajohnson%';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@postgresql_router.get("/like/string")
async def postgresql_like_string(username: str):
    response = await asyncio.to_thread(
        run_postgresql,
        SQL=f"""SELECT user_id, username, firstname, lastname, email, role, age FROM Users WHERE username LIKE '%{username}%';""",
    )

    if not response:
        return {"message": "invalid username"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE username LIKE '%${user_input}%';</code>`""",
            "api_endpoint": "`/postgresql/like/string?username=${user_input}`",
        },
        "order-by-int": {
            "database_name": "PostgreSQL",
            "badge": "ORDER-BY-INT",
            "placeholder": "index -> 1",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY 1;""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@postgresql.get("/order-by/int")
async def postgresql_order_by_int(index: str):
    response = await asyncio.to_thread(
        run_postgresql,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        ORDER BY {index};""",
    )

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY ${user_input};</code>`""",
            "api_endpoint": "`/postgresql/order-by/int?index=${user_input}`",
        },
        "order-by-string": {
            "database_name": "PostgreSQL",
            "badge": "ORDER-BY-STRING",
            "placeholder": "field_name -> firstname",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY firstname;""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@postgresql_router.get("/order-by/string")
async def postgresql_order_by_string(field_name: str):
    response = await asyncio.to_thread(
        run_postgresql,
        SQL=f"""SELECT user_id, username, firstname, 
        lastname, email, role, age 
        FROM Users 
        ORDER BY {field_name};""",
    )

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users ORDER BY ${user_input};</code>`""",
            "api_endpoint": "`/postgresql/order-by/string?field_name=${user_input}`",
        },
        "in-int": {
            "database_name": "PostgreSQL",
            "badge": "IN-INT",
            "placeholder": "user_ids -> 1,2,3",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE user_id IN(1,2,3);""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@postgresql_router.get("/in/int")
async def postgresql_in_int(user_ids: str):
    response = await asyncio.to_thread(
        run_postgresql,
        SQL=f"""SELECT user_id, username, firstname, 
        lastname, email, role, age 
        FROM Users 
        WHERE user_id IN({user_ids});""",
    )

    if not response:
        return {"message": "invalid user_ids"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE user_id IN(${user_input});</code>`""",
            "api_endpoint": "`/postgresql/in/int?user_ids=${user_input}`",
        },
    },
    "mssql": {
        "where-int": {
            "database_name": "MSSQL",
            "badge": "WHERE-INT",
            "placeholder": "user_id -> 1",
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
            "backend": '''@mssql_router.get("/where/int")
async def mssql_where_int(user_id: str):
    response = await asyncio.to_thread(
        run_mssql,
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
WHERE user_id = ${user_input};</code>`""",
            "api_endpoint": "`/mssql/where/int?user_id=${user_input}`",
        },
        "where-string": {
            "database_name": "MSSQL",
            "badge": "WHERE-STRING",
            "placeholder": "username -> christinajohnson",
            "SQL": """SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE username = 'christinajohnson';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 27
}""",
            "backend": '''@mssql_router.get("/where/string")
async def mssql_where_string(username: str):
    response = await asyncio.to_thread(
        run_mssql,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        WHERE username='{username}';""",
    )

    if not response:
        return {"message": "invalid username"}

    if response[0]["role"] == "admin":
        return {"message": "unauthorized action"}

    return response[0]''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE username = '${user_input}';</code>`""",
            "api_endpoint": "`/mssql/where/string?username=${user_input}`",
        },
        "like-int": {
            "database_name": "MSSQL",
            "badge": "LIKE-INT",
            "placeholder": "age -> 18",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE age LIKE '%18%';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": '''@mssql_router.get("/like/int")
async def mssql_like_int(age: str):
    response = await asyncio.to_thread(
        run_mssql,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        WHERE age LIKE '%{age}%';""",
    )

    if not response:
        return {"message": "invalid age"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE age LIKE '%${user_input}%';</code>`""",
            "api_endpoint": "`/mssql/like/int?age=${user_input}`",
        },
        "like-string": {
            "database_name": "MSSQL",
            "badge": "LIKE-STRING",
            "placeholder": "username -> 'christinajohnson'",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE username LIKE '%christinajohnson%';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@mssql_router.get("/like/string")
async def mssql_like_string(username: str):
    response = await asyncio.to_thread(
        run_mssql,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        WHERE username LIKE '%{username}%';""",
    )

    if not response:
        return {"message": "invalid username"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE username LIKE '%${user_input}%';</code>`""",
            "api_endpoint": "`/mssql/like/string?username=${user_input}`",
        },
        "order-by-int": {
            "database_name": "MSSQL",
            "badge": "ORDER-BY-INT",
            "placeholder": "index -> 1",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY 1;""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@mssql_router.get("/order-by/int")
async def mssql_order_by_int(index: str):
    response = await asyncio.to_thread(
        run_mssql,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        ORDER BY {index};""",
    )

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY ${user_input};</code>`""",
            "api_endpoint": "`/mssql/order-by/int?index=${user_input}`",
        },
        "order-by-string": {
            "database_name": "MSSQL",
            "badge": "ORDER-BY-STRING",
            "placeholder": "field_name -> firstname",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY firstname;""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@mssql_router.get("/order-by/string")
async def mssql_order_by_string(field_name: str):
    response = await asyncio.to_thread(
        run_mssql,
        SQL=f"""SELECT user_id, username, firstname, 
        lastname, email, role, age 
        FROM Users 
        ORDER BY {field_name};""",
    )

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users ORDER BY ${user_input};</code>`""",
            "api_endpoint": "`/mssql/order-by/string?field_name=${user_input}`",
        },
        "in-int": {
            "database_name": "MSSQL",
            "badge": "IN-INT",
            "placeholder": "user_ids -> 1,2,3",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE user_id IN(1,2,3);""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@mssql_router.get("/in/int")
async def mssql_in_int(user_ids: str):
    response = await asyncio.to_thread(
        run_mssql,
        SQL=f"""SELECT user_id, username, firstname, 
        lastname, email, role, age 
        FROM Users 
        WHERE user_id IN({user_ids});""",
    )

    if not response:
        return {"message": "invalid user_ids"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE user_id IN(${user_input});</code>`""",
            "api_endpoint": "`/mssql/in/int?user_ids=${user_input}`",
        },
    },
    "oracle": {
        "where-int": {
            "database_name": "ORACLE",
            "badge": "WHERE-INT",
            "placeholder": "user_id -> 1",
            "SQL": """SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE user_id = 1""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 27
}""",
            "backend": '''@oracle_router.get("/where/int")
async def oracle_where_int(user_id: str):
    response = await asyncio.to_thread(
        run_oracle,
        SQL=f"""SELECT user_id, username, firstname,
        lastname, email, role, age
        FROM Users
        WHERE user_id={user_id}""",
    )
    
    if not response:
        return {"message": "invalid user_id"}
    
    if response[0]["role"] == "admin":
        return {"message": "unauthorized action"}
    
    return response[0]''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE user_id = ${user_input}</code>`""",
            "api_endpoint": "`/oracle/where/int?user_id=${user_input}`",
        },
        "where-string": {
            "database_name": "ORACLE",
            "badge": "WHERE-STRING",
            "placeholder": "username -> christinajohnson",
            "SQL": """SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE username = 'christinajohnson';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 27
}""",
            "backend": '''@oracle_router.get("/where/string")
async def oracle_where_string(username: str):
    response = await asyncio.to_thread(
        run_oracle,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        WHERE username='{username}'""",
    )

    if not response:
        return {"message": "invalid username"}

    if response[0]["role"] == "admin":
        return {"message": "unauthorized action"}

    return response[0]''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age
FROM Users
WHERE username = '${user_input}';</code>`""",
            "api_endpoint": "`/oracle/where/string?username=${user_input}`",
        },
        "like-int": {
            "database_name": "ORACLE",
            "badge": "LIKE-INT",
            "placeholder": "age -> 18",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE age LIKE '%18%';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": '''@oracle_router.get("/like/int")
async def oracle_like_int(age: str):
    response = await asyncio.to_thread(
        run_oracle,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        WHERE age LIKE '%{age}%';""",
    )

    if not response:
        return {"message": "invalid age"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE age LIKE '%${user_input}%';</code>`""",
            "api_endpoint": "`/oracle/like/int?age=${user_input}`",
        },
        "like-string": {
            "database_name": "ORACLE",
            "badge": "LIKE-STRING",
            "placeholder": "username -> 'christinajohnson'",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE username LIKE '%christinajohnson%';""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@oracle_router.get("/like/string")
async def oracle_like_string(username: str):
    response = await asyncio.to_thread(
        run_oracle,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        WHERE username LIKE '%{username}%';""",
    )

    if not response:
        return {"message": "invalid username"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE username LIKE '%${user_input}%';</code>`""",
            "api_endpoint": "`/oracle/like/string?username=${user_input}`",
        },
        "order-by-int": {
            "database_name": "ORACLE",
            "badge": "ORDER-BY-INT",
            "placeholder": "index -> 1",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY 1;""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@oracle_router.get("/order-by/int")
async def oracle_order_by_int(index: str):
    response = await asyncio.to_thread(
        run_oracle,
        SQL=f"""SELECT user_id, username, firstname, lastname, 
        email, role, age 
        FROM Users 
        ORDER BY {index};""",
    )

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY ${user_input};</code>`""",
            "api_endpoint": "`/oracle/order-by/int?index=${user_input}`",
        },
        "order-by-string": {
            "database_name": "ORACLE",
            "badge": "ORDER-BY-STRING",
            "placeholder": "field_name -> firstname",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
ORDER BY firstname;""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@oracle_router.get("/order-by/string")
async def oracle_order_by_string(field_name: str):
    response = await asyncio.to_thread(
        run_oracle,
        SQL=f"""SELECT user_id, username, firstname, 
        lastname, email, role, age 
        FROM Users 
        ORDER BY {field_name};""",
    )

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users ORDER BY ${user_input};</code>`""",
            "api_endpoint": "`/oracle/order-by/string?field_name=${user_input}`",
        },
        "in-int": {
            "database_name": "ORACLE",
            "badge": "IN-INT",
            "placeholder": "user_ids -> 1,2,3",
            "SQL": r"""SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE user_id IN(1,2,3);""",
            "json_response": """{
    "user_id": 1,
    "username": "christinajohnson",
    "firstname": "Matthew",
    "lastname": "Marshall",
    "email": "qortiz@example.org",
    "role": "customer",
    "age": 18
}""",
            "backend": r'''@oracle_router.get("/in/int")
async def oracle_in_int(user_ids: str):
    response = await asyncio.to_thread(
        run_oracle,
        SQL=f"""SELECT user_id, username, firstname, 
        lastname, email, role, age 
        FROM Users 
        WHERE user_id IN({user_ids});""",
    )

    if not response:
        return {"message": "invalid user_ids"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response''',
            "users_table_content": [],
            "sql_update": """`<code id="sql" class="language-sql">SELECT user_id, username, firstname, lastname, email, role, age 
FROM Users 
WHERE user_id IN(${user_input});</code>`""",
            "api_endpoint": "`/oracle/in/int?user_ids=${user_input}`",
        },
    },
}
