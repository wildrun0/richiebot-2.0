from datatypes.peer.casino import CasinoColors
from vkbottle import Keyboard, KeyboardButtonColor, Text

casino_keyboard = (
    Keyboard(one_time=False, inline=True)
    .add(Text("черное чет 100", payload={
        "color": CasinoColors.BLACK,
        "even_bet": True,
        "price": 100
    }),
        color=KeyboardButtonColor.PRIMARY, 
    )
    .add(Text("красное нечет 50", payload={
        "color": CasinoColors.RED,
        "even_bet": False,
        "price": 50
    }),
        color=KeyboardButtonColor.PRIMARY
    )
    .add(Text("зеленое нечет 150", payload={
        "color": CasinoColors.GREEN,
        "even_bet": False,
        "price": 150
    }),
        color=KeyboardButtonColor.PRIMARY
    )
).get_json()
