import msgspec

from pathlib import Path
from datatypes.peer import peers_folder

NAME_TEMPLATE = "[%s%d|%s %s]"
DEFAULT_FOLDER = "usersdata"


class peer_achievments(msgspec.Struct):
    kosti_wins:     int = 0
    math_solved:    int = 0
    duels_winned:   int = 0


class peers_struct(msgspec.Struct):
    peer_join_date: str
    voice_messages: int = 0
    total_messages: int = 0
    photos_sent:    int = 0
    achievments:    peer_achievments = {}
    nickname:       str = "" # [id1|Пашок]


class User(msgspec.Struct, omit_defaults=True):
    name:       str = "" # [id1|Павел Дуров]
    sex:        int = 0  # 0 = не указан, 1 - жен, 2 - муж.
    id:         int = 0  # 320750004
    peers:      dict[str, peers_struct] = {}

    def save(self):
        fp = Path(users_folder, f"{self.id}.json")
        fp.write_bytes(msgspec.json.encode(self))


users_folder = Path(peers_folder, DEFAULT_FOLDER)

if not users_folder.exists():
    import logging
    logging.warning(f"{peers_folder}/{DEFAULT_FOLDER} not found. Creating a new one")
    users_folder.mkdir()