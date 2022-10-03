from anyio import Path
from commands.admin import renew_users_list
from datatypes import PeerObject
from datatypes.messages import MessagesClass
from datatypes.peer import PeerClass
from vkbottle.bot import Message


async def reset_bot_peer(event: Message, peer_obj: PeerObject, params: None):
    data = PeerClass()
    peer_obj.data = data
    await renew_users_list(event, peer_obj)
    
    peer_obj.messages.data = MessagesClass()
    await Path(peer_obj.messages.default_location).write_bytes(b'')

    await event.answer("Настройки беседы очищены!")