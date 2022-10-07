from vkbottle import Keyboard, KeyboardButtonColor, Text

marry_keyboard = (
    Keyboard(one_time=False, inline=True)
    .add(Text("Да!!!", payload={"marriage": True}),
        color=KeyboardButtonColor.POSITIVE, 
    )
    .add(Text("Нет...", payload={"marriage": False}),
        color=KeyboardButtonColor.NEGATIVE
    )
).get_json()
