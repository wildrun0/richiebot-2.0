import msgspec


class warns_struct(msgspec.Struct):
    max_warns: int = 5
    users: dict[str, int] = {}


class voteban_struct(msgspec.Struct):
    bans_pending:   list[int] = []
    min_ban_votes:  int = 10


class marriages_struct(msgspec.Struct):
    marriages_timeout:  int = 180
    marriages_pending:  list[int] = []
    couples:            list[int] = []


class commands_timeouts_struct(msgspec.Struct):
    richie_clan_duel:int = 300
    richie_roulette:int = 300
    richie_who_whom:int = 300
    richie_infa:    int = 300
    richie_kosti:   int = 300
    richie_casino:  int = 300
    richie_song:    int = 300
    richie_primer:  int = 300
    richie_duel:    int = 300


class PeerClass(msgspec.Struct):
    greeting:           str|None = None
    rules:              str|None = None
    admins:             list[int] = []
    users:              list[int] = []
    clans:              dict[str, dict] = {}
    ban_list:           dict[str, list] = {}
    commands_timeouts:  commands_timeouts_struct = {}
    marriages:          marriages_struct = {}
    voteban:            voteban_struct = {}
    last_kicked:        list[int] = []
    warns:              warns_struct = {}
    mute:               list[tuple[int, float]] = []