from datetime import datetime

from datatypes import PeerObject, User
from datatypes.peer import ban_info_struct, ban_struct
from loader import TIME_FORMAT, tz
from vkbottle import VKAPIError
from vkbottle.bot import Message


async def ban(event: Message, peer_obj: PeerObject, params: list[User]):
    usr_to_ban = params[0]
    if [ban.banned_uid for ban in peer_obj.data.ban_list if ban.banned_uid == usr_to_ban.id]:
        status = "🚫Пользователь уже забанен!"
    else:
        try:
            await event.ctx_api.messages.remove_chat_user(event.chat_id, member_id=usr_to_ban.id)
            ban_time = datetime.fromtimestamp(event.date, tz).strftime(TIME_FORMAT)
            banned_by = ban_info_struct(
                banned_by = event.from_id, 
                ban_time_str = ban_time
            )
            peer_obj.data.users.remove(usr_to_ban.id)
            peer_obj.data.ban_list.append(ban_struct(
                    banned_uid = usr_to_ban.id,
                    ban_info = banned_by,
                )
            )
            await peer_obj.save()
            status = "✅Успешно забанен!"
        except VKAPIError[935]:
            status = "🚫Пользователь не состоит в беседе!"
        except VKAPIError[15]:
            status = "🚫Невозможно забанить администратора"
    await event.answer(status)