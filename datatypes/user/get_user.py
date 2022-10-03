from datetime import datetime

import msgspec
from anyio import Path
from datatypes.user import User, peers_struct, set_user, users_folder
from loader import TIME_FORMAT, bot, ctx_storage, tz


async def get_user(user_id: int, peer_id: int) -> User:
    user_data = Path(users_folder, f"{user_id}.json")
    data = ctx_storage.get(user_id)
    if not data:
        if await user_data.is_file():
            data = msgspec.json.decode(await user_data.read_bytes(), type=User)
        else:
            data = await set_user(user_id, peer_id)
        ctx_storage.set(user_id, data)
    if (speer_id := str(peer_id)) not in data.peers:
        peer_users = (await bot.api.messages.get_conversation_members(peer_id)).items
        join_date = [user.join_date for user in peer_users if user.member_id == user_id][0]
        data.peers[speer_id] = peers_struct(
            peer_join_date = datetime.fromtimestamp(join_date, tz).strftime(TIME_FORMAT)
        )
        await data.save()
    return data