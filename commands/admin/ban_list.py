from handlers import PeerObject
from vkbottle.bot import Message
from datetime import datetime
from methods import display_nicknames
from loader import tz, TIME_FORMAT


async def ban_list(event: Message, peer_obj: PeerObject, params: None = None) -> None:
    ban_list = peer_obj.data.ban_list
    if ban_list:
        to_send = "Список забаненных:\n"
        for banned_user, details in ban_list.items():
            banner = details[0]
            ban_time = details[1]

            banner_user_name, banned_user_name = await display_nicknames((banner, banned_user), name_case=('nom', 'acc'))
            ban_time_humanized = datetime.fromtimestamp(ban_time, tz).strftime(TIME_FORMAT)
            
            to_send += f"{banner_user_name.name} забанил{'а' if banner_user_name.sex == 1 else ''} {banned_user_name.name} {ban_time_humanized}\n"
        await event.answer(to_send, disable_mentions=True)
    else:
        await event.answer("Список пуст! :(")