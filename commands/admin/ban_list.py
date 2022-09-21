from loader import peers_handler
from vkbottle.bot import Message
from datetime import datetime
from methods import display_nicknames
import pytz

tz = pytz.timezone("Europe/Moscow")

TIME_FORMAT = "%d.%m.%y %H:%M"
async def ban_list(event: Message) -> None:
    ban_list = await peers_handler.get(event.peer_id, "ban_list")
    if ban_list:
        to_send = "Список забаненных:\n"
        for banner, details in ban_list.items():
            banned_user = details[0]
            ban_time = details[1]
            
            banner_user_name, banned_user_name = await display_nicknames((banner, banned_user), name_case=('nom', 'acc'))
            ban_time_humanized = datetime.fromtimestamp(ban_time, tz).strftime(TIME_FORMAT)
            
            to_send += f"{banner_user_name.name} забанил{'а' if banner_user_name.sex == 1 else ''} {banned_user_name.name} {ban_time_humanized}"
        await event.answer(to_send, disable_mentions=True)