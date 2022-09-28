from datetime import datetime

from loader import bot, TIME_FORMAT, tz
from datatypes.user import NAME_TEMPLATE, User, peers_struct


async def set_user(user_id: int, peer_id: str|int = None, name_case: str = 'nom', do_not_save: bool = False) -> User:
    if user_id == 0: return None
    usersget_data = (await bot.api.users.get(user_id, name_case=name_case, fields=['Sex']))
    if peer_id:
        peer_members = (await bot.api.messages.get_conversation_members(peer_id=peer_id)).items
        join_date = [
            date for date in 
            [user.member_id == user_id and user.join_date for user in peer_members] 
            if date != False
        ][0]

    if not usersget_data:
        bot_name = (await bot.api.groups.get_by_id(group_id=abs(user_id)))[0].name
        user_datatype = User(
            name = f"[club{abs(user_id)}|{bot_name}]",
            sex = 0,
            id = user_id
        )
    else:
        x = usersget_data[0]
        user_datatype = User(
            name = NAME_TEMPLATE % (x.id, x.first_name, x.last_name),
            sex = x.sex,
            id = x.id
        )
    if peer_id:
        user_datatype.peers[str(peer_id)] = peers_struct(
            peer_join_date = datetime.fromtimestamp(join_date, tz).strftime(TIME_FORMAT),
        )
    if not do_not_save: # Иногда, нужно получить объект User с измененным name_case, но не сохранять его
        user_datatype.save()
    return user_datatype