import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log_special_add_device_type


def add_device_type_in_list(device_type_list):
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICE_TYPES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    # Ordenar alfabéticamente la lista
    device_type_list = sorted(device_type_list)

    for devtype in device_type_list:
        c.execute("INSERT INTO info VALUES (:device_type)",
                  {
                      'device_type': devtype,
                  }
                  )

        print("\nSe agregó " + str(devtype) +
              " a la base de datos device_types.db")

        write_to_log_special_add_device_type(devtype)

    conn.commit()

    conn.close()


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
