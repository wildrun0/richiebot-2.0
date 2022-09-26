import logging
from vkbottle.bot import Message
from handlers import PeerObject
from vkbottle import VKAPIError


async def renew_users_list(event: Message, peers_obj: PeerObject, params: None = None) -> tuple[list[int], list[int]]:
    logging.info(f"USER LIST RENEWAL IN PEER {event.peer_id}")
    try:
        users = (await event.ctx_api.messages.get_conversation_members(event.peer_id))
    except VKAPIError[917]: 
        logging.info(f"Не могу получить админов в беседе {event.peer_id}")
        return [], []

    usrs = [x.member_id for x in users.items]
    adms = list(filter(None, [x.is_admin and x.member_id for x in users.items]))

    peers_obj.data.users = usrs
    peers_obj.data.admins = adms

    await peers_obj.save()
    if params: await event.answer("Пользователи обновлены")
    return adms, users