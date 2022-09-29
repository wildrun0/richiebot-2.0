from datatypes import user
from vkbottle.bot import Message


async def hello(event: Message, peer_obj, params) -> None:
    usr = await user.get_user(event.from_id, event.peer_id)
    await event.answer(f"{usr.get_nickname(event.peer_id)}, привет из киберпанка", disable_mentions=True)