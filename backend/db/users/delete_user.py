import os
import sqlite3

from dotenv import load_dotenv

# from log.log_function import write_to_log_special_users_db


def get_usernames_registered_in_db():
    load_dotenv()
    path = os.getenv('DB_PATH_USERS')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    username_availables = c.execute(
        "SELECT username FROM infousers;").fetchall()

    conn.close()

    column = ["username"]
    resultado = []
    for _, elem in enumerate(username_availables):
        resultado.append(dict(zip(column, list(elem))))

    lista_1 = []
    for user in resultado:
        lista_1.append(user["username"])
    return lista_1


def delete_user_from_db(user_to_be_deleted):
    lista_usuarios = get_usernames_registered_in_db()
    if user_to_be_deleted not in lista_usuarios:
        return "\nNo se encontró el usuario " + user_to_be_deleted + " en users.db\n"

    load_dotenv()
    path = os.getenv('DB_PATH_USERS')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute("DELETE from infousers WHERE username = :username",
              {
                  'username': user_to_be_deleted,
              }
              )

    conn.commit()
    conn.close()
    # write_to_log_special_users_db(str(user_to_be_deleted))
    return "\nSe borró " + user_to_be_deleted + " de users.db\n"


user_to_be_deleted = "admin"


if __name__ == "__main__":
    print(delete_user_from_db(user_to_be_deleted))
