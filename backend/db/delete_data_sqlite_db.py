import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log, write_to_log_special_delete


def delete_data_db(hostname, dict_fastapi):
    print("\nEjecutando desde delete_data_db\n")

    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\devices.db"
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute("DELETE from credentials WHERE host = :host",
              {
                  'host': hostname
              }
              )

    conn.commit()

    conn.close()

    print("\nSe eliminó " + hostname)

    write_to_log_special_delete(dict_fastapi)


def hostname_list_data_db(dict_fastapi):
    # print("\nEjecutando desde hostname_list_data_db\n")

    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\devices.db"
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    # print("\n--- Datos (sòlo hostnames)")
    # print("\nSELECT host FROM credentials;")

    # print("\nnew_value ---")
    new_value = c.execute(
        "SELECT host FROM credentials;").fetchall()
    # print(new_value)

    headers = ["host"]
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
