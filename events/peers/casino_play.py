from datatypes import PeerObject
from datatypes.user import get_user
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
        win_money = None
        if bet.color == win_bet.color and bet.even_bet == win_bet.even_bet:
            win_money = bet.price * 1
            usr_peer.economic.balance += win_money
        else:
            usr_peer.economic.balance -= bet.price
        win_str += f"{user.get_nickname(event.peer_id)} {'забирает' if win_money else 'теряет'} {display_coins(win_money)}"
        await user.save()
    await event.answer(
        f"Выпадает комбинация: {win_bet.color.value} {'чет' if win_bet.even_bet else 'нечет'}\n\n{win_str}"
    )
