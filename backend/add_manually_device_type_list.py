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


def add_device_type_in_list(device_type_list):
    lista_device_type = get_device_types_registered_in_db()

    counter = 0
    accumulator = []
    for _, element in enumerate(device_type_list):
        if element in lista_device_type:
            counter += 1
            accumulator.append(element)

    if counter > 0:
        return "\n" + str(counter) + " device type already found in db:\n\n" + \
            str([accumulator[i] for i in range(len(accumulator))]) + "\n" + \
            "\nDelete repeated ones and try again\n"

    load_dotenv()
    path = os.getenv('DB_PATH_DEVICE_TYPES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    # Order list alphabetically
    device_type_list = sorted(device_type_list)

    counter_registered = 0
    accumulator_registered = []
    for devtype in device_type_list:
        c.execute(
            "INSERT INTO info VALUES (:device_type)",
            {
                'device_type': devtype,
            }
        )
        counter_registered += 1
        accumulator_registered.append(devtype)

        write_to_log_special_add_device_type(devtype)

    conn.commit()

    conn.close()

    return "\n" + str(counter_registered) + " device type registered successfully:\n\n" + \
        str([accumulator_registered[i]
            for i in range(len(accumulator_registered))]) + "\n"


device_type_list = [
    "juniper_junos",
    "huawei_vrp",
    "hp_procurve",
    "hp_comware",
    "cisco_xr",
    "cisco_s300",
    "cisco_nxos",
    "cisco_ios",
    "brocade_netiron",
    "brocade_fastiron",
    "broadcom_icos",
    "aruba_aoscx",
    "arista_eos"
]


if __name__ == "__main__":
    print(add_device_type_in_list(device_type_list))
