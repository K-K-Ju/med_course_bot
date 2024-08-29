import logging
import redis

from bot.models.AppUser import AppUser
from bot.static.states import State

logger = logging.getLogger('main_logger')

logger.info('Connecting to database...')
r = redis.Redis(db=1)
r_admin = redis.Redis(db=2)
logger.info('Connection to db established')


def test_db():
    logger.info('Testing database...')
    test_key, test_value = 'test_key', 100
    r.set(test_key, format(test_value, 'b'))
    res = int(r.get(test_key), 2)
    assert res == test_value
    r.delete(test_key)
    logger.info('Finished testing database')


def add_user(app_user: AppUser):
    logger.debug(f'Adding {app_user.user_id=}')
    r.hset(app_user.user_id, mapping={
            'username': app_user.user_name,
            'chat_id': app_user.chat_id,
            'name': app_user.name,
            'phone_number': app_user.phone_number,
            'state': format(app_user.state, 'b')
    })
    logger.debug(f'End adding user {app_user.user_id=}')


def get_user(user_id) -> AppUser:
    logger.debug(f'Retrieving user by {user_id=}')
    user_dict = r.hgetall(user_id)
    logger.debug(f'End of retrieving user by {user_id=}')

    return AppUser.from_redis_dict(user_dict)


def set_user_state(user_id, state: State):
    r.hset(user_id, 'state', format(state.value, 'b'))


def user_exists(user_id):
    logger.debug(f'Checking whether user exists - {user_id}')
    num = r.exists(user_id)
    if num == 1:
        return True
    else:
        return False


def user_is_admin(user_id):
    if r_admin.exists(user_id) > 0:
        return True
    else:
        return False
