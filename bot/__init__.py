import logging
from logging import Formatter
from logger import CustomFormatter
from bot.models import AppClient

import config
import db_driver as db


def prepare_logger(level):
    log = logging.getLogger('main_logger')
    log.setLevel(level)
    fmtr = CustomFormatter()
    ch = logging.StreamHandler()
    fh = logging.FileHandler(filename='../medSchoolBot.log', mode='a+', encoding='utf-8')

    ch.setLevel(level)
    fh.setLevel(level)

    ch.setFormatter(fmtr)
    fh.setFormatter(Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"))

    log.addHandler(ch)
    log.addHandler(fh)

    log.info('Logger configured...')


prepare_logger(logging.DEBUG)

config.init_config('C:\\Users\\tusen\\Developing\\Python\\med_course_bot\\secrets.json')
db.test_db()
AppClient(name="Surgeon Course Bot", lang='ua')

import admin
import main

