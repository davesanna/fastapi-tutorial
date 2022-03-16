from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    # define default hashing algorithm
    hashed_psw = pwd_context.hash(password)

    return hashed_psw


def verify(plain_psw: str, hashed_psw: str):
    return pwd_context.verify(plain_psw, hashed_psw)
