from loader import peers_handler
from vkbottle.bot import Message
from loader import bot
from datetime import datetime
from methods import display_nicknames
import pytz

tz = pytz.timezone("Europe/Moscow")

async def ban_list(event: Message) -> str:
    ban_list = peers_handler.get(event.peer_id, "ban_list")
    if ban_list:
        to_send = "Список забаненных:\n"
        for banner, details in ban_list.items():
            banned_user = details[0]
            banner_user_name, banned_user_name = await display_nicknames([banner, banned_user])
            ban_time = details[1]
            to_send += f"{banner_user_name} забанил {banned_user_name} {datetime.fromtimestamp(ban_time, tz)}"
        await event.answer(to_send, disable_mentions=True)