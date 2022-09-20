from loader import peers_handler
from vkbottle.bot import Message

async def add_rules(event: Message) -> None:
    peers_handler.settings.set_rules(event.peer_id, event.text)
    await event.answer("✅Правила установлены")