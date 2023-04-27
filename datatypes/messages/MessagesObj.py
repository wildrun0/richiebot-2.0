import sys
import zlib

import msgspec
from anyio import Path
from datatypes.messages import MessagesClass, UserMessage, UserProfile
from datatypes.user import User
from loader import log
from settings.config import DEBUG_STATUS


# в этом классе используем msgpack для экономии занимаемого места
class MessagesObj:
    __slots__ = 'peer_id', 'default_location', 'data'
    def __init__(self, peer_id: str, default_location: Path, data: MessagesClass):
        self.peer_id = peer_id
        self.default_location = default_location
        self.data = data


    @classmethod
    async def init(self, peer_id: str, peer_location: Path):
        log.debug("INIT MESSAGES",id=peer_id)
        message_filename = "messages.dat"
        default_location = Path(peer_location, message_filename)
        if not await default_location.exists():
            messages = MessagesClass()
        else:
            messages = msgspec.msgpack.decode(
                await default_location.read_bytes(),
                type=MessagesClass
            )
        log.debug("INIT MESSAGES DONE",id=peer_id)
        return MessagesObj(peer_id, default_location, messages)


    def _check_user(self, user_id: str):
        if user_id not in self.data.users:
            self.data.users[user_id] = UserProfile()


    async def write(self, message_text: str, cmid: int, user_id: str, date: int, user: User):
        self._check_user(user_id)
        compressed_str = zlib.compress(message_text.encode("utf-8"))
        if DEBUG_STATUS:
            og_string_size, compressed_str_size = sys.getsizeof(message_text), sys.getsizeof(compressed_str)
            compression_percent = round((abs(compressed_str_size - og_string_size) / og_string_size) * 100.0, 2)
            log.debug(f"String compressed {og_string_size} -> {compressed_str_size} ({compression_percent}%)")

        self.data.users[user_id].messages.append(
            UserMessage(compressed_str, cmid, date)
        )
        if user != None:
            user.peers[self.peer_id].total_messages += 1
            await user.save()
        self.data.messages_count += 1
        await self.default_location.write_bytes(msgspec.msgpack.encode(self.data))
