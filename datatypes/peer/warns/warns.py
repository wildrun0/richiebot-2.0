import msgspec


class warns_struct(msgspec.Struct, omit_defaults=True):
    max_warns: int = 5
    users: dict[str, int] = {}
