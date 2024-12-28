import logging
import sqlite3
from sqlite3 import Connection
from typing import Callable

from bot.models.res import Ok, Error, Res

logger = logging.getLogger('main_logger')

def run_sql(con: Connection, query: Callable) -> Res:
    try:
        with con:
            query()
            return Ok()
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
        
            FOREIGN KEY (client_id) REFERENCES clients (id),
            FOREIGN KEY (lesson_id) REFERENCES lessons (id)
        );
        """

        cur.execute(script)
        cur.close()
        con.commit()
