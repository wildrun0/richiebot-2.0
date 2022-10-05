from datatypes import PeerObject, User
from datatypes.user import get_user
from methods.display_coins import display_coins
from methods.display_nicknames import display_nicknames
from vkbottle.bot import Message


async def transfer_richiecoins(event: Message, peer_obj: PeerObject, params: tuple[str, User]):
    amount, to_user = params
    amount = int(amount)
    if amount == 0: return

    me = await get_user(event.from_id, event.peer_id)
    me_peer = me.get_peer(event.peer_id)

    if amount > me_peer.economic.balance:
        await event.answer(f"У вас недостаточно средств для передачи! ({me_peer.economic.balance}<{amount})")
    else:
        me_peer.economic.balance -= amount
        to_user.peers[str(event.peer_id)].economic.balance += amount

        me_nick = me.get_nickname(event.peer_id)
        if not (to_nick := to_user.peers[str(event.peer_id)].nickname):
            to_nick = await display_nicknames(to_user.id, 'dat')

        await to_user.save()
        await me.save()

        await event.answer(
            f"{me_nick} передал{'a' if me.sex == 1 else ''} {display_coins(amount)}  {to_nick}"
        )