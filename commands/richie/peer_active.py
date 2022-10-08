from datetime import datetime

from datatypes import PeerObject
from datatypes.user import get_user
from loader import tz
from vkbottle.bot import Message


async def peer_active(event: Message, peer_obj: PeerObject, param: None):
    curr_time = datetime.timestamp(datetime.now(tz))
    u_msgs = peer_obj.messages.data.users

    day_msgs = {}
    for profile, msg in u_msgs.items():
        uid = int(profile)
        u_day_msgs = [
            message
            for message in msg.messages
            if (curr_time - message.date) <= 86400
        ]
        uid_nickname = (
            await get_user(uid, event.peer_id)
        ).get_nickname(event.peer_id)

        day_msgs[uid_nickname] = len(u_day_msgs)

    sorted_active = dict(
        sorted(day_msgs.items(), key=lambda item: item[1], reverse=True)
    )
    top5_usrs = list(sorted_active.items())[:5]

    top5_usrs_str = ''
    for nick, len_msgs in top5_usrs:
        top5_usrs_str += f"{nick}: {len_msgs}\n"

    await event.answer(
        f"Топ 5 активных пользователей по сообщениям:\n{top5_usrs_str}", 
        disable_mentions = True
    )
