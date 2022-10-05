from datatypes import PeerObject
from datatypes.user import get_user
from loader import bot, ctx_storage
from settings.config import BENEFIT_AMOUNT


async def give_benefits():
    for objs in ctx_storage.storage.values():
        if isinstance(objs, PeerObject):
            peer_obj = objs
            peer_id = peer_obj.peer_id
            peer_benefiters = peer_obj.data.benefiters
            for uid in peer_benefiters:
                usr = await get_user(uid, peer_id)
                usr_peer = usr.get_peer(peer_id)
                usr_peer.economic.balance += BENEFIT_AMOUNT
                await usr.save()
            if peer_benefiters:
                await bot.api.messages.send(
                    peer_id = peer_id,
                    random_id = 0,
                    message = f"{len(peer_benefiters)} человек получило пособие!"
                )
