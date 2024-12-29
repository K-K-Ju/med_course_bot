from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import Field
from redis.asyncio.retry import Retry


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
    log_file_path: str = Field('LOG_FILE', validate_default=False)


class RedisConfig(BaseSettingsEntity):
    host: str = Field(alias="REDIS_HOST", default="localhost")
    port: int = Field(alias="REDIS_PORT", default=6379)

    username: str | None = Field(alias="REDIS_USER", default=None)
    password: str | None = Field(alias="REDIS_PASSWORD", default=None)

    decode_responses: bool = True
    retry: Retry | None = None

    ssl: bool = Field(alias="REDIS_SSL", default=False)
    ssl_cert_reqs: str = "none"

    retry_on_error: list = [ConnectionError, TimeoutError]

    health_check_interval: int = 30

    db: int = 0
