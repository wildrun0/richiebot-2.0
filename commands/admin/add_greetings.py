from vkbottle.bot import Message
from handlers.peer_handler import PeerObject

async def add_greetings(event: Message, peer_object: PeerObject) -> None:
    peer_object.data.greeting = event.text
    await peer_object.save()
    await event.answer("✅Приветствие установлено!")