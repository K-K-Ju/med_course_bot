import json

from bot.models import Res, Ok, Error
import redis


def init_redis_pool(redis_host, redis_port):
    return redis.ConnectionPool(db=1, host=redis_host, port=redis_port)


def run_query(query) -> Res:
    res = query()
    if res:
        return Ok(res)
    else:
        return Error('No records were found')


def prepare_db(redis_pool):
    r = redis.StrictRedis(connection_pool=redis_pool)
    docs = {'bot:users:clients': [{'id': 0}],
            'bot:users:admins': [],
            'bot:lessons': [],
            'bot:applies': []}

    for doc_name, doc_struct in docs.items():
        r.json().set(doc_name, '$', json.dumps(doc_struct), nx=True)

    print('Testing database...')
    test_key, test_value = 'test_key', 100
    r.set(test_key, format(test_value, 'b'))
    res = int(r.get(test_key), 2)
    assert res == test_value
    r.delete(test_key)
    print('Finished testing database')
    r.close()
