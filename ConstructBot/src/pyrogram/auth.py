import asyncio

from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from pyrogram import Client

import config
from src.core import models
from src.core.utils import SQLAlchemyComponent, send_to_admins

bot = Bot(config.AIOGRAM_SECOND_BOT)
admins = config.PYROGRAM_ADMINS


async def get_pyrogram_accounts():
   return await SQLAlchemyComponent(models.BotPerson).find_all()

accounts = asyncio.run(get_pyrogram_accounts())

for account in accounts:
    client = None
    sent_code_hash = None
    auth_trigger = False

    number_of_accounts = int(accounts.index(account)) + 1
    all_account_len = len(accounts)


    async def aiogram_bot():
        dp = Dispatcher(storage=MemoryStorage())
        dp.callback_query.middleware(CallbackAnswerMiddleware())
        router = Router(name="main")

        @router.message(lambda message: True)
        async def code_broker(message: types.Message, state: FSMContext):
            phone_code = message.text
            if not sent_code_hash:
                return message.answer("Hi, I am  a launch bot 🤖 (личка)")
            try:
                await client.sign_in(
                    account.phone,
                    sent_code_hash,
                    phone_code
                )
                await state.clear()
                await message.answer(f"✅ Success!")
                global auth_trigger
                auth_trigger = True
            except:
                await message.answer(f"❌ Error: make sure is correct and send again")

        dp.include_router(router)
        await dp.start_polling(bot, skip_updates=True)


    async def pyrogram_provoke_auth():
        global client, sent_code_hash, auth_trigger

        client = Client(
            name=f"sessions/{account.phone}",
            api_id=account.api_id,
            api_hash=account.hash
        )
        await client.connect()

        try:
            await client.get_me()
            auth_trigger = True
            await send_to_admins(
                bot,
                admins=admins,
                msg=f"I`m launch bot 🤖 (личка)\n⚙️ Check account {number_of_accounts} of {all_account_len}\n✅ Authenticate success!")

        except:
            sent_code_hash = await client.send_code(account.phone)
            sent_code_hash = sent_code_hash.phone_code_hash
            await send_to_admins(
                bot,
                admins=admins,
                msg=f"I`m launch bot 🤖 (личка) \n⚙️ Checking account {number_of_accounts} of {all_account_len}"
                                   f"\n📲 I send confirm-code to +{account.phone}, moved him to hear 👇🏼")

    async def aiogram_pyrogram_sinergy():
        global auth_trigger
        aiogram_task = None
        pyrogram_task = None

        while not auth_trigger:

            await asyncio.sleep(3)

            if not auth_trigger:
                if aiogram_task is None:
                    aiogram_task = asyncio.ensure_future(aiogram_bot())
                if pyrogram_task is None:
                    pyrogram_task = asyncio.ensure_future(pyrogram_provoke_auth())

            elif auth_trigger:
                if aiogram_task and not aiogram_task.done():
                    aiogram_task.cancel()
                if pyrogram_task:
                    pyrogram_task.cancel()
                await asyncio.sleep(0)
                return

    # AUTHENTICATION BOT (AIOGRAM + PYROGRAM)
    asyncio.run(aiogram_pyrogram_sinergy())
