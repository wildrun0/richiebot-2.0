import textwrap

from datatypes import PeerObject
from datatypes.peer.marriages import marriage_pending
from datatypes.user import get_user
from vkbottle.bot import Message


async def do_marriage(event: Message, peer_obj: PeerObject, pending: marriage_pending):
    peer_obj.data.marriages.marriages_pending.remove(pending)
    pid = event.peer_id

    u1 = await get_user(pending.user1, pid)
    u2 = await get_user(event.from_id, pid)
    u1_nick, u2_nick = u1.get_nickname(pid), u2.get_nickname(pid)
    if event.payload == '{"marriage":true}':
        spid = str(pid)

        u1_marry_obj = u1.peers[spid].marry_with
        u2_marry_obj = u2.peers[spid].marry_with

        u1_marry_obj.partner,    u2_marry_obj.partner    = u2.id, u1.id
        u1_marry_obj.start_date, u2_marry_obj.start_date = event.date, event.date

        await u1.save()
        await u2.save()

        peer_obj.data.marriages.couples.append([u1.id, u2.id])
        await peer_obj.save()

        await event.answer(textwrap.dedent(f"""
            {u1_nick} и {u2_nick} теперь в браке!
        """))
    else:
        await event.answer(textwrap.dedent(f"""
            {u1_nick}, {u2_nick} отказался от свадьбы.
            Не судьба...
        """))
