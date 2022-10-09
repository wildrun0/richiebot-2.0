import msgspec


class ban_info_struct(msgspec.Struct):
    banned_by:    int
    ban_time_str: str

class ban_struct(msgspec.Struct):
    banned_uid: int
    ban_info:   ban_info_struct
