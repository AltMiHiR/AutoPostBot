from config import *

from pyrogram import filters
from pyrogram.types import Message

from MBot import MBot, app
from MBot.logging import LOG_FILE_NAME
from MBot.utils.database import set_post, set_repeat_time, set_delay_time, add_served_chat, del_served_chat, get_served_chats, get_repeat_time


@app.on_message(filters.chat(POSTS_GROUP_ID) & filters.command(["sm", "setmessage"]) & filters.user(OWNER_ID))
async def set_message_ids(client: MBot, message: Message):
    r_message = message.reply_to_message

    if not r_message:
        try:
            value = message.text.split(None, 1)[1]
        except:
            await message.reply_text("Please Reply To a Message")
            return
        if str(value) == "0":
            set = await set_post(0, 0)
            if set:
                await message.reply_text("Successfully Reset")
                return

    set = await set_post(message.chat.id, r_message.id)
    if set:
        await message.reply_text("Successfully added in database.")
        return
    await message.reply_text("Failed to set this message !")
    return
          

@app.on_message(filters.private & filters.command(["st", "settime"]) & filters.user(OWNER_ID))
async def set_message_time(client, message):
    try:
        timer_value = int(message.text.split(None, 1)[1])
    except:
        return await message.reply_text(f"give me some time value in seconds.\n\nEx: `.st 10`")
    if int(timer_value) == 0:
        return await message.reply_text(f"time value need to set minium 1 sec !")
    set = await set_repeat_time(timer_value)
    if set:
        return await message.reply_text(f"Successfully Set time {timer_value} Seconds.")
    return await message.reply_text("Already Running with Same Time Value!")


@app.on_message(filters.private & filters.command(["dly", "delay"]) & filters.user(OWNER_ID))
async def set_group_time(client, message):
    try:
        timer_value = int(message.text.split(None, 1)[1])
    except:
        return await message.reply_text(f"give me some time value in seconds.\n\nEx: `.dly 2`")
    set = await set_delay_time(timer_value)
    if set:
        if int(timer_value) == 0:
            return await message.reply_text(f"group delay now disabled !")
        return await message.reply_text(f"Successfully Set time {timer_value} Seconds.")
    return await message.reply_text("Already Running with Same Time Value!")


@app.on_message(filters.private & filters.command(["ac", "addchat"]) & filters.user(OWNER_ID))
async def set_chats_ids(client, message):
    try:
        chat_id = int(message.text.split(None, 1)[1])
    except:
        return await message.reply_text("give me chat id")
    if chat_id > 0:
        return await message.reply_text("please give me correct chat id")
    is_chat = await add_served_chat(chat_id)
    if is_chat:
        return await message.reply_text("successfully added in my database")
    return await message.reply_text("already added in my database")
    

@app.on_message(filters.private & filters.command(["dc", "delchat"]) & filters.user(OWNER_ID))
async def del_chats_ids(client, message):
    try:
        chat_id = int(message.text.split(None, 1)[1])
    except:
        return await message.reply_text("give me chat id")
    if chat_id > 0:
        return await message.reply_text("please give me correct chat id")
    is_chat = await del_served_chat(chat_id)
    if is_chat:
        return await message.reply_text("successfully removed from my database")
    return await message.reply_text("chat id not active in my database")
    

@app.on_message(filters.private & filters.command("gc") & filters.user(OWNER_ID))
async def group_chats(client, message):
    chats = await get_served_chats()
    if len(chats) == 0:
        return await message.reply_text("no chat id found !")
    return await message.reply_text(f"{chats}")


@app.on_message(filters.private & filters.command("stats") & filters.user(OWNER_ID))
async def group_chats(client, message):
    chats = await get_served_chats()
    timev = await get_repeat_time()
    caption = f"""🥀 <u>**My Database Info:**</u> ✨
    
🌿 **Total Chats:** `{chats}`
🌷 **Delay Repeat Time Value:**
>> `{timev}` Seconds"""
    return await message.reply_text(caption)


@app.on_message(filters.private & filters.command('logs') & filters.user(OWNER_ID))
async def _get_logs(client, message: Message):
    if os.path.exists(LOG_FILE_NAME):
        x = await message.reply_text("🔄️ **ғᴇᴛᴄʜɪɴɢ ʟᴏɢs...**")
        await message.reply_document(LOG_FILE_NAME)
        await x.delete()
    else:
        await message.reply_text(f"⛔ **ʟᴏɢ ғɪʟᴇ `{LOG_FILE_NAME}` ᴅᴏᴇs ɴᴏᴛ ᴇxɪsᴛ.**")
