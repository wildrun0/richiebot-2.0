import random

from datatypes import PeerObject
from vkbottle.bot import Message

infa_answers = [
    "Мне кажется что инфа достоверна на: %d%%",
    "На мой взгляд инфа достоверна на: %d%%",
    "Ну я считаю инфа достоверна на: %d%%",
    "Я думаю что инфа достоверна на: %d%%"
]


async def infa(event: Message, peer_obj: PeerObject, params: list[str|None]):
    rand_percent = random.randint(0, 100)
    rand_str: str = random.choice(infa_answers)
    await event.answer(rand_str % rand_percent)