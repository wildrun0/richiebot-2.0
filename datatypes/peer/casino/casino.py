import msgspec
from datatypes.peer.casino.casino_enum import CasinoColors


class casino_bet(msgspec.Struct):
    color:    CasinoColors
    even_bet: bool
    price:    int|None


class casino_game(msgspec.Struct):
    win_bet: casino_bet
    users:   dict[str, casino_bet] = {}


class casino_struct(msgspec.Struct):
    usrs_to_start: int = 2
    playtime:      int = 300
    game:          casino_game|None = None
