import re

from main import bot
from src.core import models
from src.core.utils import update_lid


async def inspect_links(
        lid: models,
):
    link_settings: models.LinkSettings = lid.utm.links_settings[0] if len(lid.utm.links_settings) > 0 else None
    private_chat_id: int = lid.utm.private_chat_id
    if not lid.private_link and private_chat_id and link_settings:
        if link_settings.is_create_join_request:
            new_private_link = await bot.create_chat_invite_link(
                chat_id=private_chat_id,
                expire_date=link_settings.expire_datetime,
                creates_join_request=link_settings.is_create_join_request,
            )
        else:
            new_private_link = await bot.create_chat_invite_link(
                chat_id=private_chat_id,
                expire_date=link_settings.expire_datetime,
                member_limit=link_settings.member_limit,
            )
        await update_lid(chat_id=lid.telegram_id, field="private_link", value=new_private_link.invite_link)


async def link_parser(input_text, lid):
    replacement_link = lid.private_link
    pattern = r'\{([^{}]+)\}'

    def replace_match(match):
        content = match.group(1)
        if content == "private_link":
            return replacement_link
        else:
            return match.group(0)

    if replacement_link:
        output_text = re.sub(pattern, replace_match, str(input_text))
        return output_text
    return input_text
