from aiocache import cached
import itertools


@cached(ttl=300)
async def command_used(lists: tuple, text: str, check_call: bool = False) -> tuple | bool:
    if check_call:
        for notfull, full in itertools.zip_longest(*lists):
            if notfull:
                if text.startswith(notfull):
                    return True
            if full:
                if full == text:
                    return True
    else:
        for i in enumerate(map(lambda b: map(text.startswith, b), lists)):
            commands_indexes = list(i[1])
            idx = i[0]
            if True in commands_indexes:
                return lists[idx][commands_indexes.index(True)], idx
    return False