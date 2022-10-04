from datatypes import PeerObject, User
from methods.get_group_id import get_group_id
from methods.get_user_id import get_user_id
from vkbottle.bot import Message


async def unban(event: Message, peer_obj: PeerObject, param: tuple[None|User, str|int, None]):
    if isinstance(param[0], User): # юзер приходит только если пользователь в беседе
        await event.answer("Пользователь в беседе... он не забанен..ты што делаеш...")
        return
    if param[1] in ["id", "club"]:
        raw_id = param[2]
    else: raw_id = param[1]
    if raw_id.isdigit():
        raw_id = int(raw_id) if param[0] == "id" else -int(raw_id)
    else:
        try:
            try:
                raw_id = await get_user_id(raw_id)
            except:
                raw_id = await get_group_id(raw_id)
        except: return
    if (banned_id := str(raw_id)) in peer_obj.data.ban_list:
        peer_obj.data.ban_list.pop(banned_id)
        await peer_obj.save()
        await event.answer("✅Пользователь разбанен!")
    else:
        await event.answer("🚫Пользователя нет в списке забаненных!")