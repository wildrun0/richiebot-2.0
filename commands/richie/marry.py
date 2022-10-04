import textwrap

import methods
from datatypes import PeerObject, User
from datatypes.peer import marriage_pending
from datatypes.user import get_user
from vkbottle.bot import Message


async def marry(event: Message, peer_obj: PeerObject, params: list[User]):
    marry_user = params[0]
    caller = await get_user(event.from_id, event.peer_id)
    speer_id = str(event.peer_id)
    if not marry_user.peers[speer_id].marry_with:
        # peer_obj.data.marriages.marriages_pending.append(marriage_pending(
        #     user1 = event.from_id,
        #     user2 =  marry_user.id,
        #     offer_start_date = event.date
        # ))
        if not (u1_nick := caller.peers[speer_id].nickname):
            u1_nick = await methods.display_nicknames(caller.id, 'ins')

        u2_nick = marry_user.get_nickname(speer_id)

        await event.answer(textwrap.dedent(f"""
        {u2_nick}, согласны ли вы вступить в брак
        c {u1_nick}?
        """))
    else:
        await event.answer("Пользователь уже состоит в браке!")