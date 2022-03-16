from pydantic import BaseSettings


class Settings(BaseSettings):
    # checks in the environment variables if there are already some with this names (not case sensitive & checks datatype)
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
