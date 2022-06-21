
from pydantic import BaseSettings


class Setting(BaseSettings):
    database_hostname: str
    database_username: str
    database_name: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file='.env'

setting = Setting()

