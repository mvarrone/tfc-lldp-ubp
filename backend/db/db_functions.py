import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log_special_db


def create_db():
    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\devices.db"
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute("""CREATE TABLE credentials (
        device_type TEXT,
        host TEXT,
        port INTEGER,
        username TEXT,
        password TEXT,
        secret TEXT,
        conn_timeout INTEGER
        )""")

    conn.commit()

    conn.close()


def check_db(dict_fastapi):
    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\devices.db"
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    db_exists = os.path.isfile(path)
    if not(db_exists):
        print("\nNo se encontró la base de datos llamada devices.db")
        create_db()
        print("\nBase de datos devices.db creada en " + str(path) + "\n")
        write_to_log_special_db(dict_fastapi, path)

    return db_exists


def create_db_table_device_types():
    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\device_types.db"
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICE_TYPES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute("""CREATE TABLE info (
        device_type TEXT
        )""")

    conn.commit()

    conn.close()


def check_db_table_device_types(dict_fastapi):
    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\device_types.db"
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICE_TYPES')
    db_exists = os.path.isfile(path)
    if not(db_exists):
        print("\nNo se encontró la base de datos llamada device_types.db")
        create_db_table_device_types()
        print("\nBase de datos device_types.db creada en " + str(path) + "\n")
        write_to_log_special_db(dict_fastapi, path)

    return db_exists


def create_db_for_logs():
    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\logs.db"
    load_dotenv()
    path = os.getenv('DB_PATH_LOGS')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute("""CREATE TABLE information (
        date TEXT,
        hour TEXT,
        ip TEXT,
        method TEXT,
        path TEXT,
        scheme TEXT,
        error_type TEXT,
        error_descr TEXT
        )""")

    conn.commit()

    conn.close()


def check_db_for_logs(dict_fastapi):
    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\logs.db"
    load_dotenv()
    path = os.getenv('DB_PATH_LOGS')
    db_exists = os.path.isfile(path)
    if not(db_exists):
        print("\nNo se encontró la base de datos llamada logs.db")
        create_db_for_logs()
        print("\nBase de datos logs.db creada en " + str(path) + "\n")
        write_to_log_special_db(dict_fastapi, path)
    return db_exists


def create_db_for_users():
    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\users\\users.db"
    load_dotenv()
    path = os.getenv('DB_PATH_USERS')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute("""CREATE TABLE infousers (
        username TEXT,
        fullname TEXT,
        email TEXT,
        hashedpassword TEXT,
        disabled TEXT
        )""")

    conn.commit()

    conn.close()


def check_db_for_users(dict_fastapi):
    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\users\\users.db"
    load_dotenv()
    path = os.getenv('DB_PATH_USERS')
    db_exists = os.path.isfile(path)
    if not(db_exists):
        print("\nNo se encontró la base de datos llamada users.db")
        create_db_for_users()
        print("\nBase de datos users.db creada en " + str(path) + "\n")
        write_to_log_special_db(dict_fastapi, path)
    return db_exists
