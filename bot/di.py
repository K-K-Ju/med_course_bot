import logging
import os

from dependency_injector import containers, providers
from sqlalchemy import create_engine, QueuePool

from bot.db.admin_db import AdminDb
from bot.db.apply_db import ApplyDb
from bot.db.client_db import ClientsDb
from bot.config import app_config
from bot.db.lesson_db import LessonDb

sqlite_engine = create_engine(f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__package__)), app_config.db_file)}',
                      poolclass=QueuePool, pool_size=20, max_overflow=10)

def get_connection():
    con = sqlite_engine.connect()
    logging.debug('Returning Sqlite connection')
    yield con
    con.close()


class DbContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=['bot.client.db_driver', 'bot.admin.db_driver', 'bot.db_driver']
    )

    sqlite_connection = providers.Resource(sqlite_engine.connect)
    admin_db = providers.Factory(AdminDb, connection=sqlite_connection)
    clients_db = providers.Factory(ClientsDb, connection=sqlite_connection)
    lessons_db = providers.Factory(LessonDb, connection=sqlite_connection)
    applies_db = providers.Factory(ApplyDb, connection=sqlite_connection)


# class AppContainer(containers.DeclarativeContainer):
#
#     db_container = providers.Container(DbContainer, redis_pool=redis_pool)
