from . import MAX_STRING_LENGTH
from vkbottle.bot import Message
from handlers.peer_handler import PeerObject


async def add_greetings(event: Message, peer_object: PeerObject, params: list[str]) -> None:
    if len(greeting := params[0]) > MAX_STRING_LENGTH:
        await event.answer(f"🚫Недопустимая длина ({len(greeting)}>{MAX_STRING_LENGTH})")
    else:
        peer_object.data.greeting = greeting
        await peer_object.save()
        await event.answer("✅Приветствие установлено!", disable_mentions=True)