import re
from aiocache import cached

from datatypes import User, PeerObject
from datatypes.user import set_user, get_user

from settings.bot_commands import UID_REGEX, URL_UID_REGEX
from settings.config import BOT_ID
from loader import bot


@cached(ttl=300)
async def get_command_arguments(
    regex_list: list[str],
    msg_candidate: str,
    peer_object: PeerObject,
    user_id: int
) -> tuple[User|None, list[str]|str]:
    for command in regex_list:
        if matches := re.findall(command, msg_candidate):
            raw_args = list(*matches) if isinstance(*matches, tuple) else matches
            args = list(filter(None, map(str.strip, raw_args))) # removing blank strings in list
            if UID_REGEX in command or URL_UID_REGEX in command:
                try:
                    if re.search(URL_UID_REGEX, msg_candidate) and (
                        (str_id := args[0]) not in ["club", 'id']
                    ):
                        try:
                            id = (await bot.api.users.get(
                                user_ids=str_id
                            ))[0].id
                        except IndexError:
                            id = -(await bot.api.groups.get_by_id(
                                group_id=str_id
                            ))[0].id
                        args.insert(0, '')
                        # чтобы соответсвовать коду ниже, где args имеют вид (0,1,2,3,4)
                    else:
                        id = -int(args[1]) if args[0] == "club" else int(args[1])
                    if id in peer_object.data.users and id != BOT_ID:
                        args = (await get_user(id, peer_object.peer_id), args[2:])
                    else:
                        args = (None, args[2:])
                except (ValueError, IndexError):
                    args.insert(0, '')
                    pass
            else:       # хз кто ета
                if user_id in peer_object.data.users: 
                    user = await get_user(user_id, peer_object.peer_id)
                else:
                    user = set_user(user_id, peer_object.peer_id, do_not_save = True)
                args = (user, *args)
            return command, args