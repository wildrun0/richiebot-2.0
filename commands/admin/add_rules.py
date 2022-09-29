from datatypes import User
from settings.config import MAX_RULES_LENGTH
from methods import check
from datatypes import PeerObject
from vkbottle.bot import Message


async def add_rules(event: Message, peer_object: PeerObject, params: tuple[User, str]) -> None:
    if await check.length(event, rules := params[1], MAX_RULES_LENGTH):
        peer_object.data.rules = rules
        await peer_object.save()
        await event.answer("✅Правила установлены", disable_mentions=True)