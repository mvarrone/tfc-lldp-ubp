import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log, write_to_log_modify


def get_credentials(hostname_selected):
    """Get password and secret values for a certain hostname

    c.execute() return 3 values: hostname, password and secret

    hostname = c.execute(...)[0][0] (Not used, that is why the _ symbol)

    password = c.execute(...)[0][1]

    secret = c.execute(...)[0][2]
    """
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    _, password, secret = c.execute(
        "SELECT host, password, secret FROM credentials where HOST = ?",
        (hostname_selected,)).fetchall()[0]

    conn.close()

    return password, secret


def modify_data_db(hostname_selected, device, dict_fastapi):
    print("\nEjecutando desde modify_data_db\n")

    password, secret = get_credentials(hostname_selected)

    if len(device["password"]) == 0:
        device["password"] = password

    if len(device["secret"]) == 0:
        device["secret"] = secret

    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute("""
    UPDATE credentials
    SET device_type = :device_type,
        host = :host,
        port = :port, 
        username = :username,
        password = :password,
        secret = :secret,
        conn_timeout = :conn_timeout
    WHERE host = ?""",
              (
                  device["device_type"],
                  device["hostname"],
                  device["port"],
                  device["username"],
                  device["password"],
                  device["secret"],
                  device["conn_timeout"],
                  hostname_selected
              )
              )

    conn.commit()

    conn.close()

    if hostname_selected == device["hostname"]:
        print("\nSe modificó " + hostname_selected)
        write_to_log_modify(dict_fastapi)
    else:
        msg = "Se ha modificado hostname de " + \
            hostname_selected + " a " + str(device["hostname"])
        print("\n" + msg)
        write_to_log_modify(dict_fastapi, msg)


def mod_dev_val(value, dict_fastapi):
    load_dotenv()
    path = os.getenv('DB_PATH_DEVICES')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    new_value = c.execute(
        "SELECT device_type, host, port, username, conn_timeout FROM credentials;").fetchall()

    headers = ["device_type", "host", "port",
               "username", "conn_timeout"]
    resultado = []
    for idx, elem in enumerate(new_value):
        resultado.append(dict(zip(headers, list(elem))))

    for idx, elem in enumerate(resultado):
        if elem["host"] == value["hostname"]:
            valor_encontrado = resultado[idx]

    conn.close()

    write_to_log(dict_fastapi)

    return valor_encontrado
