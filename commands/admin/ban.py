from loader import peers_handler
from vkbottle.bot import Message
from methods import extract_id
from vkbottle import VKAPIError

async def ban(event: Message):
    if onreply := event.reply_message:
        to_ban = onreply.from_id
    else:
        to_ban = extract_id(event.text, 1)
    peer_id = event.peer_id
    if not to_ban:
        await event.answer("🚫Неправильно указан пользователь!")
    else:
        ban_list = await peers_handler.get(peer_id, "ban_list")
        if to_ban in ban_list.keys():
            await event.answer("🚫Пользователь уже забанен!")
        else:
            try:
                await event.ctx_api.messages.remove_chat_user(event.chat_id, member_id=to_ban)
                await peers_handler.add(peer_id, "ban_list", {
                    to_ban: [event.from_id, event.date]
                })
                await event.answer("✅Успешно забанен!")
            except VKAPIError[935]:
                await event.answer("🚫Пользователь не состоит в беседе!")