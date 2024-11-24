from dependency_injector import containers, providers


from bot.admin.db_driver import AdminDb
from bot.config import app_config
from bot.db_driver import LessonDb, ApplyDb
from bot.user.db_driver import ClientsDb
from bot.utils import init_redis_pool



class DbContainer(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(modules=[bot.user.db_driver, bot.admin.db_driver, bot.db_driver])
    redis_pool = providers.Singleton(init_redis_pool, app_config.redis_host, app_config.redis_port)
    # redis_pool = providers.Dependency()
    admin_db = providers.Factory(AdminDb, connection_pool=redis_pool)
    clients_db = providers.Factory(ClientsDb, connection_pool=redis_pool)
    lessons_db = providers.Factory(LessonDb, connection_pool=redis_pool)
    applies_db = providers.Factory(ApplyDb, connection_pool=redis_pool)


# class AppContainer(containers.DeclarativeContainer):
#
#     db_container = providers.Container(DbContainer, redis_pool=redis_pool)
