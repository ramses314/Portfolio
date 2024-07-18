import datetime

import aioredis
from aiogram import types

import config
from src.core import models
from src.core.utils import update_lid, SQLAlchemyComponent
from src.jobs.utils import check_subscribe
from src.pyrogram.utils import pyrogram_auto_request_to_channel, pyrogram_check_user_wrote, pyrogram_sendler, \
    pyrogram_send_message


async def jobs_checker():

    try:
        from src.steps.handlers import handle_from_checker
        redis = await aioredis.from_url(f'redis://{config.REDIS_HOST}')
        redis_lid_list = await redis.lrange("lid_checker", 0, -1)
        lids = [lid.decode() for lid in redis_lid_list]

        print(len(lids), "lid in checker: ", lids)

        for lid in lids:
            chat_id = int(lid.split("/")[0])
            type_of_check = lid.split("/")[1]

            if type_of_check == "is_check_quotex_register":
                await update_lid(chat_id, "is_registered", True)
                await redis.lrem("lid_checker", 0, f"{chat_id}/{type_of_check}")
                await handle_from_checker(chat_id, type_of_check)

            elif type_of_check == "is_check_quotex_deposit":
                await update_lid(chat_id, "is_deposited", True)
                await redis.lrem("lid_checker", 0, f"{chat_id}/{type_of_check}")
                await handle_from_checker(chat_id, type_of_check)

            elif type_of_check == "is_check_free_channel":
                lid = await SQLAlchemyComponent(models.Lid).get_first(
                    filter=("telegram_id", int(chat_id)),
                    rel=[(models.Lid.utm,)]
                )
                if await check_subscribe(lid.utm.public_chat_id, chat_id):
                    await update_lid(chat_id, "is_channel_joined", True)
                    await redis.lrem("lid_checker", 0, f"{chat_id}/{type_of_check}")
                    await handle_from_checker(chat_id, type_of_check)

            elif type_of_check == "is_autorequest":
                await pyrogram_auto_request_to_channel(chat_id)
                await redis.lrem("lid_checker", 0, f"{chat_id}/{type_of_check}")

            elif type_of_check == "is_check_user_wrote":
                if await pyrogram_check_user_wrote(chat_id):
                    await pyrogram_sendler(chat_id)
                    await update_lid(chat_id, "is_first_sendler", True)
                    await redis.lrem("lid_checker", 0, f"{chat_id}/{type_of_check}")

    finally:
        await redis.close()


async def jobs_reminder(
        chat_id: int,
        step_title: str,
        start_time: datetime,
):
    chat = types.Chat(id=chat_id, type="private")
    user = types.User(id=chat_id, username="user", is_bot=False, first_name='name')
    message = types.Message(message_id=111, from_user=user, text="some", chat=chat, date=start_time)
    ghost_callback = types.CallbackQuery(
        id="1",
        from_user=user,
        message=message,
        data=step_title,
        chat_instance="chat_instance",
    )
    from src.steps.construct import construct
    await construct(callback=ghost_callback)


async def jobs_pyrogram_send_msg(
        chat_id: int,
        step_title: str,
        start_time: datetime,
):
    chat = types.Chat(id=chat_id, type="private")
    user = types.User(id=chat_id, username="user", is_bot=False, first_name='name')
    message = types.Message(message_id=111, from_user=user, text="some", chat=chat, date=start_time)
    ghost_callback = types.CallbackQuery(
        id="1",
        from_user=user,
        message=message,
        data=step_title,
        chat_instance="chat_instance",
    )
    from src.steps.construct import construct
    await construct(callback=ghost_callback)


async def jobs_pyrogram_sendler(
        chat_id: int,
        step_title: str,
        start_time: datetime,
):
    chat = types.Chat(id=chat_id, type="private")
    user = types.User(id=chat_id, username="user", is_bot=False, first_name='name')
    message = types.Message(message_id=111, from_user=user, text="some", chat=chat, date=start_time)
    ghost_callback = types.CallbackQuery(
        id="1",
        from_user=user,
        message=message,
        data=step_title,
        chat_instance="chat_instance",
    )
    from src.steps.construct import construct
    await construct(callback=ghost_callback)


async def jobs_pyrogram_msg(chat_id: int, texts: list):
    for text in texts:
        await pyrogram_send_message(chat_id, text)
