from MBot import MUserbot, BOT_ID
from MBot.mongo import mongodb


USERBOT = None
userbots_col = mongodb.userbots


async def get_userbot() -> MUserbot:
    global USERBOT
    if USERBOT:
        return USERBOT

    session_doc = await userbots_col.find_one({"_id": BOT_ID})
    if not session_doc:
        return None
    try:
        userbot = MUserbot(session_doc['session'])
        await userbot.start()
        USERBOT = userbot
    except:
        return None

    return userbot
