from enum import Enum

import msgspec


class WeaponType(Enum):
    SHIELD     = "🛡️"
    SWORD      = '🗡️'
    HELMET     = '⛑️'
    CHESTPLATE = '🦺'
    LEGGINGS   = "👖"
    BOOTS      = "🥾"


class Weapon(msgspec.Struct):
    Type:   WeaponType
    UseLeft:int
    dmg:    float
    name:   str