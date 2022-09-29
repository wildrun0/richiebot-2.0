from vkbottle.bot import Message
from loader import bot
from datatypes import PeerObject, User


async def about(event: Message, peer_obj: PeerObject, params: tuple[User, str]):
    await event.answer(f"""
        Бот Ричи (2 итерация). Дата начала разработки - 18.06.2022
        Репозиторий на Github - https://github.com/wildrun0/richiebot-2.0/
        Создатели - [id397717739|wildrun0] и [id320750004|tgwalker]
        Ментор - [id264056124|Долбаеб] (он сам так попросил)
        Также посетите нашу группу в ВК, там много новостей! :)
    """, disable_mentions=True)