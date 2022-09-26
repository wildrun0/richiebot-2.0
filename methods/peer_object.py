from handlers import PeerObject
from commands.admin import renew_users_list
from vkbottle.bot import MessageMin


peers_objs = {}
def peer_object(func):
    async def wrapper(*args, **kwargs):
        event = isinstance(args[0], MessageMin) and args[0] or args[1]
        if (peer_id := event.peer_id) in peers_objs:
            peer_obj = peers_objs[peer_id]
        else:
            peer_obj = PeerObject(peer_id)
            await renew_users_list(event, peer_obj) # обновляем при каждой инициализации беседы (один раз на запуск)
            peers_objs[peer_id] = peer_obj
        f = await func(*args, peer_obj, **kwargs)
        return f
    return wrapper