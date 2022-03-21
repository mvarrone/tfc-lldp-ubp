import datetime
import os
import sqlite3

from dotenv import load_dotenv


def write_no_devices_in_db(dict_fastapi, info_error, error_descr):
    print("\nEjecutando desde write_no_devices_in_db()")
    # print(dict_fastapi)
    # print(info_error)
    # print(error_descr)

    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\logs.db"
    load_dotenv()
    path = os.getenv('DB_PATH_LOGS')
    conn = sqlite3.connect(path)

    date = datetime.datetime.now()
    fecha = "%d/%b/%Y"
    hora = "%H:%M:%S"
    fecha_str = date.strftime(fecha)
    hora_str = date.strftime(hora)

    c = conn.cursor()

    c.execute("INSERT INTO information VALUES (:date, :hour, :ip, :method, :path, :scheme, :error_type, :error_descr)",
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
    # print(dict_fastapi)
    # print(info_error)
    # print(error_descr)

    lista_a_str = ' '.join(map(str, info_error["devices_errored_descr"]))
    lista_a_str = error_descr + ":\n" + lista_a_str

    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\logs.db"
    load_dotenv()
    path = os.getenv('DB_PATH_LOGS')
    conn = sqlite3.connect(path)

    date = datetime.datetime.now()
    fecha = "%d/%b/%Y"
    hora = "%H:%M:%S"
    fecha_str = date.strftime(fecha)
    hora_str = date.strftime(hora)

    c = conn.cursor()

    c.execute("INSERT INTO information VALUES (:date, :hour, :ip, :method, :path, :scheme, :error_type, :error_descr)",
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
    # print(dict_fastapi)
    # print(info_error)
    # print(error_descr)

    lista_a_str = ' '.join(map(str, info_error["devices_errored_descr"]))
    lista_a_str = error_descr + ":\n" + lista_a_str

    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\logs.db"
    load_dotenv()
    path = os.getenv('DB_PATH_LOGS')
    conn = sqlite3.connect(path)

    date = datetime.datetime.now()
    fecha = "%d/%b/%Y"
    hora = "%H:%M:%S"
    fecha_str = date.strftime(fecha)
    hora_str = date.strftime(hora)

    c = conn.cursor()

    c.execute("INSERT INTO information VALUES (:date, :hour, :ip, :method, :path, :scheme, :error_type, :error_descr)",
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
