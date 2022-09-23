from aiopathlib import AsyncPath
from loader import bot
from aiocache import cached
from datatypes.user import NAME_TEMPLATE, User, users_folder

@cached(ttl=120)
async def set_user(user_id: int, name_case: str = 'nom', do_not_save: bool = False) -> User:
    usersget_data = (await bot.api.users.get(user_id, name_case=name_case, fields=['Sex']))
    if not usersget_data:
        bot_name = (await bot.api.groups.get_by_id(group_id=abs(user_id)))[0].name
        user_datatype = User(
            nickname = bot_name,
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
    if not do_not_save: # Иногда, нужно получить объект User с измененным name_case, но не сохранять его
        fp = AsyncPath(users_folder, f"{user_id}.dat")
        await fp.write_json(user_datatype.to_dict(), indent=4, encoding="utf8", ensure_ascii=False)
    return user_datatype