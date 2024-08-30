import asyncio

from bot.models import AppUser
import gspread as gs


class Gsheet:
    cursor = (0, 0)

    def __init__(self, config_file_name, sheet_key):
        self.cursor = [0, 0]
        self.gc = gs.service_account(filename=config_file_name)
        self.sh = self.gc.open_by_key(sheet_key).sheet1

        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self.__config_cursor__)

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

    async def __get_cell_async__(self, loop, coords):
        return loop.run_in_executor(None, self.sh.cell, coords[0], coords[1])

    async def __update_cell_async__(self, loop, coords, data):
        loop.run_in_executor(None, self.sh.update_cell, coords[0], coords[1], data)

    async def __config_cursor__(self):
        loop = asyncio.get_event_loop()
        while await self.__get_cell_async__(loop, self.cursor) != '':
            self.cursor[0] += 1




