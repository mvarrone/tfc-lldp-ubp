import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log


def datos_para_netmiko():
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    value = c.execute("SELECT * FROM credentials;").fetchall()

    conn.close()

    headers = [
        "device_type", "host", "port",
        "username", "password", "secret",
        "conn_timeout"
    ]
    resultado = []
    for _, elem in enumerate(value):
        resultado.append(dict(zip(headers, list(elem))))

    return resultado


def inventory_data_db(dict_fastapi):
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    new_value = c.execute(
        "SELECT device_type, host, port, username, conn_timeout \
            FROM credentials;").fetchall()

    conn.close()

    headers = [
        "device_type", "host", "port",
        "username", "conn_timeout"
    ]

    resultado = []
    for _, elem in enumerate(new_value):
        resultado.append(dict(zip(headers, list(elem))))

    write_to_log(dict_fastapi)

    return resultado


def inventory_data_db_full_fields(dict_fastapi):
    """
    full fields means include password and secret fields
    This is: device_type, host, port, username, password, secret and conn_timeout
    """
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    value = c.execute("SELECT * FROM credentials;").fetchall()

    conn.close()

    headers = [
        "device_type", "host", "port",
        "username", "password", "secret",
        "conn_timeout"
    ]

    resultado = []
    for _, elem in enumerate(value):
        resultado.append(dict(zip(headers, list(elem))))

    write_to_log(dict_fastapi)

    return resultado
