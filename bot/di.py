import logging
import os

from dependency_injector import containers, providers
from redis.asyncio import Redis
from sqlalchemy import create_engine, QueuePool
from typing import AsyncIterator

from bot.db.admin_db import AdminDb
from bot.db.apply_db import ApplyDb
from bot.db.client_db import ClientsDb
from bot.config import app_config, RedisConfig, AppConfig, LoggerConfig
from bot.db.lesson_db import LessonDb

sqlite_engine = create_engine(
    f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__package__)), app_config.db_file)}',
    poolclass=QueuePool, pool_size=20, max_overflow=10)


def get_sqlite_con():
    con = sqlite_engine.connect()
    logging.debug('Returning Sqlite connection')
    yield con
    con.close()


async def init_redis_pool(redis_config: RedisConfig) -> AsyncIterator[Redis]:
    """
    Returns iterator with two iterations, first - returns Redis pool instance,
    second - closes this pool

    :param redis_config:
    :return: async iterator
    """

    redis = Redis(  # type: ignore
        host=redis_config.host,
        port=redis_config.port,
        username=redis_config.username,
        password=redis_config.password,
        decode_responses=redis_config.decode_responses,
        ssl=redis_config.ssl,
        ssl_cert_reqs=redis_config.ssl_cert_reqs,
        retry_on_error=redis_config.retry_on_error,
        health_check_interval=redis_config.health_check_interval,
    )
    logging.debug("Redis pool initialized")
    yield redis
    await redis.close()
    logging.debug("Redis pool closed")


class ConfigsContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["bot.di", "bot.main"]
    )

    logger_config = providers.Singleton(LoggerConfig)
    redis_config = providers.Singleton(RedisConfig)
    app_config = providers.Singleton(AppConfig)


class DbContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=['bot.client.db_driver', 'bot.admin.db_driver', 'bot.db_driver']
    )

    redis_config = providers.Container(ConfigsContainer).container.redis_config

    redis_con = providers.Resource(init_redis_pool, redis_config=redis_config)
    sqlite_con = providers.Resource(get_sqlite_con)

    admin_db = providers.Factory(AdminDb, connection=sqlite_con)
    clients_db = providers.Factory(ClientsDb, connection=sqlite_con)
    lessons_db = providers.Factory(LessonDb, connection=sqlite_con)
    applies_db = providers.Factory(ApplyDb, connection=sqlite_con)
