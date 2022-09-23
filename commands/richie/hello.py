from vkbottle.bot import Message
from datatypes import user


async def hello(event: Message) -> None:
    usr_nickname = await user.get_users_nickname(event.from_id)
    await event.answer(f"{usr_nickname}, привет из киберпанка")