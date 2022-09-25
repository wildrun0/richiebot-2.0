from . import MAX_STRING_LENGTH
from handlers.peer_handler import PeerObject
from vkbottle.bot import Message


async def add_rules(event: Message, peers_object: PeerObject, params: list[str]) -> None:
    if len(rules := params[0]) > MAX_STRING_LENGTH:
        await event.answer(f"🚫Недопустимая длина ({len(rules)}>{MAX_STRING_LENGTH})")
    else:
        peers_object.data.rules = params[0]
        await peers_object.save()
        await event.answer("✅Правила установлены", disable_mentions=True)