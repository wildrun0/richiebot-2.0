import random

from datatypes import PeerObject
from datatypes.user import get_user
from methods.decorators import timeout_manager
from vkbottle.bot import Message

answers = [
    "Я считаю что это: {}",
    "На мой личный роботизированный взгляд это: {}",
    "Великий рандом говорит что это: {}",
    "Имхо это: {}",
    "На мой взгляд это: {}"
]


async def who(event: Message, peer_obj: PeerObject, params: list[str]) -> None:
    try:
        who_type = params[0]
    except: who_type = ""
    peer_id = event.peer_id
    chosen_user = random.choice(peer_obj.data.users)
    chosen_usertype = await get_user(chosen_user, peer_id)
    await event.answer(
        random.choice(answers).format(chosen_usertype.get_nickname(peer_id)),
        disable_mentions=True
    )