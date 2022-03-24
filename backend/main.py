import json
import os
import random
import time
from datetime import datetime, timedelta

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from db.users.get_users_available import get_hardcoded_users, get_users_from_db
# from my_code import get_diagram
# from get_process_info import get_diagram
# from diagram.get_process_info import get_diagram # REAL
from diagram.get_process_info import get_diagram_example  # PRUEBA
from my_code import (about_function, bd_add_device, bd_delete_device,
                     bd_modify_device, bd_modify_device_values,
                     bd_show_device_type_list, bd_show_hostname_list,
                     bd_show_inventory, bd_show_logs, dashboard_function,
                     logout_function, welcome_function)
from various.helper_functions_for_app import api_tags

load_dotenv()
# SECRET_KEY: to get a string like this run: openssl rand -hex 32
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

# fake_users_db = get_hardcoded_users() # users hardcoded for testing purposes
# print(fake_users_db)

fake_users_db, qusers = get_users_from_db()  # users from db
# print("\n", json.dumps(fake_users_db, indent=2))
# print("\nUsuarios en la base de datos: " + str(qusers) + "\n")


class Token(BaseModel):
    access_token: str
    token_type: str
    # exp_arg: str = None


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

description = """
API endpoints for LLDP project
---

---

**Contact**

Author: Matías José Varrone

Email: mativarrone2@gmail.com

---
Feb 2022
"""

tags_metadata = api_tags()

