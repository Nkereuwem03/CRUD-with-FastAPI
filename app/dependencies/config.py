from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
    class Config:
        env_file='.env'
        
@lru_cache
def get_settings():
    return Settings()