import logging
import redis

from bot.models.AppUser import AppUser

logger = logging.getLogger('main_logger')

logger.info('Connecting to database...')
r = redis.Redis()
logger.info('Connection to db established')


def prepare_db():
    logger.info('Preparing database...')
    ############
    logger.info('Finished preparing database')


def add_client(app_user: AppUser):
    logger.debug(f'Adding {app_user.user_id=}')
    r.hset(app_user.user_id, mapping={
            'username': app_user.user_name,
            'chat_id': app_user.chat_id,
            'state': 0
    })
    logger.debug(f'End adding user {app_user.user_id=}')


async def get_user(user_id) -> AppUser:
    logger.debug(f'Retrieving user by {user_id=}')
    user_dict = await r.hgetall(user_id)
    logger.debug(f'End of retrieving user by {user_id=}')

    return AppUser.from_dict(user_dict)


async def user_exists(user_id):
    logger.debug(f'Checking whether user exists - {user_id}')
    num = await r.exists(user_id)
    if num == 1:
        return True
    else:
        return False
