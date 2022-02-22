from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
# Algorithm
# Expiration Time Token

# openssl rand -hex 32
SECRET_KEY = "c9f96d3261cd3bcb35ea38aabab584b6687f0bf7ece81b0b7c5127c31cbd7caf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
