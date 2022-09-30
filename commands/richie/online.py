from vkbottle.bot import Message
from datetime import datetime

from datatypes import PeerObject
from datatypes.user import get_user
from loader import tz


online_status = {
    6121396: "📱VK Admin",
    6287487: "🖥️vk.com",
    2685278: "📱Kate Mobile",
    4083558: "VFeed",
    3140623: "iOS",
    2274003: "📱Android",
    3682744: "iPad",
    3697615: "🖥️Windows (ПК)",
    3502557: "📱Windows Phone",
    3116505: "⚙️VK API",
    None:    "🖥️ПК"
}


async def online(event: Message, peer_obj: PeerObject, param: None) -> None:
    users = (await event.ctx_api.messages.get_conversation_members(
        peer_id = event.peer_id
    )).profiles
    users_online = [x for x in users if x.online]
    online_list = ""
    peer_id = event.peer_id
    for user in users_online:
        if user.id in peer_obj.data.users:
            user_datatype = await get_user(user.id, peer_id)
            name = user_datatype.get_nickname(peer_id)
            online_device = online_status[user.online_app]
            if (info := user.online_info).visible:
                last_seen_date = datetime.fromtimestamp(info.last_seen, tz)
                last_seen = last_seen_date.strftime("%H:%M:%S")
                online_list += f"\n{name} в сети через {online_device} ({last_seen})"
            else:
                online_list += f"\n{name} был недавно (Невидимка)" 
    await event.answer(online_list, disable_mentions=True)