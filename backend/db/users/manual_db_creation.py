import os
import sqlite3

from dotenv import load_dotenv
# from log.log_function import write_to_log_special_db


def db_connection(db_name):
    load_dotenv()
    path = os.getenv(db_name)
    return sqlite3.connect(path)


def create_db_for_users():
    print("aca en create_db_for_users")
    conn = db_connection('DB_PATH_USERS')

    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE infousers (
        username TEXT,
        fullname TEXT,
        email TEXT,
        hashedpassword TEXT,
        disabled TEXT,
        admin_permissions INTEGER
        )""")

    conn.commit()

    conn.close()


def check_db_for_users():
    load_dotenv()
    path = os.getenv('DB_PATH_USERS')
    db_exists = os.path.isfile(path)
    if not(db_exists):
        print("\nNo se encontró la base de datos llamada users.db")
        create_db_for_users()
        print("\nBase de datos users.db creada en " + str(path) + "\n")
        # write_to_log_special_db(dict_fastapi, path)
    return db_exists


if __name__ == "__main__":
    check_db_for_users()
