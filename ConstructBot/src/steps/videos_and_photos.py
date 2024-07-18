from aiogram import types

from main import bot
from src.core import models


async def send_media_group(
    media_list,
    chat_id: int = None,
):
    """_summary_

    Args:
        media_list (_type_): list of media
        chat_id (int, optional): chat id telegram private message. Defaults to None.
    """
    return await bot.send_media_group(chat_id, media_list)


async def photos_and_videos(
    chat_id: int,
    step: models.Step,
    media_first_msg: types.Message = None
) -> types.Message:
    """Send photos and videos from db

    Args:
        chat_id (int): id from telegram user chat.
        step (models.Step): step with info for message.
        media_first_msg (types.Message, optional): aiogram message. Defaults to None.
    """

    photos_list: list = step.photos or []
    videos_list: list = step.videos or []

    media: list = list()
    group_photo: list = list()
    group_video: list = list()

    if step.is_photos_group:
        media.extend(
            group_photo := [
                types.InputMediaPhoto(media=photo_id) for photo_id in photos_list
            ]
        )
    if step.is_videos_group:
        media.extend(
            group_video := [
                types.InputMediaVideo(media=video_id) for video_id in videos_list
            ]
        )

    if media:
        msg = await send_media_group(
            media_list=media,
            chat_id=chat_id,
        )
        media_first_msg = msg[0] if not media_first_msg else media_first_msg

        if group_video and not group_photo:
            for photo in photos_list:
                await bot.send_photo(chat_id=chat_id, photo=photo)

        if group_photo and not group_video:
            for video in videos_list:
                await bot.send_video(chat_id=chat_id, video=video)
    else:
        for video in videos_list:
            msg = await bot.send_video(chat_id=chat_id, video=video)
            media_first_msg = msg if not media_first_msg else media_first_msg

        for photo in photos_list:
            msg = await bot.send_photo(chat_id=chat_id, photo=photo)
            media_first_msg = msg if not media_first_msg else media_first_msg

    return media_first_msg
