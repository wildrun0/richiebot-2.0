from dataclasses import dataclass
from dataclasses_json import dataclass_json

from pathlib import Path
from loader import peers_handler

NAME_TEMPLATE = f"[id%d|%s %s]"

@dataclass_json
@dataclass
class User:
    nickname: str = ""
    name:     str = "[]" # [id1|Павел Дуров]
    sex:      int = 2
    id:       int = 0


DEFAULT_FOLDER = "usersdata"
users_folder = Path(peers_handler.peers_folder, DEFAULT_FOLDER)
if not users_folder.exists():
    users_folder.mkdir()