import re
from vkbottle.bot import Message
from methods import check
from datatypes import PeerObject, User
from datatypes.user import NAME_TEMPLATE
from settings.config import MAX_NICKNAME_LENGTH

async def set_nickname(event: Message, peer_obj: PeerObject, params: tuple[User, str]) -> None:
    user, nickname_candidate = params
    if await check.length(event, nickname_candidate, MAX_NICKNAME_LENGTH):
        if re.search("\[(id|club)(\d+)\|.+\]", nickname_candidate):
            await event.answer("🚫Нельзя указывать пользователей в кличке!")
        else:
            nickname_id = NAME_TEMPLATE % ("club" if user.id < 0 else "id", user.id, nickname_candidate, "")
            user.peers[str(peer_obj.peer_id)].nickname = nickname_id.replace(' ', '')
            user.save()
            await event.answer(f"{user.get_nickname(event.peer_id)}, ✅Кличка добавлена", disable_mentions=True)