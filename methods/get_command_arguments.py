import re

from datatypes import PeerObject, User
from datatypes.user import get_user
from settings.bot_commands import UID_REGEX, URL_UID_REGEX
from settings.config import BOT_ID

from methods.get_group_id import get_group_id
from methods.get_user_id import get_user_id


async def get_command_arguments(
    regex_list:     list[str],
    msg_candidate:  str,
    peer_object:    PeerObject
) -> tuple[str, tuple[User, ...]|list[None]]:
    for command in regex_list:
        if matches := re.findall(command, msg_candidate, re.IGNORECASE):
            if not matches: return command, [None] # если пусто то может быть event.reply_message
            raw_args = list(*matches) if isinstance(*matches, tuple) else matches
            args = list(filter(None, map(str.strip, raw_args))) # removing blank strings in list
            procceded_ids = []
            peer_users = peer_object.data.users
            if (displayname := re.findall("(?:https:\/\/vk.com\/(?!id|club)([^\s]+))", msg_candidate)) and (
                (URL_UID_REGEX in command) or 
                (UID_REGEX in command)):
                for nick in displayname:
                    index = args.index(nick)
                    try:
                        try:
                            user = await get_user_id(nick)
                            if not user:
                                user = await get_group_id(nick)
                        except:
                            user = await get_group_id(nick)
                    except: user = 0 # заглушка чтобы выбить None
                    if (user in peer_users and
                        user != BOT_ID):
                        args[index] = await get_user(user, peer_object.peer_id)
                    else:
                        if user == BOT_ID: return command, [None]
                        args[index] = None
            for enum, i in enumerate(args):
                if i == "id" or i == 'club':
                    id_str = args[enum+1]
                    id = -int(id_str) if i == "club" else int(id_str)
                    args.remove(id_str)
                    procceded_ids.append(id)
                    if (id in peer_users and
                        id != BOT_ID):
                        args[enum] = await get_user(id, peer_object.peer_id)
                    else:
                        if id == BOT_ID: return command, [None]
                        args[enum] = None
            have_user = any(isinstance(val, User) for val in args)
            if not have_user and (URL_UID_REGEX in command or UID_REGEX in command):
                insert_index = raw_args.index('')
                raw_args[insert_index] = None
                args = [x for x in raw_args if not x == '']
            return command, args