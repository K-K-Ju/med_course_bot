import asyncio

from bot.models.AppUser import AppUser
import gspread as gs


class Gsheet:
    cursor = (0, 0)

    def __init__(self, _cursor_):
        self.cursor = _cursor_
        self.gc = gs.service_account(filename='.gspread_config/med-school-bot-ab94c6ed2675.json')
        self.sh = self.gc.open_by_key('1UNEWjM2tGdSAUdbeBjrIoRlr2P6Q1Iwc7bKscntKe70').sheet1
        self.__config_cursor__()

    async def add_user(self, user: AppUser):
        loop = asyncio.get_event_loop()
        await self.__update_cell_async__(loop, self.cursor, user.chat_id)
        self.cursor[1] += 1
        await self.__update_cell_async__(loop, self.cursor, user.user_name)
        self.cursor[1] += 1
        await self.__update_cell_async__(loop, self.cursor, user.registered)
        self.cursor[1] += 1
        await self.__update_cell_async__(loop, self.cursor,  user.state)

        self.cursor[0] += 1
        self.cursor[1] = 0

    async def __get_cell_async__(self, loop, coords: tuple):
        loop.run_in_executor(None, self.sh.cell, coords[0], coords[1])

    async def __update_cell_async__(self, loop, coords: tuple, data):
        loop.run_in_executor(None, self.sh.update_cell, coords[0], coords[1], data)

    async def __config_cursor__(self):
        loop = asyncio.get_event_loop()
        while await self.__get_cell_async__(loop, self.cursor) != '':
            self.cursor[0] += 1




