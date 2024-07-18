from aiogram.types import InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.core import models
from src.core.utils import SQLAlchemyComponent


async def keyboard(
    chat_id: int,
    keyboards_list: list,
) -> InlineKeyboardMarkup:
    lid = await SQLAlchemyComponent(models.Lid).get_first(filter=("telegram_id", chat_id,), exc=False)
    builder = InlineKeyboardBuilder()
    for keyboard in keyboards_list:
        utm = []
        for k, v in keyboard.items():
            if k == "utm" and k:
                utm.append(v.get("utm_source"))
                utm.append(v.get("utm_tg"))
            if str(v).startswith("http"):
                if utm:
                    user = None
                    if utm[1] == "username":
                        user = lid.username if lid.username else None
                    if utm[1] == "id":
                        user = lid.telegram_id
                    if v.find("/?") != -1:
                        builder.button(text=k, url=v + f"&{utm[0]}={user}")
                    else:
                        builder.button(text=k, url=v + f"?{utm[0]}={user}")
                else:
                    builder.button(text=k, url=v)
                    
            if str(v).startswith("callback"):
                builder.button(text=k, callback_data=v)
            if str(v).startswith("private_link"):
                builder.button(text=k, url=lid.private_link)
            if str(v).startswith("https://broker-qx"):
                builder.button(text=k, url=v + f"&click_id={lid.telegram_id}/Lara")

    return builder.adjust(1).as_markup()
