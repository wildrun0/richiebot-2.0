import logging
import msgspec

from pathlib import Path
from aiopathlib import AsyncPath

from datatypes.peer import PeerClass
from datatypes.messages import MessagesClass, UserProfile, UserMessage

peers_folder = Path("peers")
peers_folder.mkdir(exist_ok=True)


class Messages():
    def __init__(self, peer_location: Path):
        self.message_filename = "messages.json"
        self.default_location = AsyncPath(peer_location, self.message_filename)


    async def _get_peer_messages(self, user_id: str = None) -> MessagesClass:
        if not await self.default_location.exists():
            messages = MessagesClass()
        else:
            messages = msgspec.json.decode(await self.default_location.read_bytes(), type=MessagesClass)
        if user_id not in messages.users:
            messages.users[user_id] = UserProfile()
        return messages


    async def write(self, message_text: str, cmid: int, user_id: str, date: float):
        messages = await self._get_peer_messages(user_id)
        messages.users[user_id].messages.append(
            UserMessage(message_text, cmid, date)
        )
        messages.users[user_id].messages_count += 1
        messages.messages_count += 1

        await self.default_location.async_write(msgspec.json.encode(messages))


class PeerObject:
    def __init__(self, peer_id: int):
        logging.info(f"{peer_id} - LOAD PEER SETTINGS")
        self.peer_json_name = "main.json"
        self.peer_id = peer_id
        self.data = None
        
        self.peer_location = Path(peers_folder, str(self.peer_id))
        self.obj_file = Path(self.peer_location, self.peer_json_name)
        
        if not (peer_dir := self.peer_location).exists():
            peer_dir.mkdir()
            self.data = PeerClass()
            self.obj_file.write_bytes(
                msgspec.json.encode(self.data)
            )
        else:
            self.data = msgspec.json.decode(self.obj_file.read_bytes(), type=PeerClass)
        self.messages = Messages(self.peer_location)


    async def save(self):
        peer_class = msgspec.json.encode(self.data)
        await AsyncPath(self.obj_file).async_write(peer_class)
        logging.info(f"{self.peer_id} PEER SETTINGS SAVED")