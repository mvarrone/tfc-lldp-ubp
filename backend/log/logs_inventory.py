import os
import sqlite3

from dotenv import load_dotenv

from log.log_function import write_to_log


def show_log(dict_fastapi):
    write_to_log(dict_fastapi)

    load_dotenv()
    path = os.getenv('DB_PATH_LOGS')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    new_value = c.execute(
        "SELECT * FROM information;").fetchall()

    conn.close()

    headers = [
        "date", "hour", "ip",
        "method", "path", "scheme",
        "error_type", "error_descr"
    ]

    variable = []
    for _, elem in enumerate(new_value):
        variable.append(dict(zip(headers, list(elem))))

    # return variable
    return variable[::-1]


# def show_log_example(dict_fastapi):
#     write_to_log(dict_fastapi)
#     return [
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
