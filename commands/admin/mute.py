from vkbottle.bot import Message
from datatypes.user.User import User
from handlers.peer_handler import PeerObject
from datetime import datetime
from loader import tz, TIME_FORMAT

time_seconds = {
    "год": 31536000,
    "лет": 31536000,
    "мес": 2592000,
    "нед": 604800,
    "час": 3600,
    "мин": 60,
    "сек": 1
}


async def mute(event: Message, peer_obj: PeerObject, params: tuple[User, tuple[int, str]]):
    to_mute = params[0]
    if len(peer_obj.data.mute) > 0:
        mute_users, mute_lasting = zip(*peer_obj.data.mute)
        if to_mute.id in mute_users:
            await event.answer("Пользователь уже в муте!")
            return
    
    unmute_date_multiplier = int(params[1][0])
    unmute_date_timedelta = params[1][1]
    
    unmute_date_timestamp = unmute_date_multiplier * time_seconds[unmute_date_timedelta]
    
    unmute_date = event.date + unmute_date_timestamp
    unmute_date_humanized = datetime.fromtimestamp(unmute_date, tz).strftime(TIME_FORMAT)
    
    peer_obj.data.mute.append((to_mute.id, unmute_date))
    
    await peer_obj.save()
    await event.answer(f"{to_mute.nickname and to_mute.nickname or to_mute.name} замьючен{'a' if to_mute.sex == 1 else ''} до {unmute_date_humanized}")