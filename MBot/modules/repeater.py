import asyncio

from config import OWNER_ID, POSTS_GROUP_ID

from pyrogram.errors import FloodWait, UserDeactivatedBan

from MBot import app
from MBot.logging import LOGGER
from MBot.utils.database import *
from MBot.utils.userbot import get_userbot


async def text_repeater():
    count = 0
    while True:
        userbot = await get_userbot()
        if not userbot:
            try:
                await app.send_message(OWNER_ID, "⛔ **ᴜsᴇʀʙᴏᴛ ᴀᴄᴄᴏᴜɴᴛ ɴᴏᴛ ᴀᴅᴅᴇᴅ.**\n\nᴘʟᴇᴀsᴇ ᴀᴅᴅ ɪᴛ ᴜsɪɴɢ /auth ᴄᴏᴍᴍᴀɴᴅ.\nᴛʀʏɪɴɢ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 ᴍɪɴᴜᴛᴇs...")
            except:
                LOGGER.warning("Userbot Account Not Added. Add it using /auth command. ReTrying after 5 minutes...")
            await asyncio.sleep(300)
            continue

        chats = await get_served_chats()
        is_repeat = await get_repeater_mode()
        post_chat_id, post_msg_id = await get_post()
        speed = await get_repeat_time()
        group_delay = await get_delay_time()

        if len(chats) == 0:
            await asyncio.sleep(speed)
        elif not is_repeat:
            await asyncio.sleep(speed)
        elif post_msg_id == 0:
            await asyncio.sleep(speed)
        else:
            for chat_id in chats:
                try:
                    await userbot.copy_message(chat_id, post_chat_id, post_msg_id)
                except FloodWait as e:
                    await asyncio.sleep(e.value + 2)
                    try:
                        await userbot.copy_message(chat_id, post_chat_id, post_msg_id)
                    except:
                        pass
                except UserDeactivatedBan:
                    try:
                        await app.send_message(POSTS_GROUP_ID, "Account is Banned. @PyXen")
                    except:
                        LOGGER.warning("Account is Banned.")
                    return
                except Exception as e:
                    continue
                if group_delay != 0:
                    await asyncio.sleep(group_delay)
            sleep_times = speed - (group_delay * len(chats))
            await asyncio.sleep(sleep_times)

        count += 1
        if count % 90 == 0:
            await userbot.change_proxy()
            try:
                await app.send_message(POSTS_GROUP_ID, f"PROXY CHANGED: {userbot.proxy['hostname']}")
            except:
                LOGGER.info(f"PROXY CHANGED: {userbot.proxy['hostname']}")


asyncio.create_task(text_repeater())
