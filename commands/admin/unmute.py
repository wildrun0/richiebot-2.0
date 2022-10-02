from vkbottle.bot import Message
from datatypes import PeerObject, User

async def unmute(event: Message, peer_obj: PeerObject, params: list[User]):
    user = params[0]
    uid = user.id
    uid_in_list = [i for i in peer_obj.data.mute if uid in i]
    if uid_in_list:
        mute_tuple = uid_in_list[0]
        peer_obj.data.mute.remove(mute_tuple)
        await event.answer(f"{user.get_nickname(event.peer_id)}, мут снят!")
    else:
        await event.answer("🚫Пользователь не находится в муте!")