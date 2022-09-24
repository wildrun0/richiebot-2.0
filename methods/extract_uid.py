import re


def extract_id(message: str, ids_to_return: int = 1) -> int | list:
    id = [int(s) for s in re.findall(r'\[id(\d+)', message)]
    clubs_ids = [-int(s) for s in re.findall(r'\[club(\d+)', message)]
    all_ids = id + clubs_ids
    if not all_ids:
        return None
    if len(all_ids) == 1 or ids_to_return == 1:
        return all_ids[0]
    return all_ids