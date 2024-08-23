from enum import Enum
from pyrogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton)


class Responses:
    START = "Start command message"
    INFO = "Here will be main info about Bot"


class MenuOptions:
    STATUS = 'Show status'
    FAQ = 'Get FAQ'
    APPLY = 'Apply for lesson'


class ReplyKeyboards:
    class QuestionsOptions:
        ABOUT_SCHOOL = 'Про школу'
        WHO_SUITS = 'Кому підійде'
        MONEY = 'Оплата'

    class AboutSchoolOptions:
        WHO_WE_ARE = 'Хто ми і заради чого зібр'
        BENEFITS = 'Opt1'
        HOW = 'Opt2'

    QUESTIONS = ReplyKeyboardMarkup([
        [KeyboardButton(QuestionsOptions.ABOUT_SCHOOL)],
        [KeyboardButton(QuestionsOptions.WHO_SUITS)],
        [KeyboardButton(QuestionsOptions.MONEY)],
    ], is_persistent=True,
        placeholder='Оберіть розділ питань',
        resize_keyboard=True,
        one_time_keyboard=False)

    ABOUT_SCHOOL = ReplyKeyboardMarkup([
        [KeyboardButton(AboutSchoolOptions.WHO_WE_ARE)],
        [KeyboardButton(AboutSchoolOptions.HOW)],
        [KeyboardButton(AboutSchoolOptions.BENEFITS)],
    ], is_persistent=True,
        placeholder='Choose option in menu',
        resize_keyboard=True,
        one_time_keyboard=False)


