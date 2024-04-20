import mysql.connector
import psycopg
import oracledb
import pymssql
from .config import creds
from psycopg.rows import dict_row


def run_mysql(SQL, is_fetch: bool = True, params=None):
    try:
        conn = mysql.connector.connect(
            host=creds.MYSQL_HOSTNAME,
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
            host=creds.POSTGRESQL_HOSTNAME,
            user=creds.POSTGRES_USERNAME,
            password=creds.POSTGRES_PASSWORD,
            dbname=creds.POSTGRES_DB,
            port=creds.POSTGRES_PORT,
            row_factory=dict_row,
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


def run_oracle(SQL, is_fetch=True, params=None):
    try:
        conn = oracledb.connect(
            user=creds.ORACLE_USERNAME,
            password=creds.ORACLE_PASSWORD,
            dsn=f"{creds.ORACLE_HOSTNAME}/{creds.ORACLE_DATABASE}",
            mode=oracledb.SYSDBA,
        )
        cursor = conn.cursor()

        if params:
            cursor.executemany(SQL, params)
        else:
            cursor.execute(SQL)

        if is_fetch:
            cursor.rowfactory = lambda *args: dict(
                zip([d[0].lower() for d in cursor.description], args)
            )
            result = cursor.fetchall()
            return result
        else:
            conn.commit()

    except oracledb.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()


def run_mssql(SQL, is_fetch=True, params=None):
    try:
        conn = pymssql.connect(
            creds.MSSQL_HOSTNAME,
            creds.MSSQL_USERNAME,
            creds.MSSQL_SA_PASSWORD,
            creds.MSSQL_DATABASE,
        )
        cursor = conn.cursor(as_dict=True)

        if params:
            cursor.executemany(SQL, params)
        else:
            cursor.execute(SQL)

        if is_fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()

    except pymssql.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
