from loader import logger
from vkbottle.bot import Message
from datatypes import PeerObject
from vkbottle import VKAPIError


async def renew_users_list(event: Message, peers_obj: PeerObject, params: None = None) -> tuple[list[int], list[int]]:
    peer_id = event.peer_id
    logger.info("USER LIST RENEWAL IN PEER", id=peer_id)
    try:
        chat = await event.ctx_api.messages.get_conversations_by_id(peer_id, extended=True, fields=["id", "bdate"])
    except VKAPIError[917]: 
        logger.info("Не могу получить админов в беседе", id=peer_id)
        return [], []
    users = [user.id for user in chat.profiles]
    if chat.groups:
        users = users + [-bot.id for bot in chat.groups]
    adms = chat.items[0].chat_settings.admin_ids
    adms.append(chat.items[0].chat_settings.owner_id)
    
    peers_obj.data.users = users
    peers_obj.data.admins = adms

    await peers_obj.save()
    if params: await event.answer("Пользователи обновлены")
    return adms, users