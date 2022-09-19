from loader import peers_handler
from vkbottle.bot import Message

async def add_greetings(event: Message) -> str:
    peers_handler.settings.set_greeting(event.peer_id, event.text)
    await event.answer("✅Приветствие установлено!")