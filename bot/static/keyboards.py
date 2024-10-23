from pyrogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton)


class MenuOptions:
    PLACEHOLDER = '👇Оберіть пункт меню'
    BACK = '◀️Назад'

    class START_MENU:
        STATUS = '⚡️Дізнатись стан акаунту'
        FAQ = '❓FAQ'
        APPLY = '✅Запис на заняття'
        REGISTER = '✒️Реєстрація'
        CONTACT_MANAGER = '✋Зв\'язатись з менеджером'
        MENU = '📔Головне меню'

    class FAQ_OPTIONS:
        ABOUT_SCHOOL = 'Про школу'
        WHO_SUITS = 'Кому підійде'
        MONEY = 'Оплата'

    class ABOUT_SHOOL_OPTIONS:
        WHO_WE_ARE = 'Хто ми і заради чого збір'
        BENEFITS = 'Для чого це Вам?'
        HOW = 'Як ми це плануємо зробити?'

    class WHO_SUITS_OPTIONS:
        WHY = 'Навіщо це потрібно'
        LIST = 'Для кого підійде курс'

    class MONEY_OPTIONS:
        PRICE = 'Ціна'
        TERMS = 'Умови та строки оплати'

    class ADMIN_OPTIONS:
        FIND_USER = '🔍Отримати дані про користувача через id, моб. теле. або @username'
        ADD_LESSON = '➡️Додати занятя'
        GET_LESSONS = '⬇️Список занять'
        EXIT = '🔧Вийти з панелі'


class ReplyKeyboards:
    START = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.START_MENU.STATUS), KeyboardButton(MenuOptions.START_MENU.APPLY)],
        [KeyboardButton(MenuOptions.START_MENU.FAQ), KeyboardButton(MenuOptions.START_MENU.CONTACT_MANAGER)],
    ], is_persistent=True,
        placeholder=MenuOptions.PLACEHOLDER,
        resize_keyboard=True)

    START_NOT_REGISTERED = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.START_MENU.REGISTER), KeyboardButton(MenuOptions.START_MENU.FAQ)],
    ], is_persistent=True,
        placeholder=MenuOptions.PLACEHOLDER,
        resize_keyboard=True)

    FAQ = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.FAQ_OPTIONS.ABOUT_SCHOOL), KeyboardButton(MenuOptions.FAQ_OPTIONS.WHO_SUITS)],
        [KeyboardButton(MenuOptions.FAQ_OPTIONS.MONEY), KeyboardButton(MenuOptions.BACK)],
    ], is_persistent=True,
        placeholder='Оберіть розділ питань',
        resize_keyboard=True)

    ABOUT_SCHOOL = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.ABOUT_SHOOL_OPTIONS.WHO_WE_ARE),
         KeyboardButton(MenuOptions.ABOUT_SHOOL_OPTIONS.HOW)],
        [KeyboardButton(MenuOptions.ABOUT_SHOOL_OPTIONS.BENEFITS), KeyboardButton(MenuOptions.BACK)],
    ], is_persistent=True,
        placeholder=MenuOptions.PLACEHOLDER,
        resize_keyboard=True)

    WHO_SUITS = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.WHO_SUITS_OPTIONS.WHY), KeyboardButton(MenuOptions.WHO_SUITS_OPTIONS.LIST)],
        [KeyboardButton(MenuOptions.BACK)]
    ], is_persistent=True,
        placeholder=MenuOptions.PLACEHOLDER,
        resize_keyboard=True)

    MONEY = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.MONEY_OPTIONS.TERMS), KeyboardButton(MenuOptions.MONEY_OPTIONS.PRICE)],
        [KeyboardButton(MenuOptions.BACK)]
    ], is_persistent=True,
        placeholder=MenuOptions.PLACEHOLDER,
        resize_keyboard=True)


class AdminReplyKeyboards:
    START = ReplyKeyboardMarkup([
        [KeyboardButton(MenuOptions.ADMIN_OPTIONS.FIND_USER)],
        [KeyboardButton(MenuOptions.ADMIN_OPTIONS.ADD_LESSON), KeyboardButton(MenuOptions.ADMIN_OPTIONS.GET_LESSONS)],
        [KeyboardButton(MenuOptions.ADMIN_OPTIONS.EXIT)],
    ], is_persistent=True,
        placeholder=MenuOptions.PLACEHOLDER,
        resize_keyboard=True)


