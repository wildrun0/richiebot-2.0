import methods
from datatypes import PeerObject
from datatypes.user import get_user
from datatypes.user import marry_struct
from vkbottle.bot import Message


async def unmarry(event: Message, peer_obj: PeerObject, params: None):
    speer_id = str(event.peer_id)
    caller = await get_user(event.from_id, event.peer_id)
    caller_peer = caller.get_peer(speer_id)
    if (partner_id := caller_peer.marry_with.partner):
        partner = await get_user(partner_id, event.peer_id)
        partner_peer = partner.get_peer(speer_id)
        partner_peer.marry_with = marry_struct()
        caller_peer = marry_struct()

        for marriages in peer_obj.data.marriages.couples:
            if caller.id in marriages:
                peer_obj.data.marriages.couples.remove(marriages)
                break

        await event.answer(f"Вы успешно развелись с {await methods.display_nicknames(partner_id, 'ins')}")
        await caller.save()
        await partner.save()
        await peer_obj.save()
    else:
        await event.answer("🚫Вы не находитесь в браке")
