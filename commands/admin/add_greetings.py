from settings.config import MAX_GREETING_LENGTH
from methods import check
from vkbottle.bot import Message
from datatypes import PeerObject


async def add_greetings(event: Message, peer_object: PeerObject, params: list[str]) -> None:
    if await check.length(event, greeting := params[0], MAX_GREETING_LENGTH):
        peer_object.data.greeting = greeting
        await peer_object.save()
        await event.answer("✅Приветствие установлено!", disable_mentions=True)