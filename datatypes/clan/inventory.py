import msgspec
from datatypes.clan import Weapon


class Inventory(msgspec.Struct, omit_defaults=True):
    sword:      Weapon|None = None
    shield:     Weapon|None = None

    helmet:     Weapon|None = None
    chestplate: Weapon|None = None
    leggings:   Weapon|None = None
    boots:      Weapon|None = None