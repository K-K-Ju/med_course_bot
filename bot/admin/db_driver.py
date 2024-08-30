import logging
import redis


__r_admin__ = redis.Redis(db=2)


def user_is_admin(user_id):
    if __r_admin__.exists(user_id) > 0:
        return True
    else:
        return False