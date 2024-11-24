from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import Field


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8', case_sensitive=False)

    admin_key: str = Field('admin_key', validate_default=False)
    api_hash: str = Field('api_hash', validate_default=False)
    api_id: int = Field('api_id', validate_default=False)
    bot_token: str = Field('bot_token', validate_default=False)
    log_lvl: str = Field('log_lvl', validate_default=False)
    log_file_path: str = Field('log_file_path', validate_default=False)
    redis_host: str = Field('redis_host', validate_default=False)
    redis_port: int = Field('redis_port', validate_default=False,)

app_config = AppConfig()
