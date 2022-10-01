import textwrap
from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from datatypes import PeerObject
from methods import decorators
from settings import bot_commands
from commands.admin import renew_users_list
from loader import bot


class IsAdmin(ABCRule[Message]):
    def __init__(self, status: bool = None):
        self.status = status


    @decorators.peer_manager
    async def check(self, event: Message, peer_obj: PeerObject) -> bool:
        admins = peer_obj.data.admins
        if event.from_id in admins:
            return True
        elif not admins:
            answer = f"""
            Список админов пустой. Скорее всего, боту не выданы привелегии администратора.
            Выдайте админку боту, а затем выполните команду:
            {[k for k,v in bot_commands.administrative_commands_full.items() if v == renew_users_list]}
            """
            await event.answer(textwrap.dedent(answer))
            return False
        else:
            await event.answer("⛔Вы не являетесь администратором")
            return False

bot.labeler.custom_rules["is_admin"] = IsAdmin