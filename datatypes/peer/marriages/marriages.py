import msgspec


class marriage_pending(msgspec.Struct):
    user1: int
    user2: int
    offer_start_date: int


class marriages_struct(msgspec.Struct, omit_defaults=True):
    marriages_timeout:  int = 180
    marriages_pending:  list[marriage_pending] = []
    couples:            list[tuple[int, int]] = []
