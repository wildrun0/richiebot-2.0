from datatypes import PeerObject
from datatypes.clan.weapons import WeaponType
from datatypes.user import get_user
from vkbottle.bot import Message


async def inventory(event: Message, peer_obj: PeerObject, params: None):
    inv_user = await get_user(event.from_id, event.peer_id)
    uinv_name = inv_user.get_nickname(event.peer_id)
    uinv_peer = inv_user.get_peer(event.peer_id)

    inv_items = uinv_peer.economic.inventory

    if not inv_items:
        await event.answer(f"{uinv_name}, ваш инвентарь пуст!", disable_mentions=True)
        return    

    item_template      = "{0}. {1.value} {2}\n"
    item_spec_template = "(Урон: {0.dmg} | Прочность: {0.UseLeft})\n"
    inv_str            = ''
    
    for enum, i in enumerate(inv_items.__struct_fields__):
        value = getattr(inv_items, i)
        weap_type = getattr(WeaponType, i)
        weapon_name = 'Отсутствует' if value is None else value.name
        inv_str += item_template.format(enum + 1, weap_type, weapon_name)
        if value: 
            inv_str += item_spec_template.format(value)
    await event.answer(
        f"{uinv_name}, ваши вещи: \n\n{inv_str}\n💪Суммарная сила: {uinv_peer.get_strength()}", 
        disable_mentions=True
    )
