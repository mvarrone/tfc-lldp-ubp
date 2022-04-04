import datetime
import os

from db.log_sqlite import (write_all_down, write_at_least_one,
                           write_no_devices_in_db)
from dotenv import load_dotenv


def get_time():
    date = datetime.datetime.now()
    fecha = "%d/%b/%Y"
    hora = "%H:%M:%S"
    return date.strftime(fecha + " - " + hora)


def write_to_log_just_root(dict_fastapi):
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " +
                str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " +
                str(dict_fastapi["scheme"]).upper() + "\n")


def write_to_log(dict_fastapi):
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " +
                str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " +
                str(dict_fastapi["scheme"]).upper() + " username=" + str(dict_fastapi["username"]) + "\n")


def write_to_log_special_add(dict_fastapi, device_type):
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " +
                str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " +
                str(device_type) + " " +
                str(dict_fastapi["scheme"]).upper() + " username=" + str(dict_fastapi["username"]) + "\n")


def write_to_log_modify(dict_fastapi, msg=None):
    localtime = get_time()

    if msg:
        text = str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " + \
            str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " - " + msg + " " + \
            str(dict_fastapi["scheme"]).upper() + \
            " username=" + str(dict_fastapi["username"]) + "\n"
    else:
        text = str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " + \
            str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " + \
            str(dict_fastapi["scheme"]).upper() + \
            " username=" + str(dict_fastapi["username"]) + "\n"

    with open('log/log.txt', 'a') as f:
        f.write(text)


def write_to_log_special_delete(dict_fastapi):
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " +
                str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " +
                str(dict_fastapi["scheme"]).upper() + " username=" + str(dict_fastapi["username"]) + "\n")


def write_to_log_special_db(dict_fastapi, path):
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " +
                str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " +
                str(dict_fastapi["scheme"]).upper() +
                " - Base de datos no encontrada. Se ha creado una en " + str(path) + "\n")


def write_to_log_special_add_device_type(dev_type):
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - " +
                "Se ha agregado el siguiente device_type: " + str(dev_type) + "\n")


def write_to_log_error_diagram(dict_fastapi, info_error):
    localtime = get_time()

    text = str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " + \
        str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " + \
        str(dict_fastapi["scheme"]).upper() + "\n" + " " * 2 + \
        str(info_error["error"]) + " - " + \
        str(info_error["time"]) + " " + str(info_error["unit"]) + "\n"

    load_dotenv()
    # path = "D:\\Documentos\\Mati\\tfc\\frontend\\src\\assets\\error_log.txt"
    path = os.getenv('LOG_PATH')
    # dirs = [path, 'log/error_log.txt']
    dirs = ['log/error_log.txt']
    for dir in dirs:
        with open(dir, 'a') as f:
            f.write(text)
            cont = 0
            for elem in info_error["devices_errored"]:
                text2 = " " * 4 + str(elem) + "\n"
                f.write(text2)
                text3 = " " * 6 + \
                    str(info_error["devices_errored_descr"][cont]) + "\n\n"
                f.write(text3)
                cont = cont + 1

    error_descr = "No se pudo conectar a ningún dispositivo"
    write_all_down(dict_fastapi, info_error, error_descr)


def write_to_log_error_diagram_no_devices(dict_fastapi, info_error):
    localtime = get_time()

    error_descr = "No devices present in database. Please, add devices and try again"

    text = str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " + \
        str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " + \
        str(dict_fastapi["scheme"]).upper() + "\n" + " " * 2 + \
        str(info_error["error"]) + " - " + \
        str(info_error["time"]) + " " + str(info_error["unit"]) + "\n" + " " * 4 + \
        error_descr + "\n\n"

    load_dotenv()
    # path = "D:\\Documentos\\Mati\\tfc\\frontend\\src\\assets\\error_log.txt"
    path = os.getenv('LOG_PATH')
    dirs = [path, 'log/error_log.txt']
    for dir in dirs:
        with open(dir, 'a') as f:
            f.write(text)
    write_no_devices_in_db(dict_fastapi, info_error, error_descr)


def write_to_log_error_diagram_at_least_one(dict_fastapi, info_error):
    localtime = get_time()

    if info_error["cant_errores"] == 1:
        error_descr = "Hubo 1 error"
    else:
        error_descr = "Hubo " + str(info_error["cant_errores"]) + " errores"

    text = str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " + \
        str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " + \
        str(dict_fastapi["scheme"]).upper() + "\n" + " " * 2 + \
        str(info_error["error"]) + " - " + \
        str(info_error["time"]) + " " + str(info_error["unit"]) + "\n" + \
        " " * 4 + error_descr + "\n"

    load_dotenv()
    # path = "D:\\Documentos\\Mati\\tfc\\frontend\\src\\assets\\error_log.txt"
    path = os.getenv('LOG_PATH')
    dirs = [path, 'log/error_log.txt']
    for dir in dirs:
        with open(dir, 'a') as f:
            f.write(text)
            cont = 0
            for elem in info_error["devices_errored"]:
                text2 = " " * 6 + str(elem) + "\n"
                f.write(text2)
                text3 = " " * 8 + \
                    str(info_error["devices_errored_descr"][cont]) + "\n\n"
                f.write(text3)
                cont = cont + 1

    write_at_least_one(dict_fastapi, info_error, error_descr)


def write_to_log_section_dashboard(dict_fastapi):
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " +
                str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " +
                str(dict_fastapi["scheme"]).upper() + " username=" + str(dict_fastapi["username"]) + "\n")


def write_to_log_section_logout(dict_fastapi):
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " +
                str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " +
                str(dict_fastapi["scheme"]).upper() + " username=" + str(dict_fastapi["username"]) + "\n")


def write_to_log_special_users_db(username):
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - " + str(username) +
                " has been added to db (users.db)\n")


def write_to_log_history(id, full_date, dict_fastapi):
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - " + str(dict_fastapi["host"]) + ":" + str(dict_fastapi["port"]) + " - " +
                str(dict_fastapi["method"]) + " " + str(dict_fastapi["path"]) + " " +
                "Added to history database with id: " + str(id) + " date: " + str(full_date) + " " +
                str(dict_fastapi["scheme"]).upper() + " username=" + str(dict_fastapi["username"]) + "\n")


def write_to_log_on_startup():
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - Backend server started\n")


def write_to_log_on_shutdown():
    localtime = get_time()

    with open('log/log.txt', 'a') as f:
        f.write(str(localtime) + " - Backend server stopped\n")
