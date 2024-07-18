from aiogram import types

from src.core import models
from main import bot


async def video_notes(
    chat_id: int,
    step: models.Step,
) -> types.Message:
    """Send video notes from db

    Args:
        chat_id (int): id from telegram user chat.
        step (models.Step): step with info for message.
    """
    first_msg_media = None
    video_notes_list = step.video_notes or []

    for video in video_notes_list:
        msg = await bot.send_video_note(
            chat_id=chat_id,
            video_note=video,
        )
        first_msg_media = msg if not first_msg_media else None

    return first_msg_media
