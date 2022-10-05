import textwrap
from dataclasses import fields

from datatypes import PeerObject
from datatypes.user import get_user
from vkbottle.bot import Message


async def inventory(event: Message, peer_obj: PeerObject, params: list[None]):
    inv_user = await get_user(event.from_id, event.peer_id)
    inv_items = inv_user.peers[str(event.peer_id)].inventory
    uinv_name = inv_user.get_nickname(event.peer_id)
    if not inv_items:
        await event.answer(f"{uinv_name}, ваш инвентарь пуст!", disable_mentions=True)
        return
    inv_str = ''
    inv_template = textwrap.dedent("""
        {0.Type.value} {0.name}
        (Урон: {0.dmg} | Исп. ост. = {0.UseLeft})
    """)
    for i in inv_items.__struct_fields__:
        value = getattr(inv_items, i)
        if value != None:
            inv_str += inv_template.format(value)
    await event.answer(f"{uinv_name}, ваши вещи: \n{inv_str}", disable_mentions=True)