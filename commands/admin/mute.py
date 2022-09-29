from vkbottle.bot import Message
from datatypes import User, PeerObject
from datatypes import user
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
    to_mute, unmute_date_raw = params
    if len(peer_obj.data.mute) > 0:
        mute_users, mute_lasting = zip(*peer_obj.data.mute)
        if to_mute.id in mute_users:
            await event.answer("Пользователь уже в муте!")
            return
    unmute_date_multiplier, unmute_date_timedelta = int(unmute_date_raw[0]), unmute_date_raw[1]
    unmute_date_timestamp = unmute_date_multiplier * time_seconds[unmute_date_timedelta]
    unmute_date = event.date + unmute_date_timestamp
    try:
        unmute_date_humanized = datetime.fromtimestamp(unmute_date, tz).strftime(TIME_FORMAT)
    except OSError:
        await event.answer("Указан неправильный срок мута!")
        return
    peer_obj.data.mute.append((to_mute.id, unmute_date))
    await peer_obj.save()
    usr_nickname = to_mute.get_nickname(event.peer_id)
    await event.answer(f"{usr_nickname} замьючен{'a' if to_mute.sex == 1 else ''} до {unmute_date_humanized}")