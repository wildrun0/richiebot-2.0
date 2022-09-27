from vkbottle.bot import Message
from datatypes import PeerObject


async def check_muted(event: Message, peer_obj: PeerObject) -> bool:
    if event.from_id in [mute_tuple[0] for mute_tuple in peer_obj.data.mute]:
        usr_mute_pos = [i for i, v in enumerate(peer_obj.data.mute) if v[0] == event.from_id][0]
        timeout = peer_obj.data.mute[usr_mute_pos][1]
        if event.date > timeout:
            del peer_obj.data.mute[usr_mute_pos]
            await peer_obj.save()
            return False
        else:
            return True
    else:
        return False