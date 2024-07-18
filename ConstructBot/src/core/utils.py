import asyncio
import datetime
from typing import Type

import pytz
from aiogram import Bot
from sqlalchemy import asc, select
from sqlalchemy.orm import selectinload

from src.core import models
from src.core.database import async_session_maker


def singleton(cls: Type):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def find_field(model, field):
    try:
        field = getattr(model, field)
    except Exception:
        return None
    return field


def fill_relation(statement, relation):
    for rel in relation:
        sub_options = selectinload(rel[0])
        for single_line in rel[1:]:
            sub_options = sub_options.selectinload(single_line)
        statement = statement.options(sub_options)
    return statement


class SQLAlchemyComponent:
    def __init__(self, model):
        self.model = model

    async def find_all(self, filter=None, sort=None, rel=None, exc=True):
        async with async_session_maker() as session:
            statement = select(self.model)

            if rel and isinstance(rel, list):
                statement = fill_relation(statement, rel)
            if filter and isinstance(filter, tuple):
                field = find_field(self.model, filter[0])
                statement = statement.filter(field == filter[1])
            if sort:
                sort_field = find_field(self.model, sort)
                statement = statement.order_by(asc(sort_field))

            result = await session.execute(statement)
            all_models = result.scalars().all()

            if not all_models and exc:
                pass

            return all_models

    async def get_first(self, detail=None, filter=None, rel=None, exc=True):
        async with async_session_maker() as session:
            statement = select(self.model)

            if rel and isinstance(rel, list):
                statement = fill_relation(statement, rel)
            if filter and isinstance(filter, tuple):
                field = find_field(self.model, filter[0])
                statement = statement.filter(field == filter[1])
            if detail and isinstance(detail, tuple):
                field = find_field(self.model, detail[0])
                statement = statement.filter(field == detail[1])

            result = await session.execute(statement)
            model = result.scalars().first()

            if not model and exc:
                pass

            return model


async def parse_utm(text: str) -> models.Utm:
    default_utm = await SQLAlchemyComponent(models.Utm).get_first()
    text = text.split(" ")

    if len(text) > 1:
        sub_parts = text[1].split("_")

        if len(sub_parts) > 1:
            utm = await SQLAlchemyComponent(models.Utm).get_first(
                filter=("title", f"utm_{sub_parts[1]}",),
                exc=False
            )
            return utm if utm else default_utm

    return default_utm


async def time_since_to_now(since_datetime: datetime):
    now = datetime.datetime.now(tz=pytz.UTC)
    since_datetime_sec = (now - since_datetime).total_seconds()
    sec = 86400 if since_datetime_sec > 86400 else since_datetime_sec
    time = datetime.time(int(sec // 3600), int((sec % 3600) // 60), int(sec % 60))
    return time


async def update_lid(chat_id, field, value) -> None:
    async with async_session_maker() as session:
        lid = await SQLAlchemyComponent(models.Lid).get_first(
            filter=("telegram_id", int(chat_id),),
        )
        setattr(lid, field, value)
        session.add(lid)
        await session.commit()


def async_wrapper(func: callable, *args, **kwargs) -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(func(*args, **kwargs))
    loop.run_forever()


async def send_to_admins(
        bot: Bot,
        admins: list,
        msg,
) -> None:
    for admin in admins:
        try:
            await bot.send_message(admin, text=msg)
        except:
            pass
