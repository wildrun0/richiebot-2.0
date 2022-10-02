from datatypes import PeerObject, User
from methods.get_group_id import get_group_id
from methods.get_user_id import get_user_id
from vkbottle import VKAPIError
from vkbottle.bot import Message


async def kick(event: Message, peer_obj: PeerObject, param: list[User]):
    if len(param) == 1:
        user_to_kick = param[0]
        uid = user_to_kick.id
    else:
        raw_id = param[1]
        if raw_id.isdigit():
            uid = int(raw_id) if param[0] == "id" else -int(raw_id)
        else:
            try:
                try:
                    uid = await get_user_id(raw_id)
                except:
                    uid = await get_group_id(raw_id)
            except: return
    if uid in peer_obj.data.admins:
        await event.answer("🚫Нельзя исключить админа!")
    else:
        try:
            await event.ctx_api.messages.remove_chat_user(
                chat_id=event.chat_id,
                member_id=uid
            )
            peer_obj.data.users.remove(uid)
            await peer_obj.save()
            await event.answer("✅Пользователь исключен!")
        except VKAPIError[935]:
            await event.answer("🚫Пользователь не состоит в беседе")
