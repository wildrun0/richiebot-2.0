from pathlib import Path as SyncPath

import msgspec
from anyio import Path
from datatypes.clan import Inventory
from settings.config import PEERS_DEFAULT_FOLDER

NAME_TEMPLATE = "[%s%d|%s %s]"
DEFAULT_FOLDER = "usersdata"


class peer_achievments(msgspec.Struct, omit_defaults=True):
    kosti_wins:     int = 0
    math_solved:    int = 0
    duels_winned:   int = 0


class timeout_struct(msgspec.Struct, omit_defaults=True):
    due_date:       int
    shadowbanned:   bool = False


class marry_struct(msgspec.Struct, omit_defaults=True):
    partner:    int|None = None
    start_date: int|None = None


class peers_struct(msgspec.Struct, omit_defaults=True):
    peer_join_date: str
    nickname:       str = "" # [id1|Пашок]
    balance:        int = 0
    voice_messages: int = 0
    total_messages: int = 0
    total_warns:    int = 0
    photos_sent:    int = 0
    timeouts:       dict[str, timeout_struct] = {}
    inventory:      Inventory        = Inventory()
    marry_with:     marry_struct     = marry_struct()
    achievments:    peer_achievments = peer_achievments()


class User(msgspec.Struct, omit_defaults=True):
    name:       str = "" # [id1|Павел Дуров]
    sex:        int = 0  # 0 = не указан, 1 - жен, 2 - муж.
    id:         int = 0  # 320750004
    peers:      dict[str, peers_struct] = {}


    async def save(self):
        fp = Path(users_folder, f"{self.id}.json")
        await fp.write_bytes(msgspec.json.encode(self))

    
    def get_nickname(self, peer_id: str|int) -> str:
        if peer_nickname := self.peers[str(peer_id)].nickname:
            return peer_nickname
        else: return self.name


users_folder = SyncPath(PEERS_DEFAULT_FOLDER, DEFAULT_FOLDER)

if not users_folder.exists():
    from loader import logger
    logger.warning(f"{PEERS_DEFAULT_FOLDER}/{DEFAULT_FOLDER} not found. Creating a new one")
    users_folder.mkdir()
