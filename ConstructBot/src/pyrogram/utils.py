from pyrogram import Client

import config
from src.core import models
from src.core.utils import SQLAlchemyComponent
from src.jobs.utils import inspect_checker


async def pyrogram_send_message(chat_id, msg):
    if config.USE_PYROGRAM:
        lid = await SQLAlchemyComponent(models.Lid).get_first(
            filter=("telegram_id", int(chat_id)),
            rel=[(models.Lid.utm, models.Utm.bots_person)]
        )
        pr = lid.utm.bots_person[0]
        async with Client(f"src/pyrogram/sessions/{pr.phone}_parallel", api_id=pr.api_id, api_hash=pr.hash, phone_number=pr.phone) as app:
            await app.send_message(chat_id=chat_id, text=msg)
            await app.stop()


async def pyrogram_auto_request_to_channel(chat_id):
    if config.USE_PYROGRAM:
        lid = await SQLAlchemyComponent(models.Lid).get_first(
            filter=("telegram_id", int(chat_id)),
            rel=[(models.Lid.utm, models.Utm.bots_person)]
        )
        pr = lid.utm.bots_person[0]
        if lid.utm.private_chat_id:
            async with Client(f"src/pyrogram/sessions/{pr.phone}_parallel", api_id=pr.api_id, api_hash=pr.hash, phone_number=pr.phone) as app:
                if lid.username:
                    await app.add_contact(lid.username, f"lid_{lid.username}")
                    await app.promote_chat_member(lid.utm.private_chat_id, chat_id)


async def pyrogram_check_user_wrote(chat_id: int):
    if config.USE_PYROGRAM:
        lid = await SQLAlchemyComponent(models.Lid).get_first(
            filter=("telegram_id", int(chat_id)),
            rel=[(models.Lid.utm, models.Utm.bots_person)]
        )
        pr = lid.utm.bots_person[0]
        private_dialogs = []

        async with Client(f"src/pyrogram/sessions/{pr.phone}_parallel", api_id=pr.api_id, api_hash=pr.hash, phone_number=pr.phone) as app:
            async for dialog in app.get_dialogs():
                private_dialogs.append(dialog.chat.id)

            if chat_id not in private_dialogs:
                return False
            return True


async def pyrogram_sendler(chat_id: int) -> None:
    if config.USE_PYROGRAM:
        lid = await SQLAlchemyComponent(models.Lid).get_first(
            filter=("telegram_id", int(chat_id)),
            rel=[(models.Lid.utm, models.Utm.bots_person)]
        )
        step = await SQLAlchemyComponent(models.Step).get_first(
            filter=("utm", lid.utm),
            detail=("title", "is_check_user_wrote",),
            rel=[(models.Step.utm,)]
        )
        if step and step.texts:
            from src.jobs.set_jobs import set_pyrogram_message
            await set_pyrogram_message(chat_id, step)

            await inspect_checker(chat_id=lid.telegram_id, step=step)
            from src.steps.reminder import inspect_reminder
            await inspect_reminder(chat_id=lid.telegram_id, step=step)
