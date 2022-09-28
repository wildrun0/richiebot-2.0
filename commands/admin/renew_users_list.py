import logging
from vkbottle.bot import Message
from datatypes import PeerObject
from vkbottle import VKAPIError


async def renew_users_list(event: Message, peers_obj: PeerObject, params: None = None) -> tuple[list[int], list[int]]:
    peer_id = event.peer_id
    logging.info(f"{peer_id} - USER LIST RENEWAL IN PEER")
    try:
        chat = await event.ctx_api.messages.get_conversations_by_id(peer_id, extended=True, fields=["id", "bdate"])
    except VKAPIError[917]: 
        logging.info(f"{peer_id} - Не могу получить админов в беседе")
        return [], []
    users = [user.id for user in chat.profiles]
    adms = chat.items[0].chat_settings.admin_ids

    peers_obj.data.users = users
    peers_obj.data.admins = adms

    await peers_obj.save()
    if params: await event.answer("Пользователи обновлены")
    return adms, users