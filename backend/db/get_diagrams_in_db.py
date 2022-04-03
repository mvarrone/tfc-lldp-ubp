import json
import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log


def db_connection(db_name):
    load_dotenv()
    path = os.getenv(db_name)
    return sqlite3.connect(path)


def get_prev_diagrams(dict_fastapi):
    conn = db_connection('DB_PATH_EXTRAS')

    c = conn.cursor()

    new_value = c.execute(
        "SELECT date FROM extrasinfo;").fetchall()

    conn.close()

    headers = ["date"]
    resultado = []
    for _, elem in enumerate(new_value):
        resultado.append(dict(zip(headers, list(elem))))

    write_to_log(dict_fastapi)

    return resultado[::-1]


def get_prev_diagram_info_in_db(id, dict_fastapi):
    conn = db_connection('DB_PATH_EXTRAS')

    c = conn.cursor()

    value = c.execute(
        "SELECT nodes, edges FROM extrasinfo WHERE id=:id",
        {
            'id': id
        }).fetchall()

    conn.close()

    for _, elem in enumerate(value):
        res = [json.loads(idx.replace("'", '"')) for idx in elem]

    nodes, edges = res[0], res[1]

    data = {
        "nodes": nodes,
        "edges": edges
    }

    write_to_log(dict_fastapi)
    return data
