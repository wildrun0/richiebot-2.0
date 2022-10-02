import textwrap

from commands.admin import ban
from datatypes import PeerObject, User
from vkbottle.bot import Message


async def warn(event: Message, peer_obj: PeerObject, params: list[User]):
    user = params[0]
    suid = str(user.id)

    if suid in peer_obj.data.warns.users:
        peer_obj.data.warns.users[suid] += 1
    else:
        peer_obj.data.warns.users[suid] = 1

    have_warns = peer_obj.data.warns.users[suid]
    warns_to_ban = peer_obj.data.warns.max_warns
    user.peers[str(event.peer_id)].total_warns += 1

    await event.answer(textwrap.dedent(f"""
        {user.get_nickname(event.peer_id)}, вы получили предупреждение!
        До блокировки осталось: {have_warns}/{warns_to_ban}
    """))
    
    if have_warns >= warns_to_ban:
        del peer_obj.data.warns.users[suid]
        await ban(event, peer_obj, params)