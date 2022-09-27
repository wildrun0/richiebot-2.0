import re
import itertools

from aiocache import cached
from datatypes import User, PeerObject
from datatypes.user import get_user


@cached(ttl=300)
async def command_used(regex_list: list[str], text: str, peer_object: PeerObject) -> tuple[str, tuple[User|None, list[str]]]:
    for command in regex_list:
        if matches := re.findall(command, text):
            args = list(*matches) if isinstance(*matches, tuple) else matches
            if "\[(?:(id|club))(\d+)\|.+\]" in command:
                try:
                    id = -int(args[1]) if args[0] == "club" else int(args[1])
                    if id in peer_object.data.users:
                        args = (await get_user(id), args[2:])
                    else:
                        args = (None, args[2:])
                        # args = (await set_user(user_id = id, do_not_save=True), args[2:])
                        # не реагируем на челиков которых нет в беседе
                        # может в дальнейшем что-то сломается, поэтому щас просто закомменчу
                except ValueError: pass
            return command, args