import re
from aiocache import cached
from datatypes import User, PeerObject
from datatypes.user import get_user
from settings.bot_commands import UID_REGEX


@cached(ttl=300)
async def get_command_arguments(
    regex_list: list[str],
    msg_candidate: str,
    peer_object: PeerObject
) -> tuple[str, tuple[User|None, list[str]]]:
    for command in regex_list:
        if matches := re.findall(command, msg_candidate):
            args = list(*matches) if isinstance(*matches, tuple) else matches
            if UID_REGEX in command:
                try:
                    id = -int(args[1]) if args[0] == "club" else int(args[1])
                    if id in peer_object.data.users:
                        args = (await get_user(id), args[2:])
                    else:
                        args = (None, args[2:])
                except ValueError: pass # если команда имеет необязательный UID_REGEX
            return command, args        # напр., если она берет пользователя из onreply - event