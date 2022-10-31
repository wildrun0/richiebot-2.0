from datatypes import PeerObject
from vkbottle.bot import Message


async def muted(event: Message, peer_obj: PeerObject) -> bool:
    muted = [muted for muted in peer_obj.data.mute if muted.user == event.from_id]
    if muted:
        mute_obj = muted[0]
        if event.date > mute_obj.unmute_date:
            obj_index = peer_obj.data.mute.index(mute_obj)
            del peer_obj.data.mute[obj_index]
            await peer_obj.save()
            return False
        else:
            return True
    else:
        return False