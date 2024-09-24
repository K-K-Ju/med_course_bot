from . import user
from . import admin
import redis

redis_pool = redis.ConnectionPool(db=1)
redis_pool_lessons = None
