from random import choice, randint

from datatypes.clan import ARMOR, SWORDS, BOWS, Weapon
from datatypes.clan.weapons import WeaponType
from datatypes.economy import ShopItem


async def gen_weapons(weapon_type: WeaponType, amount: int = 1) -> list[ShopItem]:
    """
    Функция для генерации amount числа вещей (пушек) \n
    Исп. для обновления вещей в магазине бесед
    """
    armor = [
        WeaponType.HELMET, 
        WeaponType.CHESTPLATE, 
        WeaponType.LEGGINGS, 
        WeaponType.BOOTS,
        WeaponType.SHIELD
    ]
    weapon = [
        WeaponType.SWORD,
        WeaponType.BOW
    ]
    if weapon_type in armor:
        w_type = ARMOR
        w_list = armor
    else:
        # w_type = WEAPONS
        w_list = weapon
    w_ico = weapon_type.value
    gen_weapons = []
    for _ in range(amount):
        name = f"{w_ico} {choice(w_type.first)} {choice(w_type.second)} {choice(w_type.third)}"
        price = randint(100, 1000)
        set_weap = Weapon(
            Type = w_type,
            UseLeft = 0,
            dmg = 0.0,
            name = name
        )
        shop_obj = ShopItem(
            name = name,
            price = price, 
            obj = set_weap
        )
        gen_weapons.append(shop_obj)
    return gen_weapons