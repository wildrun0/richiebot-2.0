from datatypes import PeerObject
from datatypes.user import get_user
from loader import bot, ctx_storage, log
from methods.display_coins import display_coins
from settings.config import BENEFIT_AMOUNT

str_benefit_amount = display_coins(BENEFIT_AMOUNT)
async def give_benefits():
    ctx_storage_copy = ctx_storage.storage.copy()
    for peer_obj in list(dict.fromkeys(ctx_storage_copy.values())):
        if isinstance(peer_obj, PeerObject):
            peer_id = peer_obj.peer_id
            speer_id = str(peer_id)
            peer_benefiters = peer_obj.data.benefiters
            for uid in peer_benefiters:
                usr = await get_user(uid, peer_id)
                usr.peers[speer_id].economic.balance += BENEFIT_AMOUNT
                await usr.save()
                log.debug(f"{uid} получил пособие", id=peer_id)
            if peer_benefiters:
                await bot.api.messages.send(
                    peer_id = peer_id,
                    random_id = 0,
                    message = f"{len(peer_benefiters)} человек получило пособие в размере {str_benefit_amount}!"
                )
