import random
from datatypes import User, PeerObject
from datatypes.user import get_user
from vkbottle.bot import Message


async def who(event: Message, peer_obj: PeerObject, params: tuple[User, str]) -> None:
    who_type = params[1]
    peer_id = event.peer_id
    chosen_user = random.choice(peer_obj.data.users)
    chosen_usertype = await get_user(chosen_user, peer_id)
    await event.answer(
        f"Я считаю что это: {chosen_usertype.get_nickname(peer_id)}"
    )
