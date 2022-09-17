from loader import peers_handler
from vkbottle.bot import Message

async def add_greetings(event: Message) -> str:
    if event.from_id in await peers_handler.admins.get_list(event.peer_id):
        peers_handler.settings.set_greeting(event.peer_id, event.text)
        await event.answer("✅Приветствие установлено!")