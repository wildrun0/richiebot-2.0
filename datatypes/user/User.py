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


class economic_struct(msgspec.Struct, omit_defaults=True):
    balance:   int       = 0
    exp:       int       = 0
    inventory: Inventory = Inventory()


class peers_struct(msgspec.Struct, omit_defaults=True):
    peer_join_date: str
    nickname:       str = "" # [id1|Пашок]
    voice_messages: int = 0
    total_messages: int = 0
    total_warns:    int = 0
    photos_sent:    int = 0
    benefit:        bool = False
    timeouts:       dict[str, timeout_struct] = {}
    economic:       economic_struct  = economic_struct()
    marry_with:     marry_struct     = marry_struct()
    achievments:    peer_achievments = peer_achievments()


    def get_strength(self) -> int:
        total_power = 0
        inv_items = self.economic.inventory
        for prop_name in inv_items.__struct_fields__:
            prop = getattr(inv_items, prop_name)
            if prop != None:
                total_power += prop.dmg
        return total_power


class User(msgspec.Struct, omit_defaults=True):
    name:       str = "" # [id1|Павел Дуров]
    sex:        int = 0  # 0 = не указан, 1 - жен, 2 - муж.
    id:         int = 0  # 320750004
    stamina:    float = 10.0
    peers:      dict[str, peers_struct] = {}


    async def save(self):
        fp = Path(users_folder, f"{self.id}.json")
        await fp.write_bytes(msgspec.json.encode(self))


    def get_nickname(self, peer_id: str|int) -> str:
        if peer_nickname := self.peers[str(peer_id)].nickname:
            return peer_nickname
        else: return self.name


    def get_peer(self, peer_id: str|int) -> peers_struct:
        return self.peers[str(peer_id)]



users_folder = SyncPath(PEERS_DEFAULT_FOLDER, DEFAULT_FOLDER)

if not users_folder.exists():
    from loader import log
    log.warning(f"{PEERS_DEFAULT_FOLDER}/{DEFAULT_FOLDER} not found. Creating a new one")
    users_folder.mkdir()
