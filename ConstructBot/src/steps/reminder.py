import datetime

import pytz
from sqlalchemy import select

from src.core import models
from src.core.database import async_session_maker
from src.jobs.set_jobs import set_reminders
from src.jobs.utils import clean_reminders


async def inspect_reminder(
        chat_id: int,
        step: models.Step,
):
    if step.reminder:
        async with async_session_maker() as session:
            start_time = datetime.datetime.now(tz=pytz.UTC)
            result = await session.execute(select(models.Step).where(
                models.Step.utm == step.utm,
                models.Step.title.like(f"{step.reminder}%")
            ))
            reminders = result.scalars().all()
            reminders = sorted(reminders, key=lambda obj: obj.title)
            await set_reminders(chat_id, reminders, start_time)
    elif not str(step.title).startswith("reminder"):
        await clean_reminders(chat_id)
