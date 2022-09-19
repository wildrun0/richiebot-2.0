from loader import peers_handler
from vkbottle.bot import Message

async def add_rules(event: Message) -> str:
    if event.from_id in await peers_handler.admins.get_list(event.peer_id):
        peers_handler.settings.set_rules(event.peer_id, event.text)
        await event.answer("✅Правила установлены")