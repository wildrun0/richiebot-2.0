from vkbottle.bot import Message
from handlers.peer_handler import PeerObject
from datetime import datetime
from loader import tz, TIME_FORMAT


async def mute(event: Message, peer_obj: PeerObject, params: list):
    to_mute = params[0]
    if len(peer_obj.data.mute) > 0:
        mute_users, mute_lasting = zip(*peer_obj.data.mute)
        if to_mute.id in mute_users:
            await event.answer("Пользователь уже в муте!")
            return
    unmute_date = datetime.fromtimestamp(event.date, tz).strftime(TIME_FORMAT)
    
    peer_obj.data.mute.append((to_mute.id, event.date))
    
    await peer_obj.save()
    await event.answer(f"{to_mute.nickname and to_mute.nickname or to_mute.name} замьючен{'a' if to_mute.sex == 1 else ''} до {unmute_date}")