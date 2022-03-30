from pydantic import BaseModel


class AddDevice(BaseModel):
    device_type: str
    hostname: str
    port: int
    username: str
    password: str
    secret: str
    conn_timeout: int


class UpdateDevice(AddDevice):
    pass


class DeleteDevice(BaseModel):
    hostname: str
