import msgspec

from pathlib import Path
from aiopathlib import AsyncPath
from datatypes.messages import MessagesObj
from datatypes.peer import PeerClass
from loader import logger

peers_folder = Path("peers")
peers_folder.mkdir(exist_ok=True)


class PeerObject:
    __slots__ = 'peer_id', 'data', 'obj_file', 'messages'
    def __init__(self, peer_id: int, obj_file: AsyncPath, data: PeerClass, messages: MessagesObj):
        self.peer_id = peer_id
        self.data = data
        self.obj_file = obj_file
        self.messages = messages


    @classmethod
    async def init(self, peer_id: int):
        logger.info("LOAD PEER SETTINGS", id=peer_id)
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
        messages = await MessagesObj.init(str(peer_id), peer_location)
        logger.info("PEER SETTINGS LOADED", id=peer_id)
        return PeerObject(peer_id, obj_file, data, messages)


    async def save(self):
        peer_class = msgspec.json.encode(self.data)
        await self.obj_file.async_write(peer_class)
        logger.info("PEER SETTINGS SAVED", id=self.peer_id)