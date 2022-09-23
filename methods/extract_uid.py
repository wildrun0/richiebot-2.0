import re


def extract_id(message: str) -> int:
    id = re.findall(r'-?\d+', message)
    if not id: return False
    is_club = re.findall(r'\[club(.+)\|(.+)\]', message)
    if is_club:
        return -int(is_club[0][0])
    return int(id[0])