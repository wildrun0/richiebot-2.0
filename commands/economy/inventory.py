import textwrap

from datatypes import PeerObject
from datatypes.clan.weapons import Weapon, WeaponType
from datatypes.user import get_user
from vkbottle.bot import Message


async def inventory(event: Message, peer_obj: PeerObject, params: None):
    inv_user = await get_user(event.from_id, event.peer_id)
    uinv_name = inv_user.get_nickname(event.peer_id)
    uinv_peer = inv_user.get_peer(event.peer_id)
    
    inv_items = uinv_peer.economic.inventory
    # inv_items.sword = Weapon(WeaponType.SWORD, 10, 12.28, "Меч пиздатый")
    # inv_items.boots = Weapon(WeaponType.BOOTS, 10, 1, "Ботинки ахуенные")

    if not inv_items:
        await event.answer(f"{uinv_name}, ваш инвентарь пуст!", disable_mentions=True)
        return
    total_power = uinv_peer.get_strength()
    inv_str = f'💪Суммарная сила: {total_power}\n'
    inv_template = textwrap.dedent("""
        {1}. {0.Type.value} {0.name}
        (Урон: {0.dmg} | Исп. ост. = {0.UseLeft})\n
    """)
    for enum, i in enumerate(inv_items.__struct_fields__):
        value = getattr(inv_items, i)
        if value != None:
            inv_str += inv_template.format(value, enum)
    await event.answer(
        f"{uinv_name}, ваши вещи: \n{inv_str}", 
        disable_mentions=True
    )
