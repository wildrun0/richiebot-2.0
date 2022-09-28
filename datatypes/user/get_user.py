import msgspec

from aiopathlib import AsyncPath
from datetime import datetime
from loader import TIME_FORMAT, tz, bot
from datatypes.user import User, set_user, users_folder, peers_struct


async def get_user(user_id: int, peer_id: int) -> User:
    if user_id == 0: return None
    user_data = AsyncPath(users_folder, f"{user_id}.dat")

    if await user_data.is_file():
        data = msgspec.json.decode(await user_data.read_bytes(), type=User)
    else:
        data = await set_user(user_id, peer_id)
    if str(peer_id) not in data.peers:
        peer_users = (await bot.api.messages.get_conversation_members(peer_id)).items
        join_date = [date for date in [user.member_id == user_id and user.join_date for user in peer_users] if date != False][0]
        data.peers[str(peer_id)] = peers_struct(
            peer_join_date = datetime.fromtimestamp(join_date, tz).strftime(TIME_FORMAT)
        )
        data.save()
    return data