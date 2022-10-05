from datatypes import PeerObject
from datatypes.user import get_user
from methods.display_coins import display_coins
from settings.config import BENEFIT_AMOUNT
from vkbottle.bot import Message


async def benefit(event: Message, peer_obj: PeerObject, param: None):
    me = await get_user(event.from_id, event.peer_id)
    me_peer = me.get_peer(event.peer_id)
    
    if me_peer.benefit:
        await event.answer("У вас уже установлено пособие!")
    else:
        me_peer.benefit = True
        peer_obj.data.benefiters.append(me.id)
        me_nickname = me.peers[str(event.peer_id)].nickname
        await event.answer(
            f"{me_nickname if me_nickname else ''}{', вам' if me_nickname else 'Вам'} установлено пособие в размере {display_coins(BENEFIT_AMOUNT)}",
            disable_mentions=True
        )
        await me.save()
        await peer_obj.save()