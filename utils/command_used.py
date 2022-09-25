import re
import itertools
from aiocache import cached


@cached(ttl=300)
async def command_used(lists: tuple, text: str, check_call: bool = False) -> tuple[str, tuple, int] | bool:
    from datatypes.user import get_user
    if check_call:
        for notfull, full in itertools.zip_longest(*lists):
            if notfull:
                if re.findall(notfull, text):
                    return True
            if full:
                if full == text:
                    return True
        return False
    else:
        for notfull, full in itertools.zip_longest(*lists):
            if notfull:
                if matches := re.findall(notfull, text):
                    args = list(*matches) if isinstance(*matches, tuple) else matches
                    if "\[(?:(id|club))(\d+)\|.+\]" in notfull:
                        try:
                            id = -int(args[1]) if args[0] == "club" else int(args[1])
                            args = (await get_user(id), args[2:])
                        except ValueError: pass
                    return notfull, args, 0
            if full:
                if full == text:
                    return full, "", 1