from handlers.peer_handler import PeerObject
from vkbottle.bot import Message
from methods import extract_id
from vkbottle import VKAPIError

async def ban(event: Message, peer_obj: PeerObject):
    if onreply := event.reply_message:
        to_ban = onreply.from_id
    else:
        to_ban = extract_id(event.text, 1)
    if not to_ban:
        await event.answer("🚫Неправильно указан пользователь!")
    else:
        ban_list = peer_obj.data.ban_list
        if str(to_ban) in ban_list.keys():
            await event.answer("🚫Пользователь уже забанен!")
        else:
            try:
                await event.ctx_api.messages.remove_chat_user(event.chat_id, member_id=to_ban)
                peer_obj.data.ban_list[str(to_ban)] = [event.from_id, event.date]
                await peer_obj.save()
                await event.answer("✅Успешно забанен!")
            except VKAPIError[935]:
                await event.answer("🚫Пользователь не состоит в беседе!")