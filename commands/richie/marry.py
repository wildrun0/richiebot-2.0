import textwrap

import methods
from datatypes import PeerObject, User
from datatypes.peer import marriage_pending
from datatypes.user import get_user
from keyboards import marry_keyboard
from loader import bot
from tasks.functions import check_marry
from vkbottle.bot import Message


async def marry(event: Message, peer_obj: PeerObject, params: list[User]):
    are_already_in = [
        pending
        for pending in peer_obj.data.marriages.marriages_pending
        if pending.user1 == event.from_id or pending.user2 == event.from_id
    ]
    marry_timeout = peer_obj.data.marriages.marriages_timeout
    if are_already_in:
        pends = are_already_in[0]
        if event.date > (pends.offer_start_date + marry_timeout):
            peer_obj.data.marriages.marriages_pending.remove(pends)
        else:
            await event.answer("🚫Вы уже запросили брак.\nНельзя подавать несколько запросов!")
            return
    speer_id = str(event.peer_id)
    caller = await get_user(event.from_id, event.peer_id)
    if caller.peers[speer_id].marry_with.partner:
        await event.answer("🚫Вы уже находитесь в браке!")
        return
    marry_user = params[0]
    if marry_user.peers[speer_id].marry_with.partner:
        await event.answer("😢Пользователь уже состоит в браке!")
    else:
        pend_req = marriage_pending(
            user1 = event.from_id,
            user2 =  marry_user.id,
            offer_start_date = event.date
        )
        peer_obj.data.marriages.marriages_pending.append(
            pend_req
        )
        if not (u1_nick := caller.peers[speer_id].nickname):
            u1_nick = await methods.display_nicknames(caller.id, 'ins')
        u2_nick = marry_user.get_nickname(speer_id)

        await event.answer(textwrap.dedent(f"""
            💍 {u2_nick}, согласны ли вы вступить в брак
            c {u1_nick}?
        """), keyboard=marry_keyboard)

        bot.loop.create_task(check_marry(event.peer_id, marry_timeout, pend_req))