from aiogram import types

from src.core import models


async def delete_message(
        utm: models.Utm,
        callback: types.CallbackQuery = None,
):
    bot = callback.message.bot if callback else None

    if utm.is_delete_keyboard and callback:
        try:
            await callback.message.edit_text(text=callback.message.text, reply_markup=None)
        except:
            pass

    if utm.is_delete_all and callback:
        try:
            first_for_delete = callback.message.reply_to_message.message_id
            last_for_delete = callback.message.message_id
            for msg in range(first_for_delete, last_for_delete + 1):
                await bot.delete_message(callback.message.chat.id, msg)
        except:
            pass
