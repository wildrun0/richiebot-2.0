from datatypes import PeerObject
from methods import check
from settings.config import MAX_RULES_LENGTH
from vkbottle.bot import Message


async def add_rules(event: Message, peer_object: PeerObject, params: list[str]) -> None:
    if await check.length(event, rules := params[0], MAX_RULES_LENGTH):
        peer_object.data.rules = rules
        await peer_object.save()
        await event.answer("✅Правила установлены", disable_mentions=True)