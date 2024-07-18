from datetime import datetime
import pytz

from aiogram import types

from src.core import models
from src.core.database import async_session_maker
from src.core.utils import parse_utm, SQLAlchemyComponent, time_since_to_now


class LidConnector:
    def __init__(
            self,
            message: types.Message = None,
            callback: types.CallbackQuery = None,
    ):
        self.message = message
        self.callback = callback
        self.chat_id = message.chat.id if message else callback.message.chat.id

    async def init(self):
        message = self.message if self.message else self.callback.message
        utm = await parse_utm(message.text)
        lid = await SQLAlchemyComponent(models.Lid).get_first(
            filter=("telegram_id", int(self.chat_id),),
            rel=[(models.Lid.utm, models.Utm.steps,), (models.Lid.stages,), (models.Lid.utm, models.Utm.links_settings)],
            exc=False
        )

        async with async_session_maker() as session:
            if lid and not lid.utm_id:
                lid.utm_id = utm.id
                session.add(lid)

            if not lid:
                lid = models.Lid(
                    telegram_id=self.chat_id,
                    username=message.from_user.username if message.from_user else None,
                    current_step="init user",
                    partner_pk="None",
                    private_link="None",
                    datetime_startup=datetime.now(),
                    datetime_stop=datetime.now(),
                    utm_id=utm.id,
                )
                session.add(lid)
            await session.commit()
            lid = await SQLAlchemyComponent(models.Lid).get_first(
                filter=("telegram_id", self.chat_id,),
                rel=[
                    (models.Lid.utm, models.Utm.steps,),
                    (models.Lid.stages,),
                    (models.Lid.utm, models.Utm.links_settings)
                ],
                exc=False
            )
        return lid

    async def add_metric(self, step):
        async with async_session_maker() as session:
            lid = await self.init()
            lid.current_step = step.title_info
            now = datetime.now(tz=pytz.UTC)
            current_stage = step.title_info
            stages = lid.stages
            session.add(lid)

            new_stage = models.Stage(
                title=step.title_info,
                lid_id=lid.id,
            )

            for stage in lid.stages:
                if stage.title == current_stage:

                    previous_stage = stages[stages.index(stage) - 1]
                    previous_stage.finished = now
                    previous_stage.time = await time_since_to_now(previous_stage.updated)
                    stage.updated = now
                    session.add(stage)
                    session.add(previous_stage)
                    return await session.commit()

                elif stage == lid.stages[-1]:
                    stage.time = await time_since_to_now(stage.updated)
                    stage.finished = now
                    session.add(stage)
                    session.add(new_stage)

            if len(lid.stages) == 0:
                session.add(new_stage)

            await session.commit()