class FAQInfo:
    WHO_WE_ARE = ('Ми молода команда, на чолі якої студенти медичного, економічного університету '
                  'та інформаційних технологій. Ми маємо бажання зробити свій внесок в майбутнє'
                  'української медицини та допомогти студентам-медикам знайти себе у вирі цієї складної, '
                  'надзвичайно конкурентної професії.')

    BENEFITS = ('Ми певні, якщо Ви студент-медик, то вже зіштовхнулись або чули від старших колег про '
                'брак практичних навичок на парах в університеті. Наші курси по-максимуму наповнені '
                'практикою, що подається після найважливішої теорії по визначеній темі заняття.')

    HOW = ('Ми підготували для Вас цікаві, практично-орієнтовані тренінги для навчання та '
           'відпрацювання навичок з різних хірургічних спеціальностей.')

    WHO_SUITS_LIST = ('-Студентам-медикам, що тільки вступили до лав університу і вже хочуть набивати '
                      'руку та отримувати цікаві знання та цінні навички. Студентам 3-го курсу, що готуються '
                      'до іспиту ОСКІ-1, так як саме для Вас ми готуємо тренінг по підготовці до цього екзамену.'
                      '\n-Студентам старших курсів, що готуються до інтернатури, адже тільки уявіть '
                      'собі конкуренцію, коли тільки починаєте шлях нтерна: Ви приходите в новий колектив,'
                      ' Ви знаєте багато теорії, але не знаєте як їїзастосувати, і зовсім нічого не вмієте '
                      'робити руками, ні банально шити або в\'язати хірургічні вузлики, натомість '
                      'у відділені є старші інтерни, які асистують на операціях, а Вас не беруть асистувати, '
                      'бо ніхто не зацікавлений Вас навчити, і лишаєтесь просто писати величезну купу історій.'
                      ' Але інша сторона медалі, якщо Ви приходите на інтернатуру, заздалегідь оволодівши '
                      'базовими навичками, поступово, але впевнено набираєтесь довіри лікарів і вже маєте '
                      'помітний буст в порівнянні з тими, хто прийшов тільки із теоритичними знаннями.'
                      '\n-Школярі, які задумуються над майбутньою професією лікаря і бажають спробувати '
                      'як це зробити свою міні-операцію, до прикладу.')

    WHY = ('1. Ми виступаємо платформою для ком\'юніті медичної молоді для обміну досвідом, новинами, '
           'знаннями, створюємо коло однодумців.\n2. Ментором тренінгів є студент 4-го курсу НМУ ім. '
           'О. О. Богомольця. Хто як не студент зрозуміє всі проблеми сучасних студентів медичного, '
           'знає на що варто звернути увагу, і знає так багато лайфхаків, як швидше і простіше чомусь навчитись?')

    PRICE = ('Ціна за один тренінг 800 грн з предоплатою в 100 грн. Предоплата використовується для'
             'закупівлі матеріалів і для впевненості у ваших намірах.')
    TERMS = ('Передоплата в розмірі 100 грн вноситься не пізніше ніж за 3 дні до тренінгу. '
             'Також, якщо у вас змінились плани і ви не зможете відвідати тренінг, ми можемо повернути предоплату '
             'не пізніше ніж за 3 дні до тренінгу.')


faq_mapping = {
    MenuOptions.FAQ_OPTIONS.MONEY: {
        'keyboard': ReplyKeyboards.MONEY,
        MenuOptions.MONEY_OPTIONS.PRICE: FAQInfo.PRICE,
        MenuOptions.MONEY_OPTIONS.TERMS: FAQInfo.TERMS
    },
    MenuOptions.FAQ_OPTIONS.WHO_SUITS: {
        'keyboard': ReplyKeyboards.WHO_SUITS,
        MenuOptions.WHO_SUITS_OPTIONS.LIST: FAQInfo.WHO_SUITS_LIST,
        MenuOptions.WHO_SUITS_OPTIONS.WHY: FAQInfo.WHY
    },
    MenuOptions.FAQ_OPTIONS.ABOUT_SCHOOL: {
        'keyboard': ReplyKeyboards.ABOUT_SCHOOL,
        MenuOptions.ABOUT_SHOOL_OPTIONS.HOW: FAQInfo.HOW,
        MenuOptions.ABOUT_SHOOL_OPTIONS.BENEFITS: FAQInfo.BENEFITS,
        MenuOptions.ABOUT_SHOOL_OPTIONS.WHO_WE_ARE: FAQInfo.WHO_WE_ARE,
    }
}
