import redis

from . import user
from . import admin

redis_pool = redis.ConnectionPool(db=1)
redis_pool_lessons = redis.ConnectionPool(db=2)
