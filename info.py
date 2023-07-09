import re
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]:
        return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# Bot information
PORT = environ.get("PORT", "8080")
WEBHOOK = bool(environ.get("WEBHOOK", True)) # for web support on/off
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PICS = (environ.get('PICS' ,'https://telegra.ph/file/42467dcbba60b89bdfcc3.jpg https://telegra.ph/file/035c689d755d861d3128a.jpg https://telegra.ph/file/485d7888d2156e24c17d9.jpg https://telegra.ph/file/1286cdc1a5f247bdbb22c.jpg https://telegra.ph/file/ec16a91557b5547659a8e.jpg https://telegra.ph/file/b53d515f874862ea81219.jpg https://telegra.ph/file/e65e4ef97558a825dcc6b.jpg https://telegra.ph/file/6823f3bd0914a8ceecca2.jpg https://telegra.ph/file/27ea4e5a1a7736bef46c4.jpg https://telegra.ph/file/610a9305f7a2318c852ac.jpg')).split()
BOT_START_TIME = time()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '324012925').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

#maximum search result buttos count in number#
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "10"))
START_MESSAGE = environ.get('START_MESSAGE', '👋 𝙷𝙴𝙻𝙾 {user}\n\n𝙼𝚈 𝙽𝙰𝙼𝙴 𝙸𝚂 {bot},\n𝙸 𝙲𝙰𝙽 𝙿𝚁𝙾𝚅𝙸𝙳𝙴 𝙼𝙾𝚅𝙸𝙴𝚂')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "⚠️ 𝙃𝙚𝙮 {query}! 𝙏𝙝𝙖𝙩'𝙨 𝙉𝙤𝙩 𝙁𝙤𝙧 𝙔𝙤𝙪. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙍𝙚𝙦𝙪𝙚𝙨𝙩 𝙔𝙤𝙪𝙧 𝙊𝙬𝙣")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', 'يجب الاشتراك في القناة لاستخدام البوت')
RemoveBG_API = environ.get("RemoveBG_API", "")
WELCOM_PIC = environ.get("WELCOM_PIC", "")
WELCOM_TEXT = environ.get("WELCOM_TEXT", "Hai {user}\nwelcome to {chat}")
PMFILTER = is_enabled(environ.get('PMFILTER', "False"), False)
G_FILTER = is_enabled(environ.get("G_FILTER", "True"), True)
BUTTON_LOCK = is_enabled(environ.get("BUTTON_LOCK", "False"), False)

# url shortner
SHORT_URL = environ.get("SHORT_URL")
SHORT_API = environ.get("SHORT_API")

# Others
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "80000"))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'Movies & Series Club 🎬')
P_TTI_SHOW_OFF = is_enabled(environ.get('P_TTI_SHOW_OFF', "True"), True)
PM_IMDB = is_enabled(environ.get('PM_IMDB', "True"), True)
IMDB = is_enabled(environ.get('IMDB', "True"), True)
SINGLE_BUTTON = is_enabled(environ.get('SINGLE_BUTTON', "True"), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b>{file_name}</b> \n\n⚙️ <b>الـحـجـم</b> {file_size}\n\n➲ [𝐆𝐫𝐨𝐮𝐩](https://t.me/AflamyGroup)\n➲ [𝐂𝐡𝐚𝐧𝐧𝐞𝐥](https://t.me/AflamSocietyy)</b>")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", None)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "🔮 الإسم : <a href={url}>{title}</a>\n📆 السنه : {year}\n🎭 التصنيف : {genres}\n⭐ التقييم : <a href={url}/ratings>{rating} IMDB</a>\n⏰ وقت التشغيل : {runtime} دقيقة\n🎞 إخراج : {director}\n🎙️ اللغة : {languages}\n🌍 بلد الإنتاج : {countries} \n\n®Pᴏᴡᴇʀᴇᴅ Bʏ : <a href=https://t.me/AflamSocietyy><b>Mᴏᴠɪᴇs & Sᴇʀɪᴇs Cʟᴜʙ 🎬</b></a>")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "False"), False)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled(environ.get('MELCOW_NEW_USERS', "False"), False)
PROTECT_CONTENT = is_enabled(environ.get('PROTECT_CONTENT', "False"), False)
PUBLIC_FILE_STORE = is_enabled(environ.get('PUBLIC_FILE_STORE', "True"), True)









