import os
import sqlite3

from dotenv import load_dotenv

from log.log_function import write_to_log


def show_log(dict_fastapi):
    write_to_log(dict_fastapi)
    # print("\nConseguir datos de log")

    # path = "D:\\Documentos\\Mati\\tfc\\backend\\db\\logs.db"
    load_dotenv()
    path = os.getenv('DB_PATH_LOGS')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    new_value = c.execute(
        "SELECT * FROM information;").fetchall()
    # print(new_value)

    headers = ["date", "hour", "ip",
               "method", "path", "scheme",
               "error_type", "error_descr"]

    variable = []
    for _, elem in enumerate(new_value):
        variable.append(dict(zip(headers, list(elem))))

    # print("\n--- variable ---\n")
    # print(variable)
    # print("\n")
    # print(type(variable))
    # print("\n")
    # print(len(variable))

    # conn.close()
    # return variable

    variable_upside_down = [x for x in variable[::-1]]

    conn.close()
    return variable_upside_down


# def show_log_example(dict_fastapi):
#     write_to_log(dict_fastapi)
#     variable = [
#         {
#             "date": "10/Feb/2022",
#             "hour": "21:00:21",
#             "ip": "181.92.21.206",
#             "method": "GET",
#             "path": "/diagram",
#             "scheme": "HTTPS",
#             "error_type": "all_down",
#             "error_descr": "Este es el contenido del mensaje 1"
#         },
#         {
#             "date": "10/Feb/2022",
#             "hour": "22:50:21",
#             "ip": "181.92.21.206",
#             "method": "PUT",
#             "path": "/about",
#             "scheme": "HTTPS",
#             "error_type": "no_devices_in_db",
#             "error_descr": "Este es el contenido del mensaje 2"
#         }
#     ]
#     return variable
