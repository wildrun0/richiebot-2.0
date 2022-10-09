import textwrap
from random import choice, getrandbits

from datatypes import PeerObject
from datatypes.peer import casino_bet, casino_game
from loader import bot
from tasks.functions import check_casino
from vkbottle.bot import Message

colors = ["красное", "черное", 'зеленое']

async def casino(event: Message, peer_obj: PeerObject, params):
    if peer_obj.data.casino.game:
        await event.answer("Казино уже запущено!")
    else:
        win_bet = casino_bet(
            color = choice(colors), 
            even_bet = bool(getrandbits(1))
        )
        game = casino_game(
            win_bet = win_bet,
        )
        peer_obj.data.casino.game = game

        casino_timeout = 5

        bot.loop.create_task(
            check_casino(event.peer_id, casino_timeout)
        )

        await event.answer(textwrap.dedent(f"""
        Добро пожаловать в казино!
        Принимаются ставки: черное/красное/зеленое чет/нечет *сумма*
        Например: черное чет 100, где 100 - сумма ричсонов

        Коэффиценты: зеленое чет - х10, зеленое нечет - х3, красное чет - х1.75, красное нечет - х1.5, черное чет - х1.25, черное нечет - х1.10

        Чтобы сделать ставку, воспользуйтесь кнопками или напишите ставку(пример: красное чет 1000)
        """))
