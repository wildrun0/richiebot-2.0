from datatypes import user
from vkbottle.bot import Message


async def hello(event: Message, peer_obj, params) -> None:
    usr_nickname = await user.get_users_nickname(event.from_id, event.peer_id)
    await event.answer(f"{usr_nickname}, привет из киберпанка", disable_mentions=True)