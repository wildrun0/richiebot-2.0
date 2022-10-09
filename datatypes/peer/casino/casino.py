import msgspec


class casino_bet(msgspec.Struct):
    color:    str
    even_bet: bool


class casino_game(msgspec.Struct):
    win_bet: casino_bet
    users:   dict[str, casino_bet] = {}


class casino_struct(msgspec.Struct):
    usrs_to_start: int = 10
    playtime:      int = 300
    game:          casino_game|None = None
