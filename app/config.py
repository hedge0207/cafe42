import os
import json

from pathlib import Path
from typing import List

from pydantic import BaseSettings


PROFILE = os.environ.get("PROFILE", "develop")

def list_parse_fallback(v):
    try:
        return json.loads(v)
    except Exception as e:
        return v.split(",")

class Settings(BaseSettings):
    secret_key: str
    sign_algorithm: str
    token_expire_minutes: int
    db_user: str
    db_password: str
    

    class Config:
        env_file = f'{Path(os.path.dirname(__file__)).parent}/app/{PROFILE}.env'
        env_file_encoding = 'utf-8'
        json_loads = list_parse_fallback
        case_sensitive = False


config = Settings()