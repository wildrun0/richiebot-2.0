import msgspec


class ban_pending(msgspec.Struct):
    usr_to_ban: int
    votes:      int
    voted_users:list
