import logging
from vkbottle.bot import Message
from handlers.peer_handler import PeerObject
from vkbottle import VKAPIError


async def renew_admin_list(event: Message, peers_obj: PeerObject, params: None = None) -> list[int]:
    try:
        admins = (await event.ctx_api.messages.get_conversation_members(event.peer_id))
    except VKAPIError[917]: 
        logging.debug(f"Не могу получить админов в беседе {event.peer_id}")
        return []
    adms = list(filter(None, [x.is_admin and x.member_id for x in admins.items]))
    peers_obj.data.admins = adms
    await peers_obj.save()
    return adms