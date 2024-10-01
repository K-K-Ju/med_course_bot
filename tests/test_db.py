import pytest
import redis

from bot.models import LessonDAO, ApplyDAO
from bot.admin.db_driver import AdminDb
from bot.db_driver import LessonDb, ApplyDb
from bot.static.states import ApplyState

con_pool = redis.ConnectionPool(db=1)
r = redis.StrictRedis(db=1)
ad_db = AdminDb(_connection_pool_=con_pool)
l_db = LessonDb(_connection_pool_=con_pool)
apply_db = ApplyDb(_connection_pool_=con_pool)


@pytest.fixture()
def data_lesson_dao():
    return LessonDAO('Test lesson',
                     '20.09.2024 11:30', '1000', 'Some test description')


@pytest.fixture()
def data_apply_dao():
    return ApplyDAO('123456789', 'lesson:0', ApplyState.NEW)


def test_add_lesson(data_lesson_dao):
    idx = 'lesson:' + (r.get('lesson_id_gen')).decode('utf-8')
    length_before = r.json().arrlen('bot:lessons', '$.lessons')[0]
    l_db.add(data_lesson_dao)
    length_after = r.json().arrlen('bot:lessons', '$.lessons')[0]

    assert length_after - length_before == 1
    assert l_db.get(idx) is not None

    r.json().delete('bot:lessons', f'$.lessons[?(@.id=="{idx}")]')


def test_add_apply(data_apply_dao):
    idx = 'apply:' + (r.get('apply_id_gen')).decode('utf-8')
    length_before = r.json().arrlen('bot:applies', '$.applies')[0]
    apply_db.add(data_apply_dao)
    length_after = r.json().arrlen('bot:applies', '$.applies')[0]

    assert length_after - length_before == 1
    assert apply_db.get(idx) is not None

    r.json().delete('bot:applies', f'$.applies[?(@.id=="{idx}")]')
