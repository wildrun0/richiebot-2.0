import re


def extract_id(message: str) -> int | list:
    id = [int(s) for s in re.findall(r'\[id(\d+)', message)]
    clubs_ids = [-int(s) for s in re.findall(r'\[club(\d+)', message)]
    all_ids = id + clubs_ids
    if len(all_ids) == 1:
        return all_ids[0]
    return all_ids