import msgspec
from datatypes.clan import Weapon


class ShopItem(msgspec.Struct):
    name: str
    price: int
    obj: Weapon
