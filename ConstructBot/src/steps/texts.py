from aiogram import types

from main import bot
from src.steps.keyboards import keyboard
from src.core import models
from src.steps.links import link_parser


async def texts(
    chat_id: int,
    lid: models.Lid,
    step: models.Step,
    media_first_msg: types.Message = None,
) -> None:
    """Send texts from db

    Args:
        chat_id (int): id from telegram user chat.
        lid (models.Lid): lid obj from db.
        step (step): step with info for message.
        media_first_msg (types.Message, optional): aiogram message. Defaults to None.
    """

    message_id = media_first_msg.message_id if media_first_msg else None
    texts = step.texts or []
    key = None

    if step.keyboards:
        key = await keyboard(
            chat_id,
            step.keyboards or [],
        )
    for text in texts:
        text = await link_parser(text, lid)
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=key,
            reply_to_message_id=message_id,
        )
        key = None
    return
