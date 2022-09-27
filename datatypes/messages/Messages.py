import msgspec


class UserMessage(msgspec.Struct):
    message_text: str
    cmid: int
    date: float


class UserProfile(msgspec.Struct):
    messages_count: int = 0
    messages: list[UserMessage] = []


class MessagesClass(msgspec.Struct):
    users: dict[str, UserProfile] = {}
    messages_count: int = 0