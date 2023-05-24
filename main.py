import os
from typing import Tuple, Union
from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message, User, Chat
import random
from datetime import datetime, timedelta
from pyrogram.errors import UserNotParticipant
from pyrogram.enums import MessageEntityType

HRZ = Client(
   "BanBot",
   api_id=int(os.environ.get("API_ID", "23050566")),
   api_hash=os.environ.get("API_HASH", "25e954ccd4afb778eea69bd6754275ff"),
   bot_token=os.environ.get("BOT_TOKEN", "6114635649:AAFUbkQtpjI3Fmn8ehmhBIdpu4qCPFsDHhs")
)
             
PICS = [
 "https://telegra.ph/file/cc4e670c97263c4984091.png"
]
             
force_channel = "TheHRZTG"
             
@HRZ.on_message(filters.command(["start"]) & filters.private)
async def start(client, message):
    if force_channel:
        try:
            user = await client.get_chat_member(force_channel, message.from_user.id)
            if user.status == "kicked out":
                await message.reply_text("You Are Banned")
                return
        except UserNotParticipant :
            await message.reply_text(
                text="🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🤭\nPlease Join our Channel to use this Bot..!",
                reply_markup=InlineKeyboardMarkup( [[
                 InlineKeyboardButton("🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 🤭", url=f"t.me/{force_channel}")
                 ]]
                 )
            )
            return
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=f"""**Hi {message.from_user.mention} 👋

I am [HRZ Ban Bot](http://t.me/HRZBanBot) Created By [HRZ TG](t.me/TheHRZTG)... 😎
I can Ban users from your group who break your groups rules... 🔥

Add me to a group and make me Admin to show my powers... 😍

Hit /help for to see how my power works... 😁**""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("➕ Add me to your Group ➕", url="http://t.me/HRZBanBot?startgroup=start"),
            ],[
            InlineKeyboardButton("📢 Channel", url="t.me/TheHRZTG"),
            InlineKeyboardButton("👥 Support Group", url="t.me/HRZSupport"),
            ],[
            InlineKeyboardButton("🛠 Help", callback_data="help"),
            InlineKeyboardButton("🤠 About", callback_data="about")
            ]]
            )
        )
             
@HRZ.on_message(filters.command(["help"]) & filters.private)
async def help(client, message):
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=f"""**Hey {message.from_user.mention} 👋

Welcome to Help menu of [HRZ Ban Bot](http://t.me/HRZBanBot)..!**""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("💁🏼‍♂️ Basic Commands", callback_data="commands"),
            ],[
            InlineKeyboardButton("🏡 Home", callback_data="start"),
            InlineKeyboardButton("🔙 Back", callback_data="start")
            ]]
            )
        )
@HRZ.on_message(filters.command(["about"]) & filters.private)
async def about(client, message):
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=f"""**Hey {message.from_user.mention} 👋
        
Welcome to About menu of [Group Help Bot](http://t.me/HRZGroupHelpBot)..!

亗 Name      : [Group Help Bot](http://t.me/HRZGroupHelpBot)
亗 Developer : [HRZ 🇮🇳](t.me/HRZRobot)
亗 Language  : [Python](https://python.org)
亗 Library   : [Pyrogrsm](https://pyrogram.org)
亗 Channel   : [HRZ TG](t.me/TheHRZTG)
亗 Support   : [HRZ Support](t.me/HRZSupport)
亗 Server    : [Somewhere](t.me/HRZRobot)
亗 Source    : [Click Here](t.me/HRZRobot)**""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("🏡 Home", callback_data="start"),
            InlineKeyboardButton("🔙 Back", callback_data="help")
            ]]
            )
        )
      
# extract_user

def extract_user(message: Message) -> Tuple[int, str, Union[Chat, User]]:
    """extracts the user from a message"""
    user_id = None
    user_first_name = None
    aviyal = None

    if len(message.command) > 1:
        if (
            len(message.entities) > 1 and
            message.entities[1].type == MessageEntityType.TEXT_MENTION
        ):
            # 0: is the command used
            # 1: should be the user specified
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
            aviyal = required_entity.user
        else:
            user_id = message.command[1]
            # don't want to make a request -_-
            user_first_name = user_id
            aviyal = True

        try:
            user_id = int(user_id)
        except ValueError:
            pass

    elif message.reply_to_message:
        user_id, user_first_name, aviyal = _eufm(message.reply_to_message)

    elif message:
        user_id, user_first_name, aviyal = _eufm(message)

    return (user_id, user_first_name, aviyal)

# extract_time

def extract_time(time_val):
    if any(time_val.endswith(unit) for unit in ("s", "m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            return None

        if unit == "s":
            bantime = datetime.now() + timedelta(seconds=int(time_num))
        elif unit == "m":
            bantime = datetime.now() + timedelta(minutes=int(time_num))
        elif unit == "h":
            bantime = datetime.now() + timedelta(hours=int(time_num))
        elif unit == "d":
            bantime = datetime.now() + timedelta(days=int(time_num))
        else:
            # how even...?
            return None
        return bantime
    else:
        return None
   
# _enufm

def _eufm(message: Message) -> Tuple[int, str, Union[Chat, User]]:
    user_id = None
    user_first_name = None
    ithuenthoothengaa = None

    if message.from_user:
        ithuenthoothengaa = message.from_user
        user_id = ithuenthoothengaa.id
        user_first_name = ithuenthoothengaa.first_name

    elif message.sender_chat:
        ithuenthoothengaa = message.sender_chat
        user_id = ithuenthoothengaa.id
        user_first_name = ithuenthoothengaa.title

    return (user_id, user_first_name, ithuenthoothengaa)

# Ban Command Available in Groups

@HRZ.on_message(filters.command(["ban"]) & filters.group)
async def ban(_, message):
    user_id, user_first_name, _ = extract_user(message)

    try:
        await message.chat.ban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"""**Someone is breaked the limit..!
{user_first_name} is Banned ⚠"""
            )
            
# UnBan Command Available in Groups

@HRZ.on_message(filters.command(["unban"]) & filters.group)
async def unban(_, message):
    user_id, user_first_name, _ = extract_user(message)

    try:
        await message.chat.unban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"""Ok, You are Unbanned Now ✔ 
{user_first_name} can Join the group..!"""
            )
            
@HRZ.on_message(filters.command(["tban"]) & filters.group)
async def tban(_, message):
    if not len(message.command) > 1:
        return

    user_id, user_first_name, _ = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "An invalid time type was specified. "
                "I am expected m, h, or d, But I got: {}"
            ).format(message.command[1][-1])
        )
        return

    try:
        await message.chat.ban_member(user_id=user_id, until_date=until_date_val)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Someone is beaked group rules..! "
                f"{user_first_name}"
                f" banned for {message.command[1]}!"
            )
            
print("Bot Started..!")

HRZ.run()
