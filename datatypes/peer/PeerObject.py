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
        self.default_location = Path(peer_location, self.message_filename)
        if not self.default_location.exists():
            self.messages = MessagesClass()
        else:
            self.messages = msgspec.json.decode(self.default_location.read_bytes(), type=MessagesClass)


    def _check_user(self, user_id: str):
        if user_id not in self.messages.users:
            self.messages.users[user_id] = UserProfile()


    async def write(self, message_text: str, cmid: int, user_id: str, date: float):
        self._check_user(user_id)
        self.messages.users[user_id].messages.append(
            UserMessage(message_text, cmid, date)
        )
        self.messages.users[user_id].messages_count += 1
        self.messages.messages_count += 1

        self.default_location.write_bytes(msgspec.json.encode(self.messages))


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
        logging.info(f"{peer_id} - PEER SETTINGS LOADED")


    async def save(self):
        peer_class = msgspec.json.encode(self.data)
        await AsyncPath(self.obj_file).async_write(peer_class)
        logging.info(f"{self.peer_id} - PEER SETTINGS SAVED")