from bot import redis_pool
from bot.models import Res, Ok, Error
import redis


def run_query(query) -> Res:
    res = query()
    if res:
        return Ok(res)
    else:
        return Error('No records were found')


def prepare_db():
    r = redis.StrictRedis(connection_pool=redis_pool, db=1)
    docs = {'bot:users': '{"users":{"clients":[], "admins":[]}}',
            'bot:lessons': '{"lessons":[]}',
            'bot:applies': '{"applies": []}'}

    for doc_name, doc_struct in docs.items():
        r.json().set(doc_name, '$', doc_struct, nx=True)

    print('Testing database...')
    test_key, test_value = 'test_key', 100
    r.set(test_key, format(test_value, 'b'))
    res = int(r.get(test_key), 2)
    assert res == test_value
    r.delete(test_key)
    print('Finished testing database')
