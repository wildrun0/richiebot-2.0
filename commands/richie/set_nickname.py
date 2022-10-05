import re

from datatypes import PeerObject
from datatypes.user import NAME_TEMPLATE, get_user
from methods import check
from settings.config import MAX_NICKNAME_LENGTH
from vkbottle.bot import Message


async def set_nickname(event: Message, peer_obj: PeerObject, params: list[str]) -> None:
    user, nickname_candidate = await get_user(event.from_id, event.peer_id), params[0]
    if await check.length(event, nickname_candidate, MAX_NICKNAME_LENGTH):
        from settings.bot_commands import UID_REGEX, WEB_URL_REGEX
        if (re.search(UID_REGEX, nickname_candidate, re.IGNORECASE) or 
            nickname_candidate in ["@all", "@online"] or 
            re.search("@(?:id|club)\s?\d+", nickname_candidate)):
            await event.answer("🚫Нельзя указывать пользователей в кличке!")
        elif re.search(WEB_URL_REGEX, nickname_candidate.replace(' ',''), re.IGNORECASE):
            await event.answer("🚫Нельзя указывать URL-ссылки в кличке!")
        else:
            nickname_id = NAME_TEMPLATE % ("club" if user.id < 0 else "id", user.id, '', nickname_candidate)
            user.peers[str(peer_obj.peer_id)].nickname = nickname_id
            await user.save()
            await event.answer(
                f"{user.get_nickname(event.peer_id)}, ✅Кличка добавлена", disable_mentions=True
            )