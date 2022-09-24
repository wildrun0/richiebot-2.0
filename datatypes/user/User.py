import msgspec

from pathlib import Path
from handlers.peer_handler import peers_folder

NAME_TEMPLATE = "[id%d|%s %s]"
DEFAULT_FOLDER = "usersdata"


class User(msgspec.Struct):
    nickname: str = ""   # Пашка Дуров
    name:     str = "[]" # [id1|Павел Дуров]
    sex:      int = 0    # 0 = не указан, 1 - жен, 2 - муж.
    id:       int = 0    # 320750004


if not (users_folder := Path(peers_folder, DEFAULT_FOLDER)).exists():
    import logging
    logging.warning(f"{peers_folder}/{DEFAULT_FOLDER} not found. Creating a new one")
    users_folder.mkdir()