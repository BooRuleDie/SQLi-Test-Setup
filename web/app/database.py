import mysql.connector
import psycopg
from .config import creds
from psycopg.rows import dict_row


def run_mysql(SQL, is_fetch: bool = True, params=None):
    try:
        conn = mysql.connector.connect(
            host=creds.HOST,
            user=creds.MYSQL_USERNAME,
            password=creds.MYSQL_ROOT_PASSWORD,
            database=creds.MYSQL_DATABASE,
        )

        cursor = conn.cursor(dictionary=True)
        if params:
            cursor.executemany(SQL, params)
        else:
            cursor.execute(SQL)

        if is_fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()


def run_postgresql(SQL, is_fetch: bool = True, params=None):
    try:
        conn = psycopg.connect(
            host=creds.HOST,
            user=creds.POSTGRES_USERNAME,
            password=creds.POSTGRES_PASSWORD,
            dbname=creds.POSTGRES_DB,
            port=creds.POSTGRES_PORT,
            row_factory=dict_row
        )

        cursor = conn.cursor()
        if params:
            cursor.executemany(SQL, params)
        else:
            cursor.execute(SQL)

        if is_fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()

    except psycopg.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
