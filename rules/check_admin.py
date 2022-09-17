from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from loader import peers_handler

class IsAdmin(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        admins = await peers_handler.admins.get_list(event.peer_id)
        if event.from_id in admins:
            return True
        else:
            await event.answer("⛔Вы не являетесь администратором")
            return False