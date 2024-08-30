import logging
import redis
import re

from bot.models import AppUser
from bot.static.states import State

logger = logging.getLogger('main_logger')

logger.info('Connecting to database...')
__r__ = redis.Redis(db=1)

logger.info('Connection to db established')


def test_db():
    logger.info('Testing database...')
    test_key, test_value = 'test_key', 100
    __r__.set(test_key, format(test_value, 'b'))
    res = int(__r__.get(test_key), 2)
    assert res == test_value
    __r__.delete(test_key)
    logger.info('Finished testing database')


def add_user(app_user: AppUser):
    logger.debug(f'Adding {app_user.user_id=}')
    __r__.hset(app_user.user_id, mapping={
            'username': app_user.user_name,
            'chat_id': app_user.chat_id,
            'name': app_user.name,
            'phone_number': app_user.phone_number,
            'state': format(app_user.state.value, 'b')
    })
    logger.debug(f'End adding user {app_user.user_id=}')


def get_users_with_state(state: State):
    cursor = '0'
    pattern = re.compile(format(state.value, 'b'))
    filtered_data = {}
    ids = __r__.scan()

    for i in ids:
        while cursor != 0:
            cursor, data = __r__.hscan(i, cursor=cursor)
            for k, v in data.items():
                if pattern.match(v.decode('utf-8')):
                    filtered_data[k.decode('utf-8')] = v.decode('utf-8')

    return filtered_data


def get_user(user_id) -> AppUser:
    logger.debug(f'Retrieving user by {user_id=}')
    user_dict = __r__.hgetall(user_id)
    logger.debug(f'End of retrieving user by {user_id=}')

    return AppUser .from_redis_dict(user_dict)


def set_user_state(user_id, state: State):
    __r__.hset(user_id, 'state', format(state.value, 'b'))


def user_exists(user_id):
    logger.debug(f'Checking whether user exists - {user_id}')
    num = __r__.exists(user_id)
    if num == 1:
        return True
    else:
        return False
