import multiprocessing as mp
import subprocess

import pytz
from aiogram import Bot, Dispatcher, enums
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
from src.core.utils import async_wrapper
from src.pyrogram.antiscam import build_antiscam_tasks

bot = Bot(config.BOT_TOKEN, parse_mode=enums.ParseMode.MARKDOWN)
scheduler = AsyncIOScheduler(timezone=pytz.UTC)
scheduler.start()


async def main():
    from src.steps.handlers import router
    dp = Dispatcher(storage=MemoryStorage())
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":

    tasks = [(main,)]

    if config.USE_PYROGRAM:
        subprocess.run(['python', 'auth.py'])
        tasks = build_antiscam_tasks(tasks)

    procs = [mp.Process(target=async_wrapper, args=(i for i in task)) for task in tasks]

    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()

