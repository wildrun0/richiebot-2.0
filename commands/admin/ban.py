from vkbottle.bot import Message
from datatypes import User, PeerObject
from vkbottle import VKAPIError


async def ban(event: Message, peer_obj: PeerObject, params: tuple[User, list]):
    usr_to_ban = params[0]
    if not usr_to_ban:
        status = "🚫Неправильно указан пользователь!"
    else:
        ban_list = peer_obj.data.ban_list
        if str(usr_to_ban.id) in ban_list.keys():
            status = "🚫Пользователь уже забанен!"
        else:
            try:
                await event.ctx_api.messages.remove_chat_user(event.chat_id, member_id=usr_to_ban.id)
                peer_obj.data.ban_list[str(usr_to_ban.id)] = [event.from_id, event.date]
                await peer_obj.save()
                status = "✅Успешно забанен!"
            except VKAPIError[935]:
                status = "🚫Пользователь не состоит в беседе!"
            except VKAPIError[15]:
                status = "🚫Невозможно забанить администратора"
    await event.answer(status)