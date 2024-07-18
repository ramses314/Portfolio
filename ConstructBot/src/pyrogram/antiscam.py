import random

from aiogram import Bot
from pyrogram import Client, filters

from src.core import models
from src.core.database import get_sync_session
from src.core.utils import SQLAlchemyComponent


def manage_sessions():
    import os
    import shutil

    folder_path = 'src/pyrogram/sessions'
    files = os.listdir(folder_path)

    for file in files:
        if file.endswith('parallel.session') or file.endswith('parallel.session-journal'):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)

    files = os.listdir(folder_path)
    for file in files:
        if not file.endswith('.session-journal'):
            base_name, extension = os.path.splitext(file)
            copy_name = f'{base_name}_parallel{extension}'
            src = os.path.join(folder_path, file)
            dest = os.path.join(folder_path, copy_name)
            shutil.copy2(src, dest)


def build_antiscam_tasks(tasks: list, session=get_sync_session()) -> list:
    manage_sessions()
    session = get_sync_session()
    query = session.query(models.BotPerson).join(models.BotPerson.utms)
    accounts = query.filter(models.Utm.is_bot_person == True).all()
    session.close()

    for account in accounts:
        tasks.append(
            (pyrogram_antiscam, account.api_id, account.hash, account.phone)
        )
    return tasks


async def pyrogram_antiscam(api_id, api_hash, phone):
    account: models.BotPerson = await SQLAlchemyComponent(models.BotPerson).get_first(
        filter=("api_id", api_id),
        rel=[(models.BotPerson.utms, models.Utm.bots_antiscam)]
    )
    pyrogram_client = Client(
        f"src/pyrogram/sessions/{phone}",
        api_id=api_id,
        api_hash=api_hash,
        phone_number=phone
    )

    try:
        token = account.utms[0].bots_antiscam[0].token
        if token:
            bot = Bot(token, parse_mode="MARKDOWN")
    except Exception as e:
        from main import bot

    @pyrogram_client.on_message(filters.me)
    async def pyrogram_handler(client, message):
        slices = str(message.text).split(" ")
        channel_id = account.utms[0].bots_antiscam[0].chat_id

        for search_crypto in slices:
            if len(search_crypto) > 30:
                prefixes = ["TQ", "t", "T", "0", "bc", "ltc", "DN"]

                if any(search_crypto.startswith(prefix) for prefix in prefixes):
                    administrators = await bot.get_chat_administrators(str(channel_id))
                    admin = random.choice(
                        [admin for admin in administrators if admin.user.id != (await bot.get_me()).id]
                    )

                    lid = await SQLAlchemyComponent(models.Lid).get_first(
                        filter=("telegram_id", int(message.chat.id),),
                        rel=[(models.Lid.utm,)]
                    )

                    text = [
                        "🆘 Подозрительная активность: возможен адрес криптокошелька в личке",
                        f"\n❗️ Отправитель: [{message.from_user.username}](tg://user?id={message.from_user.id})",
                        f"\n⬇️ Получатель ([написать](tg://user?id={message.chat.id}))",
                        f"Telegram ID: {message.chat.id}",
                        f"Quotex ID: {lid.partner_pk if lid else 'None'}",
                        f"sub utm: `{lid.utm.funnel if lid else 'None'}`  ",
                        f"\n📋 Текст сообщения: 👇🏼👇🏼👇🏼\n{message.text}",
                        f"\n📌 [{admin.user.username}](tg://user?id={admin.user.id}) требуется проверка"
                    ]
                    return await bot.send_message(channel_id, "\n".join(text))

    try:
        await pyrogram_client.start()
    except Exception as e:
        print(f"pyrogram ERROR: {e}")
