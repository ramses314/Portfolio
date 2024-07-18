import datetime
import random

import pytz

from main import scheduler
from src.core import models
from src.jobs import jobs
from src.pyrogram.utils import pyrogram_send_message


async def set_reminders(
        chat_id: int,
        reminders: list,
        start_time: datetime
):
    for reminder in reminders:
        start_time += datetime.timedelta(minutes=reminder.send_after_min)

        scheduler.add_job(
            jobs.jobs_reminder,
            'date',
            run_date=start_time,
            args=[chat_id, reminder.title, start_time],
            id=f'{chat_id}_reminder_{random.randint(0, 999)}'
        )


async def set_pyrogram_message(
        chat_id: int,
        step: models.Step,
):
    if step.send_after_min:
        start_time = (datetime.datetime.now(tz=pytz.UTC) +
                      datetime.timedelta(seconds=step.send_after_min))

        scheduler.add_job(
            jobs.jobs_pyrogram_msg,
            'date',
            run_date=start_time,
            args=[chat_id, step.texts],
            id=f'{chat_id}_reminder_pyrogram_{random.randint(0, 999)}'
        )

    else:
        for text in step.texts:
            await pyrogram_send_message(chat_id, text)


def set_checker():
    if not scheduler.get_job('check_checker'):
        scheduler.add_job(
            jobs.jobs_checker,
            'interval',
            seconds=5,
            id='check_checker',
        )


set_checker()
