from typing import Callable
from vkbottle.bot import Message
from vkbottle import VKAPIError

from datatypes import PeerObject
from methods import check_muted
from commands.admin import renew_users_list


# Насчет Callable. Вместо ивента сюда может прилететь что угодно,
# если декоратор вызывается не на ивенте, а в любом другом месте помимо
peers_objs = {}
def peer_manager(func):
    async def wrapper(*context_event: tuple[Message|Callable, Message|None], **kwargs):
        event = isinstance(context_event[0], Message) and context_event[0] or context_event[1]
        if (peer_id := event.peer_id) in peers_objs:
            peer_obj = peers_objs[peer_id]
        else:
            peer_obj = await PeerObject.init(peer_id)
            await renew_users_list(event, peer_obj) # обновляем при каждой инициализации беседы (один раз на запуск)
            peers_objs[peer_id] = peer_obj
        ### реагируем на ивенты
        if await check_muted(event, peer_obj):
            try:
                await event.ctx_api.messages.delete(
                    cmids = event.message_id, 
                    peer_id = event.peer_id,
                    delete_for_all = True
                )
                return None # чтобы бот не реагировал
            except (VKAPIError[15], VKAPIError[917]): pass
        if event.action:
            if peer_obj.data.ban_list.get(member_id := str(event.action.member_id)):
                try:
                    await event.ctx_api.messages.remove_chat_user(
                        chat_id = event.chat_id,
                        member_id = int(member_id)
                    )
                    await event.answer("Пользователь находится в бане")
                    return None
                except VKAPIError[925]: pass
        f = await func(*context_event, peer_obj, **kwargs)
        return f
    return wrapper