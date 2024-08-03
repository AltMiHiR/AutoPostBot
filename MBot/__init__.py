from config import API_ID, API_HASH, BOT_TOKEN, POST_GROUP_LINK

from pyromod import Client as MClient

from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant

from MBot.logging import LOGGER
from MBot.utils.data import BOT_COMMANDS

BOT_ID = BOT_TOKEN.split(":", 1)[0]


class MBot(MClient):
    def __init__(self):
        super().__init__("MBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="MBot/modules"))
    
    async def start(self):
        await super().start()
        me = await self.get_me()
        self.id = me.id
        self.username = me.username

        # Set Bot Commands
        is_set = await self.set_bot_commands(BOT_COMMANDS)
        if is_set:
            LOGGER.info("Bot Commands Set.")
        else:
            LOGGER.info("Failed to Set Bot Commands.")


class MUserbot(Client):
    def __init__(self, session: str):
        self.proxy_generator = self.get_proxy()
        proxy = next(self.proxy_generator)
        super().__init__("MUserbot", api_id=API_ID, api_hash=API_HASH, session_string=session, no_updates=False, proxy=proxy)

    def get_proxy(self):
        PROXIES = [
            {
                "hostname": "103.172.84.68",
                "scheme": "socks5",
                "port": 59101,
                "username": "9919harshit",
                "password": "UoqPXdyQpz",
            },
            {
                "hostname": "103.172.85.53",
                "scheme": "socks5",
                "port": 59101,
                "username": "9919harshit",
                "password": "UoqPXdyQpz",
            }
        ]
        while True:
            for proxy_doc in PROXIES.copy():
                yield proxy_doc

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.id = me.id

        try:
            mx = await self.get_chat(POST_GROUP_LINK)
            await self.get_chat_member(mx.id, "me")
        except:
            try:
                await self.join_chat(POST_GROUP_LINK)
            except UserAlreadyParticipant:
                pass
            except Exception as err:
                pass

    async def change_proxy(self):
        await self.stop()
        self.proxy = next(self.proxy_generator)
        await self.start()


app = MBot()
