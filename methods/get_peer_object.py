from handlers.peer_handler import PeerObject


peers_objs = {}
def get_peer_object(func):
    async def wrapper(*args, **kwargs):
        if (peer_id:= args[0].peer_id) in peers_objs:
            peer_obj = peers_objs[peer_id]
        else:
            peer_obj = PeerObject(peer_id)
            peers_objs[peer_id] = peer_obj
            await peer_obj.save()
        f = await func(*args, peer_obj, **kwargs)
        return f
    return wrapper