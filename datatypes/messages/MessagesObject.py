import zlib
import sys
import logging
import msgspec

from pathlib import Path
from aiopathlib import AsyncPath
from datatypes.messages import MessagesClass, UserProfile, UserMessage

class MessagesObj():
    __slots__ = 'peer_id', 'default_location', 'messages'
    def __init__(self, peer_id: str, default_location: AsyncPath, messages: MessagesClass):
        self.peer_id = peer_id
        self.default_location = default_location
        self.messages = messages


    @classmethod
    async def init(self, peer_id: str, peer_location: Path):
        logging.debug(f"{peer_id} - INIT MESSAGES")
        message_filename = "messages.dat"
        default_location = AsyncPath(peer_location, message_filename)
        if not await default_location.exists():
            messages = MessagesClass()
        else:
            messages = msgspec.msgpack.decode(
                await default_location.read_bytes(), 
                type=MessagesClass
            )
        logging.debug(f"{peer_id} - INIT MESSAGES DONE")
        return MessagesObj(peer_id, default_location, messages)


    def _check_user(self, user_id: str):
        if user_id not in self.messages.users:
            self.messages.users[user_id] = UserProfile()


    async def write(self, message_text: str, cmid: int, user_id: str, date: float, user):
        self._check_user(user_id)
        compressed_str = zlib.compress(message_text.encode("utf-8"))
        
        og_string_size, compressed_str_size = sys.getsizeof(message_text), sys.getsizeof(compressed_str)
        compression_percent = round((abs(compressed_str_size - og_string_size) / og_string_size) * 100.0, 2)
        logging.debug(f"String compressed {og_string_size} -> {compressed_str_size} ({compression_percent}%)")
        
        self.messages.users[user_id].messages.append(
            UserMessage(compressed_str, cmid, date)
        )
        user.peers[self.peer_id].total_messages += 1
        await user.save()
        self.messages.messages_count += 1

        await self.default_location.async_write(msgspec.msgpack.encode(self.messages))