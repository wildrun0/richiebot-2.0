from typing import Callable
from vkbottle.bot import MessageMin
from datatypes import PeerObject
from commands.admin import renew_users_list

# Насчет Callable. Вместо ивента сюда может прилететь что угодно,
# если декоратор вызывается не на ивенте, а в любом другом месте помимо
peers_objs = {}
def peer_object(func):
    async def wrapper(*context_event: tuple[MessageMin|Callable, None], **kwargs):
        event = isinstance(context_event[0], MessageMin) and context_event[0] or context_event[1]
        if (peer_id := event.peer_id) in peers_objs:
            peer_obj = peers_objs[peer_id]
        else:
            peer_obj = PeerObject(peer_id)
            await renew_users_list(event, peer_obj) # обновляем при каждой инициализации беседы (один раз на запуск)
            peers_objs[peer_id] = peer_obj
        if event.from_id in [mute_tuple[0] for mute_tuple in peer_obj.data.mute]:
            usr_mute_pos = [i for i, v in enumerate(peer_obj.data.mute) if v[0] == event.from_id][0]
            timeout = peer_obj.data.mute[usr_mute_pos][1]
            if event.date > timeout:
                del peer_obj.data.mute[usr_mute_pos]
                await peer_obj.save()
            else:
                try:
                    await event.ctx_api.messages.delete(cmids=event.message_id, delete_for_all=True, peer_id=event.peer_id)
                    return None
                except: pass
        f = await func(*context_event, peer_obj, **kwargs)
        return f
    return wrapper