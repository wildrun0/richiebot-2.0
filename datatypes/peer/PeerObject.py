import logging
import msgspec

from pathlib import Path
from aiopathlib import AsyncPath

from datatypes.peer import PeerClass
from datatypes.messages import MessagesClass, UserProfile, UserMessage

peers_folder = Path("peers")
peers_folder.mkdir(exist_ok=True)


class Messages():
    def __init__(self, peer_id: int, default_location: AsyncPath, messages: MessagesClass):
        # в этом классе используем msgpack для экономии занимаемого места
        self.peer_id = peer_id
        self.default_location = default_location
        self.messages = messages


    @classmethod
    async def init(self, peer_id: int, peer_location: Path):
        logging.info(f"{peer_id} - INIT MESSAGES")
        message_filename = "messages.dat"
        default_location = AsyncPath(peer_location, message_filename)
        if not await default_location.exists():
            messages = MessagesClass()
        else:
            messages = msgspec.msgpack.decode(
                await default_location.read_bytes(), 
                type=MessagesClass
            )
        logging.info(f"{peer_id} - INIT MESSAGES DONE")
        return Messages(peer_id, default_location, messages)


    def _check_user(self, user_id: str):
        if user_id not in self.messages.users:
            self.messages.users[user_id] = UserProfile()


    async def write(self, message_text: str, cmid: int, user_id: str, date: float, user):
        self._check_user(user_id)
        self.messages.users[user_id].messages.append(
            UserMessage(message_text, cmid, date)
        )
        user.peers[str(self.peer_id)].total_messages += 1
        user.save()
        self.messages.messages_count += 1

        await self.default_location.async_write(msgspec.msgpack.encode(self.messages))


class PeerObject:
    def __init__(self, peer_id: int, obj_file: AsyncPath, data: PeerClass, messages: Messages):
        self.peer_id = peer_id
        self.data = data
        self.obj_file = obj_file
        self.messages = messages


    @classmethod
    async def init(self, peer_id: int):
        logging.info(f"{peer_id} - LOAD PEER SETTINGS")
        peer_json_name = "main.json"
        peer_location = AsyncPath(peers_folder, str(peer_id))
        obj_file = AsyncPath(peer_location, peer_json_name)

        if not (await peer_location.exists()):
            await peer_location.mkdir()
            data = PeerClass()
            await obj_file.async_write(
                msgspec.json.encode(data)
            )
        else:
            data = msgspec.json.decode(await obj_file.read_bytes(), type=PeerClass)
        messages = await Messages.init(peer_id, peer_location)
        logging.info(f"{peer_id} - PEER SETTINGS LOADED")
        return PeerObject(peer_id, obj_file, data, messages)


    async def save(self):
        peer_class = msgspec.json.encode(self.data)
        await self.obj_file.async_write(peer_class)
        logging.info(f"{self.peer_id} - PEER SETTINGS SAVED")