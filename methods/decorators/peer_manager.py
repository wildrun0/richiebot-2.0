from typing import Callable

from vkbottle.bot import Message
from vkbottle import VKAPIError
from vkbottle_types.objects import MessagesMessageActionStatus

from datatypes import PeerObject
from methods import check
from loader import ctx_storage
from commands.admin import renew_users_list


# Насчет Callable. Вместо ивента сюда может прилететь что угодно,
# если декоратор вызывается не на ивенте, а в любом другом месте помимо
def peer_manager(func):
    async def wrapper(*context_event: tuple[Message|Callable, Message|None], **kwargs):
        event = isinstance(context_event[0], Message) and context_event[0] or context_event[1]
        peer_id = event.peer_id
        peer_obj = ctx_storage.get(peer_id)
        if not peer_obj:
            peer_obj = await PeerObject.init(peer_id)
            await renew_users_list(event, peer_obj) # обновляем при каждой инициализации беседы (один раз на запуск)
            ctx_storage.set(peer_id, peer_obj)
        ### реагируем на ивенты
        if await check.muted(event, peer_obj):
            try:
                await event.ctx_api.messages.delete(
                    cmids = event.message_id, 
                    peer_id = peer_id,
                    delete_for_all = True
                )
                return None # чтобы бот не реагировал
            except (VKAPIError[15], VKAPIError[917]): pass
        if event.action:
            member_id = event.action.member_id
            if event.action.type != MessagesMessageActionStatus.CHAT_KICK_USER:
                if peer_obj.data.ban_list.get(str(member_id)):
                    try:
                        await event.ctx_api.messages.remove_chat_user(
                            chat_id = event.chat_id,
                            member_id = member_id
                        )
                        await event.answer("Пользователь находится в бане")
                        return None
                    except VKAPIError[925]: pass
                else:
                    peer_obj.data.users.append(member_id)
                    if member_id == peer_obj.data.owner_id: 
                        peer_obj.data.admins.append(member_id)
            else:
                peer_obj.data.users.remove(member_id)
                if member_id in peer_obj.data.admins:
                    peer_obj.data.admins.remove(member_id)
            await peer_obj.save()
        f = await func(*context_event, peer_obj, **kwargs)
        return f
    return wrapper