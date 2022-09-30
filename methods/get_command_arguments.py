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
            procceded_ids = []
            peer_users = peer_object.data.users
            for enum, i in enumerate(args):
                if i == "id" or i == 'club':
                    id_str = args[enum+1]
                    id = -int(id_str) if i == "club" else int(id_str)
                    args.remove(id_str)
                    if id in peer_users and id != BOT_ID:
                        procceded_ids.append(id)
                        args[enum] = await get_user(id, peer_object.peer_id)
                    else:
                        args[enum] = None
            if not args: return command, [None]
            if is_url := re.findall(URL_UID_REGEX, msg_candidate):
                nickname_url = list(filter(None, list(*is_url)))
                nickname_type = "id"
                if 'club' in nickname_url:
                    nickname_type = "club"
                    nickname_url.remove("club")
                for nickname in nickname_url:
                    try:
                        if int(nickname) in procceded_ids: continue
                        if -int(nickname) in procceded_ids: continue
                    except: pass
                    usr_index = args.index(nickname)
                    if nickname_type == "club":
                        user_id = (await bot.api.groups.get_by_id(
                                group_id=nickname
                            ))[0].id
                    else:
                        user_id = (await bot.api.users.get(
                            user_ids=nickname
                        ))[0].id
                    if user_id in peer_users:
                        args[usr_index] = await get_user(
                            user_id,
                            peer_object.peer_id
                        )
                    else: args[usr_index] = None
            if not any(filter(lambda x: type(x) is User, args)) and not None in args:
                args.insert(0, await get_user(user_id, peer_object.peer_id))
            return command, args