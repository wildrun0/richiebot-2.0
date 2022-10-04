import methods
from datatypes import PeerObject
from datatypes.user import get_user
from vkbottle.bot import Message


async def ban_list(event: Message, peer_obj: PeerObject, params: None):
    ban_list = peer_obj.data.ban_list
    if ban_list:
        to_send = "Список забаненных:\n"
        for banned_user, details in ban_list.items():
            banner = details[0]
            ban_time = details[1]

            banned_user_name = await methods.display_nicknames(int(banned_user), name_case='acc')
            
            banner_user = await get_user(banner, event.peer_id)
            banner_nickname = banner_user.get_nickname(event.peer_id)

            to_send += f"{banner_nickname} забанил{'а' if banner_user.sex == 1 else ''} {banned_user_name} {ban_time}\n"
        await event.answer(to_send, disable_mentions=True)
    else:
        await event.answer("Список пуст! :(")