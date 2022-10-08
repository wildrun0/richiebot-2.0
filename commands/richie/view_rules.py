from datatypes import PeerObject
from vkbottle.bot import Message


async def view_rules(event: Message, peer_obj: PeerObject, param: None):
    if (rules := peer_obj.data.rules):
        await event.answer(
            f"Правила беседы:\n{rules}", 
            disable_mentions = True
        )
    else:
        await event.answer("🚫Администратор не указал правила.")
