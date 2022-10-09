import msgspec


class mute_struct(msgspec.Struct):
    user:        int
    unmute_date: int
