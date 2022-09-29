from vkbottle.bot import Message
from datetime import datetime
from loader import tz, TIME_FORMAT
from datatypes import User, PeerObject
from vkbottle import VKAPIError


async def ban(event: Message, peer_obj: PeerObject, params: tuple[User, list[None]]):
    usr_to_ban = params[0]
    if str(usr_to_ban.id) in peer_obj.data.ban_list:
        status = "🚫Пользователь уже забанен!"
    else:
        try:
            await event.ctx_api.messages.remove_chat_user(event.chat_id, member_id=usr_to_ban.id)

            peer_obj.data.users.remove(usr_to_ban.id)
            ban_time = datetime.fromtimestamp(event.date, tz).strftime(TIME_FORMAT)

            peer_obj.data.ban_list[str(usr_to_ban.id)] = [event.from_id, ban_time]
            await peer_obj.save()
            status = "✅Успешно забанен!"
        except VKAPIError[935]:
            status = "🚫Пользователь не состоит в беседе!"
        except VKAPIError[15]:
            status = "🚫Невозможно забанить администратора"
    await event.answer(status)