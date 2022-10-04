from vkbottle.bot import Message
from datatypes import PeerObject

async def del_rules(event: Message, peer_obj: PeerObject, params: None):
    if peer_obj.data.rules:
        peer_obj.data.rules = None
        await peer_obj.save()
        await event.answer("✅Правила удалены!")
    else:
        await event.answer("🚫Правила отсуствуют, удалять нечего")