import msgspec
from datatypes.clan import Weapon


class warns_struct(msgspec.Struct, omit_defaults=True):
    max_warns: int = 5
    users: dict[str, int] = {}


class ban_pending(msgspec.Struct):
    usr_to_ban: int
    votes:      int
    voted_users:list


class voteban_struct(msgspec.Struct, omit_defaults=True):
    bans_pending:   list[ban_pending] = []
    min_ban_votes:  int = 10


class marriage_pending(msgspec.Struct):
    user1: int
    user2: int
    offer_start_date: int


class marriages_struct(msgspec.Struct, omit_defaults=True):
    marriages_timeout:  int = 180
    marriages_pending:  list[marriage_pending] = []
    couples:            list[int] = []


class commands_timeouts_struct(msgspec.Struct, omit_defaults=True):
    clan_duel:int = 300
    roulette:int = 300
    who:     int = 300
    infa:    int = 300
    kosti:   int = 300
    casino:  int = 300
    song:    int = 300
    math:    int = 300
    duel:    int = 300


class mute_struct(msgspec.Struct):
    user:        int
    unmute_date: int


class ban_info_struct(msgspec.Struct):
    banned_by:    int
    ban_time_str: str


class ban_struct(msgspec.Struct):
    banned_uid: int
    ban_info:   ban_info_struct


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
    shop:               list[Weapon]             = []
    last_kicked:        list[int]                = []
    mute:               list[mute_struct]        = []