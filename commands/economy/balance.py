from datatypes import PeerObject, User
from datatypes.user import get_user
from methods.display_coins import display_coins
from vkbottle.bot import Message


async def balance(event: Message, peer_obj: PeerObject, param: list[User|None]):
    balance_user = param[0] or await get_user(event.from_id, event.peer_id)
    balance = balance_user.peers[str(event.peer_id)].economic.balance
    if balance_user.id == event.from_id:
        await event.answer(f"Ваш баланс составляет: {display_coins(balance)}")
    else:
        balanced_user_nickname = balance_user.get_nickname(event.peer_id)
        await event.answer(
            f"Баланс пользователя {balanced_user_nickname} составляет {display_coins(balance)}",
            disable_mentions = True
        )