import datetime
import os
import sqlite3

from dotenv import load_dotenv


def write_no_devices_in_db(dict_fastapi, info_error, error_descr):
    load_dotenv()
    path = os.getenv('DB_PATH_LOGS')
    conn = sqlite3.connect(path)

    date = datetime.datetime.now()
    fecha_str = date.strftime("%d/%b/%Y")
    hora_str = date.strftime("%H:%M:%S")

    c = conn.cursor()

    c.execute(
        "INSERT INTO information \
            VALUES \
                (:date, :hour, :ip, :method, :path, :scheme, :error_type, :error_descr)",
        {
            'date': str(fecha_str),
            'hour': str(hora_str),
            'ip': dict_fastapi["host"],
            'method': dict_fastapi["method"],
            'path': dict_fastapi["path"],
            'scheme': dict_fastapi["scheme"],
            'error_type': info_error["error"],
            "error_descr": error_descr
        }
    )

    print("\nSe agregaron datos a la base de datos logs.db (write_no_devices_in_db)")

    conn.commit()
    conn.close()


def write_at_least_one(dict_fastapi, info_error, error_descr):
    print("\nEjecutando desde write_at_least_one()")

    lista_a_str = ' '.join(map(str, info_error["devices_errored_descr"]))
    lista_a_str = error_descr + ":\n" + lista_a_str

    load_dotenv()
    path = os.getenv('DB_PATH_LOGS')
    conn = sqlite3.connect(path)

    date = datetime.datetime.now()
    fecha_str = date.strftime("%d/%b/%Y")
    hora_str = date.strftime("%H:%M:%S")

    c = conn.cursor()

    c.execute(
        "INSERT INTO information VALUES (:date, :hour, :ip, :method, :path, :scheme, :error_type, :error_descr)",
        {
            'date': str(fecha_str),
            'hour': str(hora_str),
            'ip': dict_fastapi["host"],
            'method': dict_fastapi["method"],
            'path': dict_fastapi["path"],
            'scheme': dict_fastapi["scheme"],
            'error_type': info_error["error"],
            "error_descr": lista_a_str
        }
    )

    print("\nSe agregaron datos a la base de datos logs.db (write_at_least_one)")

    conn.commit()
    conn.close()


def write_all_down(dict_fastapi, info_error, error_descr):
    print("\nEjecutando desde write_all_down()")

    lista_a_str = ' '.join(map(str, info_error["devices_errored_descr"]))
    lista_a_str = error_descr + ":\n" + lista_a_str

    load_dotenv()
    path = os.getenv('DB_PATH_LOGS')
    conn = sqlite3.connect(path)
    c = conn.cursor()

    date = datetime.datetime.now()
    fecha_str = date.strftime("%d/%b/%Y")
    hora_str = date.strftime("%H:%M:%S")

    c.execute(
        "INSERT INTO information VALUES (:date, :hour, :ip, :method, :path, :scheme, :error_type, :error_descr)",
        {
            'date': str(fecha_str),
            'hour': str(hora_str),
            'ip': dict_fastapi["host"],
            'method': dict_fastapi["method"],
            'path': dict_fastapi["path"],
            'scheme': dict_fastapi["scheme"],
            'error_type': info_error["error"],
            "error_descr": lista_a_str
        }
    )

    print("\nSe agregaron datos a la base de datos logs.db (write_all_down)")

    conn.commit()
    conn.close()
