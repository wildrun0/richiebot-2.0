import msgspec
from datatypes.economy import ShopItem
from datatypes.peer.bans import *
from datatypes.peer.casino import *
from datatypes.peer.marriages import *
from datatypes.peer.mutes import *
from datatypes.peer.votebans import *
from datatypes.peer.warns import *


class commands_timeouts_struct(msgspec.Struct, omit_defaults=True):
    clan_duel:int = 300
    roulette:int = 300
    kosti:   int = 300
    casino:  int = 300
    song:    int = 300
    math:    int = 300
    duel:    int = 300


### MAIN STRUCT
class PeerClass(msgspec.Struct, omit_defaults=True):
    owner_id:           int|None = None
    greeting:           str|None = None
    rules:              str|None = None
    admins:             list[int] = []
    users:              list[int] = []
    benefiters:         list[int] = []
    clans:              dict[str, dict]  = {}
    ban_list:           list[ban_struct] = []
    commands_timeouts:  commands_timeouts_struct = commands_timeouts_struct()
    marriages:          marriages_struct         = marriages_struct()
    voteban:            voteban_struct           = voteban_struct()
    warns:              warns_struct             = warns_struct()
    casino:             casino_struct            = casino_struct()
    shop:               list[ShopItem]           = []
    last_kicked:        list[int]                = []
    mute:               list[mute_struct]        = []
