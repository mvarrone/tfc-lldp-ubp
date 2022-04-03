import datetime
import os
import sqlite3

from dotenv import load_dotenv
from log.log_function import write_to_log_history


def db_connection(db_name):
    load_dotenv()
    path = os.getenv(db_name)
    return sqlite3.connect(path)


def add_history_to_db(last_id, data, dict_fastapi) -> None:
    id = last_id + 1
    date = datetime.datetime.now()
    full_date = date.strftime("%d-%m-%y") + "_" + date.strftime("%H:%M:%S")

    conn = db_connection('DB_PATH_EXTRAS')

    c = conn.cursor()

    c.execute(
        "INSERT INTO extrasinfo \
            VALUES (:id, :date, :nodes, :edges)",
        {
            'id': id,
            'date': full_date,
            'nodes': str(data["nodes"]),
            'edges': str(data["edges"])
        }
    )

    conn.commit()

    conn.close()

    write_to_log_history(id, full_date, dict_fastapi)


def get_latest_id_from_extras_db():
    conn = db_connection('DB_PATH_EXTRAS')

    c = conn.cursor()

    new_value = c.execute(
        "SELECT id FROM extrasinfo;").fetchall()

    conn.close()

    headers = ["id"]
    resultado = []
    for _, elem in enumerate(new_value):
        resultado.append(dict(zip(headers, list(elem))))

    if len(resultado) == 0:
        last_id = 0
        return last_id

    for _, elem in enumerate(resultado):
        last_id = elem["id"]

    # write_to_log(dict_fastapi)
    return last_id
