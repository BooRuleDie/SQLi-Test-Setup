from fastapi import APIRouter
from ..app.database import run_mysql
import asyncio

mysql_router = APIRouter(prefix="/mysql", tags=["MySQL"])


@mysql_router.get("/where/int")
async def mysql_where_int(user_id: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, email, role, age FROM Users WHERE user_id={user_id};""",
    )

    if not response:
        return {"message": "invalid user_id"}

    if response[0]["role"] == "admin":
        return {"message": "unauthorized action"}

    return response[0]


@mysql_router.get("/where/string")
async def mysql_where_string(username: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, email, role, age FROM Users WHERE username='{username}';""",
    )

    if not response:
        return {"message": "invalid username"}

    if response[0]["role"] == "admin":
        return {"message": "unauthorized action"}

    return response[0]


@mysql_router.get("/like/int")
async def mysql_like_int(age: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, email, role, age FROM Users WHERE age LIKE '%{age}%';""",
    )

    if not response:
        return {"message": "invalid age"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response


@mysql_router.get("/like/string")
async def mysql_like_string(username: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, email, role, age FROM Users WHERE username LIKE '%{username}%';""",
    )

    if not response:
        return {"message": "invalid username"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response


@mysql_router.get("/order-by/int")
async def mysql_order_by_int(index: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, email, role, age FROM Users ORDER BY {index};""",
    )

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response


@mysql_router.get("/order-by/string")
async def mysql_order_by_string(field_name: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, email, role, age FROM Users ORDER BY {field_name};""",
    )

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response


@mysql_router.get("/in/int")
async def mysql_in_int(user_ids: str):
    response = await asyncio.to_thread(
        run_mysql,
        SQL=f"""SELECT user_id, username, firstname, lastname, email, role, age FROM Users WHERE user_id IN({user_ids});""",
    )

    if not response:
        return {"message": "invalid user_ids"}

    for index, user in enumerate(response):
        if user["role"] == "admin":
            del response[index]

    return response
