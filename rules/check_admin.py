from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule
from handlers.peer_handler import PeerObject
from methods.get_peer_object import peers_objs

from settings import bot_commands
from commands.admin import renew_admin_list

class IsAdmin(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        if not (peer_id := event.peer_id) in peers_objs:
            peer_obj = PeerObject(peer_id)
            await renew_admin_list(event, peer_obj)
            peers_objs[peer_id] = peer_obj

        admins = peers_objs[peer_id].data.admins
        if not admins:
            admins = await renew_admin_list(event, peers_objs[peer_id])
        if event.from_id in admins:
            return True
        elif not admins:
            await event.answer(f"""
                Список админов пустой. Скорее всего, боту не выданы привелегии администратора.
                Выдайте админку боту, а затем выполните команду:
                {[k for k,v in bot_commands.administrative_commands_full.items() if v == renew_admin_list]}
            """)
            return False
        else:
            await event.answer("⛔Вы не являетесь администратором")
            return False