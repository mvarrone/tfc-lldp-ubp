import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log_special_add_device_type


def get_device_types_registered_in_db():
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICE_TYPES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    device_type_availables = c.execute(
        "SELECT device_type FROM info;").fetchall()

    conn.close()

    column = ["device_type"]
    resultado = []
    for _, elem in enumerate(device_type_availables):
        resultado.append(dict(zip(column, list(elem))))

    lista_1 = []
    for dev_type in resultado:
        lista_1.append(dev_type["device_type"])

    return lista_1


def add_device_types_db(device_type_to_be_added):
    lista_device_type = get_device_types_registered_in_db()
    if device_type_to_be_added in lista_device_type:
        return "\nEl device_type " + device_type_to_be_added + " ya se encuentra registrado en device_types.db\n"

    load_dotenv()
    path = os.getenv('DB_PATH_DEVICE_TYPES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute(
        "INSERT INTO info VALUES (:device_type)",
        {
            'device_type': device_type_to_be_added,
        }
    )

    conn.commit()

    conn.close()

    write_to_log_special_add_device_type(device_type_to_be_added)

    return "\nSe agregó " + str(device_type_to_be_added) + " a la base de datos device_types.db\n"


device_type_to_be_added = "fortigate_os"

if __name__ == "__main__":
    print(add_device_types_db(device_type_to_be_added))
