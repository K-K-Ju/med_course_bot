from pyrogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton)


class Responses:
    START = "Start command message"
    INFO = "Here will be main info about Bot"
    BACK = 'Назад'


class MenuOptions:
    class START_MENU:
        STATUS = 'Show status'
        FAQ = 'Get FAQ'
        APPLY = 'Apply for lesson'
        REGISTER = 'Register'

    class FAQ_OPTIONS:
        ABOUT_SCHOOL = 'Про школу'
        WHO_SUITS = 'Кому підійде'
        MONEY = 'Оплата'

    class ABOUT_SHOOL_OPTIONS:
        WHO_WE_ARE = 'Хто ми і заради чого збір'
        BENEFITS = 'Для чого це Вам?'
        HOW = 'Як ми це плануємо зробити?'

    class WHO_SUITS_OPTIONS:
        WHY = 'Some text'
        LIST = 'Some text 2'


class ReplyKeyboards:
    START = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.START_MENU.STATUS)],
        [KeyboardButton(MenuOptions.START_MENU.APPLY)],
        [KeyboardButton(MenuOptions.START_MENU.FAQ)],
    ], is_persistent=True, placeholder='Choose option in menu', resize_keyboard=False)

    START_NOT_REGISTERED = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.START_MENU.STATUS)],
        [KeyboardButton(MenuOptions.START_MENU.REGISTER)],
        [KeyboardButton(MenuOptions.START_MENU.FAQ)],
    ], is_persistent=True, placeholder='Choose option in menu', resize_keyboard=False)

    FAQ = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.FAQ_OPTIONS.ABOUT_SCHOOL)],
        [KeyboardButton(MenuOptions.FAQ_OPTIONS.WHO_SUITS)],
        [KeyboardButton(MenuOptions.FAQ_OPTIONS.MONEY)],
    ], is_persistent=True,
        placeholder='Оберіть розділ питань',
        resize_keyboard=True,
        one_time_keyboard=False)

    ABOUT_SCHOOL = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.ABOUT_SHOOL_OPTIONS.WHO_WE_ARE)],
        [KeyboardButton(MenuOptions.ABOUT_SHOOL_OPTIONS.HOW)],
        [KeyboardButton(MenuOptions.ABOUT_SHOOL_OPTIONS.BENEFITS)],
    ], is_persistent=True,
        placeholder='Choose option in menu',
        resize_keyboard=True,
        one_time_keyboard=True)

    WHO_SUITS = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.WHO_SUITS_OPTIONS.WHY)],
        [KeyboardButton(MenuOptions.WHO_SUITS_OPTIONS.LIST)],
    ], is_persistent=True,
        placeholder='Choose option in menu',
        resize_keyboard=True,
        one_time_keyboard=True)

    MONEY = ReplyKeyboardMarkup([
        [KeyboardButton('about money 1')],
        [KeyboardButton('about money 2')],
        [KeyboardButton('about money 3')]
    ])


class FAQInfo:
    WHO_WE_ARE = '''Ми молода команда, на чолі якої студенти медичного, економічного університету 
                    та інформаційних технологій. Ми маємо бажання зробити свій внесок в майбутнє 
                    української медицини та допомогти студентам-медикам знайти себе у вирі цієї складної, 
                    надзвичайно конкурентної професії.'''

    BENEFITS = '''Ми певні, якщо Ви студент-медик, то вже зіштовхнулись або чули від старших колег про 
                  брак практичних навичок на парах в університеті. Наші курси по-максимуму наповнені 
                  практикою, що подається після найважливішої теорії по визначеній темі заняття.'''

    HOW = '''Ми підготували для Вас цікаві, практично-орієнтовані тренінги для навчання та 
             відпрацювання навичок з різних хірургічних спеціальностей.'''


states = {
    'LEVEL1': [
        MenuOptions.START_MENU.FAQ,
        MenuOptions.START_MENU.APPLY,
        MenuOptions.START_MENU.STATUS
    ],
    'LEVEL2': [
        MenuOptions.FAQ_OPTIONS.MONEY,
        MenuOptions.FAQ_OPTIONS.WHO_SUITS,
        MenuOptions.FAQ_OPTIONS.ABOUT_SCHOOL
    ],
    'LEVEL3': [
        MenuOptions.ABOUT_SHOOL_OPTIONS.HOW,
        MenuOptions.ABOUT_SHOOL_OPTIONS.BENEFITS,
        MenuOptions.ABOUT_SHOOL_OPTIONS.WHO_WE_ARE,

        MenuOptions.WHO_SUITS_OPTIONS.LIST,
        MenuOptions.WHO_SUITS_OPTIONS.WHY
        # TODO add options
    ],
    'LEVEL4': [
        FAQInfo.HOW,
        FAQInfo.BENEFITS,
        FAQInfo.WHO_WE_ARE
    ]
}


class Level:
    MENU_OPTIONS: dict = None
    KEYBOARDS: dict = None


class Level1(Level):
    MENU_OPTIONS = {
        'STATUS': 'Show status',
        'FAQ': 'Get FAQ',
        'APPLY': 'Apply for lesson'
    }
    KEYBOARDS = {
        'FAQ': ReplyKeyboards.FAQ,
        'ABOUT_SCHOOL': ReplyKeyboards.ABOUT_SCHOOL,
        'WHO_SUITS': ReplyKeyboards.WHO_SUITS
    }


class Level2(Level):
    MENU_OPTIONS = {

    }
    # 'FAQ_OPTIONS': {
    #     'ABOUT_SCHOOL': 'Про школу',
    #     'WHO_SUITS': 'Кому підійде',
    #     'MONEY': 'Оплата'
    # },
    # 'ABOUT_SHOOL_OPTIONS': {
    #     'WHO_WE_ARE': 'Хто ми і заради чого збір',
    #     'BENEFITS': 'Для чого це Вам?',
    #     'HOW': 'Як ми це плануємо зробити?'
    # },
    # 'WHO_SUITS_OPTIONS': {
    #     'WHY': 'Some text',
    #     'LIST': 'Some text 2'
    # }
