from enum import Enum

import msgspec


class WeaponType(Enum):
    SWORD      = '🗡️'
    BOW        = '🏹'

    SHIELD     = "🛡️"
    HELMET     = '⛑️'
    CHESTPLATE = '🦺'
    LEGGINGS   = "👖"
    BOOTS      = "🥾"


class Weapon(msgspec.Struct):
    Type:   WeaponType
    UseLeft:int
    dmg:    float
    name:   str
