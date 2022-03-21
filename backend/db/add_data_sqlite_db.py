import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log, write_to_log_special_add


def add_data_db(hostname, creds, dict_fastapi):
    print("\nEjecutando desde add_data_db\n")
    print(creds)
    print(len(creds))
    print(type(creds))
    print("\n")

    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\devices.db"
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute("INSERT INTO credentials VALUES (:device_type, :host, :port, :username, :password, :secret, :conn_timeout)",
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

    # print("\nSe agregó " + str(creds["hostname"]))
    print("\nSe agregó " + str(hostname))

    conn.commit()

    conn.close()

    write_to_log_special_add(dict_fastapi, creds["device_type"])


def device_type_list_data_db(dict_fastapi):
    # print("\nEjecutando desde device_type_list_data_db\n")

    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\device_types.db"
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICE_TYPES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    # print("\n--- Datos (sòlo device_types)")
    # print("\nSELECT device_type FROM info;")

    # print("\nnew_value ---")
    new_value = c.execute(
        "SELECT device_type FROM info;").fetchall()
    # print(new_value)

    headers = ["device_type"]
    resultado = []
    for idx, elem in enumerate(new_value):
        resultado.append(dict(zip(headers, list(elem))))

    # print("\n--- resultado ---")
    # print(resultado)
    # print(type(resultado))
    # print(len(resultado))

    conn.close()

    write_to_log(dict_fastapi)

    return resultado
