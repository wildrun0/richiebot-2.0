import msgspec
from datatypes.clan import Weapon


class Inventory(msgspec.Struct, omit_defaults=True):
    SWORD:      Weapon|None = None
    SHIELD:     Weapon|None = None

    HELMET:     Weapon|None = None
    CHESTPLATE: Weapon|None = None
    LEGGINGS:   Weapon|None = None
    BOOTS:      Weapon|None = None
