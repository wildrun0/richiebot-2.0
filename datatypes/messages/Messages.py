import msgspec


class UserMessage(msgspec.Struct, array_like=True):
    message_text: bytes
    cmid: int
    date: int


class UserProfile(msgspec.Struct, array_like=True, omit_defaults=True):
    messages: list[UserMessage] = []


class MessagesClass(msgspec.Struct, array_like=True, omit_defaults=True):
    users: dict[str, UserProfile] = {}
    messages_count: int = 0