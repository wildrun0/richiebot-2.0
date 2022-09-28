from datatypes.user import get_user


async def get_users_nickname(user_id: int, peer_id: int) -> str:
    user_obj = await get_user(user_id, peer_id)
    if nickname := user_obj.peers[str(peer_id)].nickname:
        return nickname
    else: 
        return user_obj.name