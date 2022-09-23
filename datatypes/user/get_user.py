from aiopathlib import AsyncPath
from datatypes.user import User, set_user, users_folder
from aiocache import cached


cached_users = {}

@cached(ttl=120)
async def get_user(user_id: int) -> User:
    if user_id in cached_users: return cached_users[user_id]
    user_data = AsyncPath(users_folder, f"{user_id}.dat")

    if await user_data.is_file():
        data = User.from_dict(
            await user_data.read_json(encoding="utf8")
        )
    else:
        data = await set_user(user_id)

    cached_users[user_id] = data
    return data