import re
import itertools

from aiocache import cached
from handlers.peer_handler import PeerObject


@cached(ttl=300)
async def command_used(lists: tuple, text: str, peer_object: PeerObject) -> tuple[str, tuple, int] | bool:
    from datatypes.user import get_user
    for notfull, full in itertools.zip_longest(*lists):
        if notfull:
            if matches := re.findall(notfull, text):
                args = list(*matches) if isinstance(*matches, tuple) else matches
                if "\[(?:(id|club))(\d+)\|.+\]" in notfull:
                    try:
                        id = -int(args[1]) if args[0] == "club" else int(args[1])
                        if id in peer_object.data.users:
                            args = (await get_user(id), args[2:])
                        else:
                            args = ("", args[2:])
                            # args = (await set_user(user_id = id, do_not_save=True), args[2:])
                            # не реагируем на челиков которых нет в беседе
                            # может в дальнейшем что-то сломается, поэтому щас просто закомменчу
                    except ValueError: pass
                return notfull, args, 0
        if full:
            if full == text:
                return full, "", 1