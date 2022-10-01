import re

from aiocache import cached
from datatypes import User, PeerObject
from datatypes.user import get_user
from settings.bot_commands import URL_UID_REGEX
from settings.config import BOT_ID
from loader import bot


async def get_group_id(nickname: str) -> int:
    return -(await bot.api.groups.get_by_id(
        group_id=nickname
    ))[0].id


async def get_user_id(nickname: str) -> int:
    return (await bot.api.users.get(
        user_ids=nickname
    ))[0].id


@cached(ttl=300)
async def get_command_arguments(
    regex_list:     list[str],
    msg_candidate:  str,
    peer_object:    PeerObject,
    user_id:        int
) -> tuple[str, tuple[User, ...]|list[None]]:
    for command in regex_list:
        if matches := re.findall(command, msg_candidate):
            if not matches: return command, [None] # если пусто то может быть event.reply_message
            raw_args = list(*matches) if isinstance(*matches, tuple) else matches
            args = list(filter(None, map(str.strip, raw_args))) # removing blank strings in list
            procceded_ids = []
            peer_users = peer_object.data.users
            for enum, i in enumerate(args):
                if i == "id" or i == 'club':
                    id_str = args[enum+1]
                    id = -int(id_str) if i == "club" else int(id_str)
                    args.remove(id_str)
                    if (id in peer_users and
                        id != BOT_ID):
                        procceded_ids.append(id)
                        args[enum] = await get_user(id, peer_object.peer_id)
                    else:
                        args[enum] = None
            if is_url := re.findall(URL_UID_REGEX, msg_candidate): # ссылки типа vk.com/durov
                nickname_url = list(filter(None, list(*is_url)))   # т.е. где вместо id - display_name
                nickname_type = None
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
                        user_id = await get_group_id(nickname)
                    else:
                        try:
                            user_id = await get_user_id(nickname)
                        except IndexError:
                            user_id = await get_group_id(nickname)
                    if user_id in peer_users and user_id != BOT_ID:
                        args[usr_index] = await get_user(
                            user_id,
                            peer_object.peer_id
                        )
                    else: args[usr_index] = None
            if not any(filter(lambda x: type(x) is User, args)) and not None in args:
                args.insert(0, await get_user(user_id, peer_object.peer_id))
            return command, args