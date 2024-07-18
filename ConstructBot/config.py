from environs import Env

env = Env()
env.read_env()

# FOR BOT-CONSTRUCTOR
BOT_TOKEN = env.str('BOT_TOKEN')

# BOT HELPER FOR PYROGRAM AUTH
AIOGRAM_SECOND_BOT = env.str('AIOGRAM_SECOND_BOT')

USE_PYROGRAM = True if str(env.str('USE_PYROGRAM')).lower() == "true" else False

if USE_PYROGRAM:
    PYROGRAM_ADMINS = env.list('PYROGRAM_ADMINS')

REDIS_HOST = env.str('REDIS_HOST')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.str('DB_PORT')
DB_USER = env.str('DB_USER')
DB_NAME = env.str('DB_NAME')
DB_PASS = env.str('DB_PASS')

database_url = f"postgresql+asyncpg://{DB_USER}:" \
               f"{DB_PASS}@{DB_HOST}:" \
               f"{DB_PORT}/{DB_NAME}"

sync_database_url = f"postgresql://{DB_USER}:" \
               f"{DB_PASS}@{DB_HOST}:" \
               f"{DB_PORT}/{DB_NAME}"

