from datatypes import PeerObject, User
from vkbottle.bot import Message


async def unwarn(event: Message, peer_obj: PeerObject, params: list[User]):
    user = params[0]
    suid = str(user.id)

    if suid in peer_obj.data.warns.users:
        peer_obj.data.warns.users[suid] -= 1
    else:
        await event.answer("У пользователя нет предупреждений!")
        return

    warns_to_ban = peer_obj.data.warns.max_warns
    del peer_obj.data.warns.users[suid]

    await event.answer(f"{user.get_nickname(event.peer_id)}, предупреждения сняты (0/{warns_to_ban})")
    await peer_obj.save()