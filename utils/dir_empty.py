import os


def dir_empty(dir_path: str) -> bool:
    return not next(os.scandir(dir_path), None)