app = FastAPI(
    title="FastAPI Documentation",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
    license_info={
        "name": "nginx 1.21.6",
        "url": "https://nginx.org/LICENSE",
    },
    docs_url="/documentation",
    redoc_url="/redocumentation",
    # openapi_url=None
    # Inhabilitar https://www.lldp.duckdns.org:8000/documentation y https://www.lldp.duckdns.org:8000/redocumentation
    # usando 1) openapi_url=None
    # o sino 2) docs_url=None y redoc_url=None
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    exp_arg = expire - timedelta(minutes=60*3)  # -180 min == -3 hs
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM), exp_arg


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception_expired = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Signature has expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    credentials_exception_not_enough_segments = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough segments",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # print("try section: username")
        # print(username)
        if username is None:
            # print("A-Here")
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        # print("except JWTError section: B-Here")
        # print(e)
        # print(len(e.args))
        # print(type(e.args[0]))
        if e.args[0] == "Signature has expired.":
            # print("Signature has expired.")
            raise credentials_exception_expired
        if "Not enough segments" in str(e.args[0]):
            # print("E-Here-Not enough segments")
            raise credentials_exception_not_enough_segments
        else:
            # print("D-Here")
            raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    # print("normal section: user")
    # print(user)
    if user is None:
        # print("C-Here")
        raise credentials_exception
    # print(user.username)
    global usuario
    usuario = user.username
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@ app.post("/token", response_model=Token, tags=["Login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, exp_arg = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        # "exp_arg": str(exp_arg)
    }


@ app.get("/users/me/", response_model=User, tags=["Login"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@ app.get("/users/me/items/", tags=["Login"])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@ app.get("/", tags=["Root"])
async def root(request: Request):
    """
    Used when click on Home tab -->
    File: Home.vue, Section: mounted()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    return welcome_function(dict_fastapi)


@ app.get("/diagram", tags=["Diagram"])
def diagram(request: Request, current_user: User = Depends(get_current_active_user)):
    """
    Used when click on Diagram tab -->
    File: components/NetworkDiagram.vue, Section: mounted()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    # time.sleep(random.randint(1, 6))
    return get_diagram_example(dict_fastapi)
    # variable = get_diagram(dict_fastapi)
    # # print("\nDentro de @app.get("/diagram")")
    # # print(variable)
    # if variable["error"] == "all_down":
    #     raise HTTPException(status_code=500,
    #                         detail="No se pudo conectar a ningún dispositivo. Revisar Logs")
    # elif variable["error"] == "no_devices_in_db":
    #     raise HTTPException(status_code=500,
    #                         detail="No hay dispositivos cargados en la base de datos. Revisar Logs")
    # return variable


@ app.get("/device_type_list", tags=["Lists"])
async def get_device_type_list(request: Request, current_user: User = Depends(get_current_active_user)):
    """
    Used when click on Add Tab -->
    File: AddDevice.vue, Section: mounted()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    return bd_show_device_type_list(dict_fastapi)

# @app.get("/logs/", include_in_schema=False)


@ app.get("/logs", tags=["Logs"])
async def get_logs(request: Request, current_user: User = Depends(get_current_active_user)):
    """
    Used when click on Logs tab -->
    File: Logs.vue, Section: mounted()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    return bd_show_logs(dict_fastapi)


class AddDevice(BaseModel):
    device_type: str
    hostname: str
    port: int
    username: str
    password: str
    secret: str
    conn_timeout: int


@ app.post("/add_device/{hostname}", status_code=201, tags=["Devices"])
async def add_device(hostname: str, request: Request, post: AddDevice, current_user: User = Depends(get_current_active_user)):
    """
    Used when click on Add Button on Add Tab -->
    File: AddDevice.vue, Section: method: add_device_button()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    bd_add_device(hostname, post.dict(), dict_fastapi)
    return {"Info": "Success"}


class UpdateDevice(BaseModel):
    device_type: str
    hostname: str
    port: int
    username: str
    password: str
    secret: str
    conn_timeout: int


@ app.put("/modify_device/{hostname}", tags=["Devices"])
async def modify_device(hostname: str, request: Request, post: UpdateDevice, current_user: User = Depends(get_current_active_user)):
    """
    Used when click on Modify Button on Modify Tab -->
    File: ModifyDevice.vue, Section: method: modify_device_button()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    bd_modify_device(hostname, post.dict(), dict_fastapi)


class DeleteDevice(BaseModel):
    hostname: str


@ app.delete("/delete_device/{hostname}", response_model=DeleteDevice, tags=["Devices"])
async def delete_device(hostname: str, request: Request, current_user: User = Depends(get_current_active_user)):
    """
    Used when click on Delete Button on Delete Tab -->
    File: DeleteDevice.vue, Section: method: delete_device_button()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    bd_delete_device(hostname, dict_fastapi)


@ app.get("/hostname_list", tags=["Lists"])
async def get_hostname_list(request: Request, current_user: User = Depends(get_current_active_user)):
    """
    Used when click on Delete Tab -->
    File: DeleteDevice.vue, Section: mounted()

    Also, after Delete button on Delete Tab is pressed -->
    File: DeleteDevice.vue, Section: method: update_info_after_button_clicked()

    Also, after Modify button on Modify Tab is pressed -->
    File: ModifyDevice.vue, Section: method: update_info_after_modify_button_clicked()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    return bd_show_hostname_list(dict_fastapi)


@ app.get("/inventory_list", tags=["Lists"])
async def get_inventory_list(request: Request, current_user: User = Depends(get_current_active_user)):
    """
    Used when click on Inventory Tab -->
    File: Inventory.vue, Section: mounted()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    return bd_show_inventory(dict_fastapi)


@ app.get("/about", tags=["About"])
async def about(request: Request, current_user: User = Depends(get_current_active_user)):
    """
    Used when click on About tab -->
    File: About.vue, Section: mounted()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    return about_function(dict_fastapi)


class ModifyDeviceValues(BaseModel):
    device_type: str
    hostname: str
    port: int
    username: str
    password: str
    secret: str
    conn_timeout: int


@ app.get("/device_values_to_modify/{hostname}", tags=["Lists"])
async def get_device_values_to_modify(hostname: str, request: Request, current_user: User = Depends(get_current_active_user)):
    """
    Used when click on an item from selectable list on Modify Tab -->
    File: ModifyDevice.vue, Section: method: switchSelect(event)

    Also, update_info_after_modify_button_clicked uses this endpoint.
    update_info_after_modify_button_clicked is only executed when there are no
    errors when Modify Button is clicked -->
    File: ModifyDevice.vue, Section: method: update_info_after_modify_button_clicked()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port
    }
    # print("\nhostname")
    # print(hostname)
    value = {
        "hostname": hostname
    }
    return bd_modify_device_values(value, dict_fastapi)


@ app.get("/dashboard", tags=["Root"])
async def dashboard(request: Request, current_user: User = Depends(get_current_active_user)):
    """
    Called when user logged in successfully -->
    File: Dashboard.vue, Section: mounted()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port,
        'username': usuario
    }
    return dashboard_function(dict_fastapi)


@ app.get("/logout", tags=["Login"])
async def logout(request: Request, current_user: User = Depends(get_current_active_user)):
    """
    Called when user click in Log out Tab -->
    File: Logout.vue, Section: mounted()
    """
    dict_fastapi = {
        'method': request.method,
        'path': request.url.path,
        'scheme': request.url.scheme,
        'host': request.client.host,
        'port': request.client.port,
        'username': usuario
    }
    return logout_function(dict_fastapi)


if __name__ == "__main__":
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=5000,
                reload=True,
                workers=4,
                ssl_keyfile="./ssl_keys/cert.key",
                ssl_certfile="./ssl_keys/cert.pem"
                )
