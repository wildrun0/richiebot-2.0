from datatypes import PeerObject
from datatypes.user import get_user
from datatypes.peer.casino import get_casino_ratio
from methods import display_coins
from vkbottle.bot import Message


async def casino_play(event: Message, peer_obj: PeerObject):
    casino_users = peer_obj.data.casino.game.users
    win_bet = peer_obj.data.casino.game.win_bet
    speer_id = str(event.peer_id)
    win_str = ''
    for uid, bet in casino_users.items():
        user = await get_user(int(uid), event.peer_id)
        usr_peer = user.get_peer(speer_id)
        win_money = bet.price
        if bet.color == win_bet.color and bet.even_bet == win_bet.even_bet:
            win_money = bet.price * get_casino_ratio(bet)
            usr_peer.economic.balance += win_money
        else:
            usr_peer.economic.balance -= bet.price
        win_str += f"{user.get_nickname(event.peer_id)} {'забирает' if win_money != bet.price else 'теряет'} {display_coins(win_money)}\n"
        await user.save()
    await event.answer(
        f"Выпадает комбинация: {win_bet.color.value} {'чет' if win_bet.even_bet else 'нечет'}\n\n{win_str}"
    )
    peer_obj.data.casino.game = None
    await peer_obj.save()
