from loader import peers_handler
from vkbottle.bot import Message
from methods import extract_id

async def ban(event: Message):
    if onreply := event.reply_message:
        to_ban = onreply.from_id
    else:
        to_ban = extract_id(event.text)
    if not to_ban:
        await event.answer("Неправильно указан пользователь!")
    else:
        pass