from datatypes.user import get_user


async def get_users_nickname(user_id: int) -> str:
    user_obj = await get_user(user_id)
    if nickname := user_obj.nickname:
        return f"[id{user_obj.id}|{nickname}"
    else: 
        return user_obj.name