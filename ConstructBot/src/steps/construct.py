from aiogram import types

from src.core import models
from src.core.utils import SQLAlchemyComponent
from src.jobs.utils import inspect_checker
from src.steps.delete_message import delete_message
from src.core.lid_connector import LidConnector
from src.steps.links import inspect_links
from src.steps.reminder import inspect_reminder
from src.steps.texts import texts
from src.steps.video_notes import video_notes
from src.steps.videos_and_photos import photos_and_videos


async def construct(
    message: types.Message = None,
    callback: types.CallbackQuery = None,
) -> None:

    media_first_msg = None
    callback_data = callback.data if callback else "start"
    lid = await LidConnector(message=message, callback=callback).init()
    step = await SQLAlchemyComponent(models.Step).get_first(
        filter=("utm", lid.utm),
        detail=("title", callback_data,),
        rel=[(models.Step.utm,)]
    )

    for construct in step.construct:
        if construct == "video_notes":
            media_first_msg = await video_notes(
                chat_id=lid.telegram_id,
                step=step
            )
        elif construct == "gallery":
            media_first_msg = await photos_and_videos(
                chat_id=lid.telegram_id,
                step=step,
                media_first_msg=media_first_msg
            )
        elif construct == "texts":
            await texts(
                chat_id=lid.telegram_id,
                step=step,
                lid=lid,
                media_first_msg=media_first_msg
           )

    await inspect_links(lid)
    await inspect_checker(chat_id=lid.telegram_id, step=step)
    await inspect_reminder(chat_id=lid.telegram_id, step=step)

    await delete_message(utm=lid.utm, callback=callback)
    await LidConnector(message=message, callback=callback).add_metric(step=step)
