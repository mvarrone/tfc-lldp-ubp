import os
import sqlite3

from dotenv import load_dotenv
from passlib.context import CryptContext

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


def add_user_to_db(new_user):
    lista_usuarios = get_usernames_registered_in_db()
    if new_user["username"] in lista_usuarios:
        return "\nEl usuario " + new_user["username"] + " ya se encuentra registrado en users.db\n"

    load_dotenv()
    path = os.getenv('DB_PATH_USERS')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    c.execute("INSERT INTO infousers VALUES (:username, :full_name, :email, :hashed_password, :disabled)",
              {
                  'username': new_user["username"],
                  'full_name': new_user["full_name"],
                  'email': new_user["email"],
                  'hashed_password': new_user["hashed_password"],
                  'disabled': new_user["disabled"],
              }
              )

    conn.commit()
    conn.close()
    # write_to_log_special_users_db(str(new_user["username"]))
    return "\nSe agregó " + new_user["username"] + " a la base de datos users.db\n"


def create_hash(password):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)


new_user = {
    "username": "mvarrone",
    "full_name": "Matias Varrone",
    "email": "mativarrone2@gmail.com",
    "hashed_password": create_hash("ubp1234"),
    "disabled": "False",
}

# new_user = {
#     "username": "dtrump",
#     "full_name": "Donald Trump",
#     "email": "dtrump@gmail.com",
#     "hashed_password": create_hash("donald123"),
#     "disabled": "False",
# }

# new_user = {
#     "username": "admin",
#     "full_name": "Admin Account",
#     "email": "thisisadminaccount@gmail.com",
#     "hashed_password": create_hash("admin123"),
#     "disabled": "False",
# }


if __name__ == "__main__":
    print(add_user_to_db(new_user))
