import aioredis

import config
from main import bot, scheduler
from src.core import models


async def inspect_checker(
    chat_id: int,
    step: models.Step,
):

    type_of_checks = [
        "is_check_free_channel",
        "is_check_user_wrote",
        "is_autorequest",
    ]

    for type_of_check in type_of_checks:
        is_need = getattr(step, type_of_check)
        if is_need:
            redis = await aioredis.from_url(f'redis://{config.REDIS_HOST}')
            chats = await redis.lrange("lid_checker", 0, -1)
            chat_ids = [chat_id.decode() for chat_id in chats]

            if str(f"{chat_id}/{type_of_check}") not in chat_ids:
                await redis.rpush("lid_checker", f"{chat_id}/{type_of_check}")


async def check_subscribe(group_chat_id, user_id):
    try:
        chat_member = await bot.get_chat_member(chat_id=group_chat_id, user_id=user_id)

        if chat_member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception as e:
        return False


async def clean_reminders(chat_id):
    jobs = scheduler.get_jobs()
    for job in jobs:
        if str(job.id).startswith(f"{chat_id}_reminder_"):
            scheduler.remove_job(job.id)
