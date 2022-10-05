import msgspec
from datatypes.clan import Weapon


class economic_struct(msgspec.Struct, omit_defaults = True):
    benefit:    int = 0
    shop_items: list[Weapon] = []