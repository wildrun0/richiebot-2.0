from datetime import datetime

from datatypes import PeerObject
from datatypes.user import get_user
from loader import tz
from methods.display_coins import _display_obj
from vkbottle.bot import Message


async def marry_list(event: Message, peer_obj: PeerObject, param: None):
    marry_list = peer_obj.data.marriages.couples
    if not marry_list:
        await event.answer("Браков нет! :(")
        return
    marry_str = '%s и %s в браке уже %s\n'
    to_send = ''
    curr_date = datetime.now(tz)
    for i in marry_list:
        u1, u2 = await get_user(i[0], event.peer_id), await get_user(i[1], event.peer_id)
        start_date = datetime.fromtimestamp(
            u1.peers[str(event.peer_id)].marry_with.start_date, 
            tz
        )
        to_send += marry_str % (u1.get_nickname(event.peer_id), 
                                u2.get_nickname(event.peer_id),
                                _display_obj(
                                    num = (curr_date - start_date).days, 
                                    titles=("день", 'дня', 'дней')
                                ))
    await event.answer(
        f"Браки в этой беседе: \n{to_send}", 
        disable_mentions = True
    )
