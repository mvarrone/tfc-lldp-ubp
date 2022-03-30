import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log, write_to_log_special_add


def db_connection(db_name):
    load_dotenv()
    path = os.getenv(db_name)
    return sqlite3.connect(path)


def add_data_db(hostname, creds, dict_fastapi):
    conn = db_connection('DB_PATH_DEVICES')

    c = conn.cursor()

    c.execute(
        "INSERT INTO credentials \
            VALUES (:device_type, :host, :port, :username, :password, :secret, :conn_timeout)",
        {
            'device_type': creds["device_type"],
            'host': creds["hostname"],
            'port': creds["port"],
            'username': creds["username"],
            'password': creds["password"],
            'secret': creds["secret"],
            'conn_timeout': creds["conn_timeout"]
        }
    )

    print("\nSe agregó " + str(hostname))

    conn.commit()

    conn.close()

    write_to_log_special_add(dict_fastapi, creds["device_type"])


def device_type_list_data_db(dict_fastapi):
    conn = db_connection('DB_PATH_DEVICE_TYPES')

    c = conn.cursor()

    new_value = c.execute(
        "SELECT device_type FROM info;").fetchall()

    headers = ["device_type"]
    resultado = []
    for idx, elem in enumerate(new_value):
        resultado.append(dict(zip(headers, list(elem))))

    conn.close()

    write_to_log(dict_fastapi)

    return resultado
