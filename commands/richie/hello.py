from vkbottle.bot import Message
from loader import bot

async def hello(event: Message) -> str:
    await event.answer(f"{(await bot.api.users.get(event.from_id))[0].first_name}, привет из киберпанка")