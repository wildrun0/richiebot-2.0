from handlers.peer_handler import PeerObject
from vkbottle.bot import Message

async def add_rules(event: Message, peers_object: PeerObject) -> None:
    peers_object.data.rules = event.text
    await peers_object.save()
    await event.answer("✅Правила установлены")