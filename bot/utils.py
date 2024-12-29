import logging
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Callable, Any, Optional, Dict

from bot.models.res import Res, Ok, Error

logger = logging.getLogger('main_logger')


def get_single_dict_by_sql(con: Connection, query: Callable[[], Cursor]) -> Optional[Dict[str, Any]]:
    res = run_sql(con, query)
    if res is Ok and (d := res.val.fetchone()):
        return d
    return None


def run_sql(con: Connection, query: Callable[[], Cursor]) -> Res[
    Cursor, sqlite3.OperationalError | sqlite3.IntegrityError]:
    try:
        with con:
            return Ok(query())
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as pe:
        logger.error(pe)
        return Error(f"Cannot execute query -- {query}")


def prepare_db(con):
    with con:
        cur = con.cursor()

        script = """
        CREATE TABLE IF NOT EXISTS clients
        (
            id           VARCHAR(100) PRIMARY KEY,
            username     VARCHAR(50) NOT NULL,
            name         VARCHAR(50),
            phone_number VARCHAR(20),
            state        INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS receipts
        (
            message_id VARCHAR(100) PRIMARY KEY,
            client_id  VARCHAR(100) NOT NULL,
        
            FOREIGN KEY (client_id) REFERENCES clients (id)
        );
        
        CREATE TABLE IF NOT EXISTS admins
        (
            client_id VARCHAR(100),
            state     INTEGER NOT NULL,
        
            FOREIGN KEY (client_id) REFERENCES clients (id)
        );
        
        CREATE TABLE IF NOT EXISTS lessons
        (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       VARCHAR(255) NOT NULL,
            datetime    TIMESTAMP    NOT NULL,
            price       INTEGER      NOT NULL,
            description VARCHAR(255) NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS applies
        (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER      NOT NULL,
            client_id VARCHAR(100) NOT NULL,
            state     INTEGER DEFAULT (0),
        
            FOREIGN KEY (client_id) REFERENCES clients (id),
            FOREIGN KEY (lesson_id) REFERENCES lessons (id)
        );
        """

        cur.execute(script)
        cur.close()
        con.commit()
