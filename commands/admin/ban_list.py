import methods
from vkbottle.bot import Message
from datatypes import PeerObject, User


async def ban_list(event: Message, peer_obj: PeerObject, params: tuple[User, str]) -> None:
    ban_list = peer_obj.data.ban_list
    if ban_list:
        to_send = "Список забаненных:\n"
        for banned_user, details in ban_list.items():
            banner = details[0]
            ban_time = details[1]

            banner_user_name, banned_user_name = await methods.display_nicknames((banner, banned_user), name_case=('nom', 'acc'))
            
            to_send += f"{banner_user_name.name} забанил{'а' if banner_user_name.sex == 1 else ''} {banned_user_name.name} {ban_time}\n"
        await event.answer(to_send, disable_mentions=True)
    else:
        await event.answer("Список пуст! :(")