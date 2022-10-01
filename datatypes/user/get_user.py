import msgspec

from aiopathlib import AsyncPath
from datetime import datetime
from loader import TIME_FORMAT, tz, bot, ctx_storage
from datatypes.user import User, set_user, users_folder, peers_struct


async def get_user(user_id: int, peer_id: int) -> User:
    if user_id == 0: return None
    user_data = AsyncPath(users_folder, f"{user_id}.json")
    data = ctx_storage.get(user_id)
    if not data:
        if await user_data.is_file():
            data = msgspec.json.decode(await user_data.read_bytes(), type=User)
        else:
            data = await set_user(user_id, peer_id)
        ctx_storage.set(user_id, data)

    if str(peer_id) not in data.peers:
        peer_users = (await bot.api.messages.get_conversation_members(peer_id)).items
        join_date = [user.join_date for user in peer_users if user.member_id == user_id][0]
        data.peers[str(peer_id)] = peers_struct(
            peer_join_date = datetime.fromtimestamp(join_date, tz).strftime(TIME_FORMAT)
        )
        await data.save()
    return data