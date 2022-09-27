from datatypes import PeerObject


async def check_banned(member_id: int|str, peer_obj: PeerObject) -> bool:
    if str(member_id) in peer_obj.data.ban_list:
        return True
    else: return False
