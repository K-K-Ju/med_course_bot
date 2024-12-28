from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import Field


class BaseSettingsEntity(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8', case_sensitive=False)


class AppConfig(BaseSettingsEntity):
    admin_key: str = Field(alias='ADMIN_KEY')
    api_hash: str = Field(alias='API_HASH')
    api_id: int = Field(alias='API_ID')
    bot_token: str = Field(alias='BOT_TOKEN')
    db_file: str = Field(alias='DB_FILE')


class LoggerConfig(BaseSettingsEntity):
    log_lvl: str = Field('LOG_LVL', validate_default=False)
    log_file_path: str = Field('log_file_path', validate_default=False)


app_config = AppConfig()
