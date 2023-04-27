from datatypes import PeerObject
from loader import log
from vkbottle import VKAPIError
from vkbottle.bot import Message


async def renew_users_list(
    event: Message,
    peers_obj: PeerObject,
    params: None = None
) -> tuple[list[int], list[int]]:
    peer_id = event.peer_id
    log.info("USER LIST RENEWAL IN PEER", id=peer_id)
    try:
        chat = await event.ctx_api.messages.get_conversation_members(
            peer_id = peer_id,
            # extended = True,
            fields = ["id", "bdate"]
        )
        chat_users = chat.items
    except VKAPIError[917]:
        log.info("Не могу получить админов в беседе", id=peer_id)
        return [], []

    users = [user.member_id for user in chat_users]
    owner_id = [user.member_id for user in chat_users if user.is_owner][0]
    adms = [user.member_id for user in chat_users if user.is_admin == True]

    peers_obj.data.users = users
    peers_obj.data.admins = adms
    peers_obj.data.owner_id = owner_id

    await peers_obj.save()
    if event.text.lower() == "ричи обновить пользователей":
        await event.answer("Пользователи обновлены")
    return adms, users
