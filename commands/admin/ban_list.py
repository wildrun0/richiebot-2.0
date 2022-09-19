from loader import peers_handler
from vkbottle.bot import Message
from loader import bot
from datetime import datetime
import pytz

tz = pytz.timezone("Europe/Moscow")

async def ban_list(event: Message) -> str:
    ban_list = peers_handler.get(event.peer_id, "ban_list")
    if ban_list:
        to_send = ""
        for banner, details in ban_list.items():
            users_names = await bot.api.users.get([details[0], banner], fields=["Sex"])
            
            banned_user_fullname = f"{users_names[0].first_name} {users_names[0].last_name}"
            banner_user_fullname = f"{users_names[1].first_name} {users_names[1].last_name}"

            ban_time = details[1]
            to_send += f"[id{banner}|{banner_user_fullname}] забанил{'a' if users_names[1].sex == 1 else ''} [id{details[0]}|{banned_user_fullname}] {datetime.fromtimestamp(ban_time, tz)}"
        await event.answer(to_send)