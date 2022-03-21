import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log


def datos_para_netmiko():
    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\devices.db"
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    # print("\nSELECT * FROM credentials;\n")
    value = c.execute("SELECT * FROM credentials;").fetchall()

    # print(value)
    # print(type(value))
    # print(len(value))
    # print("\n---")

    headers = ["device_type", "host", "port",
               "username", "password", "secret",
               "conn_timeout"]
    resultado = []
    for idx, elem in enumerate(value):
        resultado.append(dict(zip(headers, list(elem))))

    # print(resultado)
    # print(type(resultado))
    # print(len(resultado))

    conn.close()

    return resultado


def inventory_data_db(dict_fastapi):
    # print("\nEjecutando desde show_data_db\n")

    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\devices.db"
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    # print("\nSELECT * FROM credentials;\n")
    # value = c.execute("SELECT * FROM credentials;").fetchall()

    # print("\n--- value ---")
    # print(value)
    # print(type(value))
    # print(len(value))

    # print("\nDatos completos (incluyendo password y secret)---")

    # headers = ["device_type", "host", "port",
    #            "username", "password", "secret",
    #            "conn_timeout"]
    # resultado = []
    # for idx, elem in enumerate(value):
    #     resultado.append(dict(zip(headers, list(elem))))

    # print("\n--- resultado ---")
    # print(resultado)
    # print(type(resultado))
    # print(len(resultado))

    # conn.close()

    # write_to_log(dict_fastapi)

    # return resultado

    # print("\n--- Datos incompletos (sin password ni secret) ---")
    # print("\nSELECT device_type, host, port, username, conn_timeout FROM credentials;")

    # print("\nnew_value ---")
    new_value = c.execute(
        "SELECT device_type, host, port, username, conn_timeout FROM credentials;").fetchall()
    # print(new_value)

    headers = ["device_type", "host", "port",
               "username", "conn_timeout"]
    resultado_2 = []
    for idx, elem in enumerate(new_value):
        resultado_2.append(dict(zip(headers, list(elem))))

    # print("\n--- resultado_2 ---")
    # print(resultado_2)
    # print(type(resultado_2))
    # print(len(resultado_2))

    conn.close()

    write_to_log(dict_fastapi)

    return resultado_2
