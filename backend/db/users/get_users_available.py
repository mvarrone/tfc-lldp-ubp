import os
import sqlite3

from dotenv import load_dotenv


def get_hardcoded_users():
    fake_users_db = {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
        },
        "admin": {
            "username": "admin",
            "full_name": "Administrator",
            "email": "mativarrone2@gmail.com",
            "hashed_password": "$2b$12$SyTqEYFV6vHuFJMuPRpeL.LS/ah3e9mTi6vY.IDIO8bb73F7rSEsS",
            "disabled": False,
        }
    }
    return fake_users_db


def get_users_from_db():
    load_dotenv()
    path = os.getenv('DB_PATH_USERS')
    conn = sqlite3.connect(path)

    c = conn.cursor()

    new_value = c.execute(
        "SELECT username, fullname, email, hashedpassword, disabled FROM infousers;").fetchall()

    nested_dict = {}
    for _, elem in enumerate(new_value):
        nested_dict[elem[0]] = {}
        nested_dict[elem[0]]["username"] = elem[0]
        nested_dict[elem[0]]["full_name"] = elem[1]
        nested_dict[elem[0]]["email"] = elem[2]
        nested_dict[elem[0]]["hashed_password"] = elem[3]
        nested_dict[elem[0]]["disabled"] = elem[4]

    # print("\n--- nested_dict ---")
    # print(nested_dict)
    # print(len(nested_dict))

    conn.close()

    # write_to_log(dict_fastapi)

    return nested_dict, len(nested_dict)
