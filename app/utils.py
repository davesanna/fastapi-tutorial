import json
import os
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_keys():
    with open(os.path.join(os.path.abspath("./"), "keys.json")) as file:
        keys_file = json.load(file)
        username = keys_file["username"]
        password = keys_file["password"]
        host_name = keys_file["host_name"]
        db_name = keys_file["db_name"]

    return username, password, host_name, db_name


def hash(password: str):
    # define default hashing algorithm
    hashed_psw = pwd_context.hash(password)

    return hashed_psw


def verify(plain_psw: str, hashed_psw: str):
    return pwd_context.verify(plain_psw, hashed_psw)
