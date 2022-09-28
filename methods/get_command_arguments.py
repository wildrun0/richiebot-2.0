import re
from aiocache import cached
from datatypes import User, PeerObject
from datatypes.user import set_user, get_user
from settings.bot_commands import UID_REGEX


@cached(ttl=300)
async def get_command_arguments(
    regex_list: list[str],
    msg_candidate: str,
    peer_object: PeerObject,
    user_id: int
) -> tuple[str, tuple[User|None, list[str]]]:
    for command in regex_list:
        if matches := re.findall(command, msg_candidate):
            args = list(*matches) if isinstance(*matches, tuple) else matches
            if UID_REGEX in command:
                try:
                    id = -int(args[1]) if args[0] == "club" else int(args[1])
                    if id in peer_object.data.users:
                        args = (await get_user(id, peer_object.peer_id), args[2:])
                    else:
                        args = (None, args[2:])
                except ValueError: pass
            else:       # хз кто ета
                if user_id in peer_object.data.users: 
                    user = await get_user(user_id, peer_object.peer_id)
                else:
                    user = set_user(user_id, peer_object.peer_id, do_not_save = True)
                args = (user, *args)
            return command, args