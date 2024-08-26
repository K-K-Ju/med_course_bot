import sqlite3
import logging

from bot.models.AppUser import AppUser

logger = logging.getLogger('main_logger')

logger.info('Connecting to database...')
con = sqlite3.connect("../clients.db")
cur = con.cursor()
logger.info('Connection to db established')


def prepare_db():
    logger.info('Preparing database...')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT UNIQUE NOT NULL,
            username TEXT,
            chat_id BIGINT NOT NULL,
            registered BOOLEAN DEFAULT FALSE,
            state SMALLINT NOT NULL DEFAULT 0
        );
    ''')
    logger.info('Finished preparing database')


def add_client(user_id, username, chat_id):
    logger.debug(f'Adding {user_id=}')
    cur.execute('INSERT INTO users (user_id, username, chat_id, state) VALUES (?, ?, ?, ?)',
                (user_id, username, chat_id, 0))
    logger.debug(f'End adding user {user_id}')


def get_user(user_id) -> AppUser:
    logger.debug(f'Retrieving user by {user_id=}')
    cur.execute(f'SELECT * FROM users WHERE user_id={user_id}')
    row = cur.fetchone()
    logger.debug(f'End of retrieving user by {user_id=}')

    return AppUser(row[0], row[1], row[2], row[3])


def user_exists(user_id):
    logger.debug(f'Checking whether user exists - {user_id}')
    cur.execute(f'SELECT COUNT(user_id) FROM users WHERE user_id={user_id}')
    res = cur.fetchone()
    if res[0] == 1:
        return True
    else:
        return False
