from aiocache import cached
from datatypes.user import NAME_TEMPLATE
from loader import bot


# Функция возвращает строки (или list-объекты) класса Users, где name = '[id1|Павел Дуров] в нужном name_case
@cached(ttl=120)
async def display_nicknames(users_id: tuple|int, name_case: tuple|str = 'nom') -> list[str] | str:
    if isinstance(name_case, tuple):
        to_ret = []
        for uid, ncs in zip(users_id, name_case):
            if uid > 0:
                user = (await bot.api.users.get(uid, name_case=ncs))[0]
                name = NAME_TEMPLATE % ("id", uid, user.first_name, user.last_name)
            else:
                bot_id = abs(uid)
                name = NAME_TEMPLATE % ("club", bot_id, (await bot.api.groups.get_by_id(bot_id))[0].name, "")
            to_ret.append(name)
        return to_ret
    else:
        if isinstance(users_id, int): #if only one
            if users_id > 0:
                user = (await bot.api.users.get(users_id, name_case=name_case))[0]
                to_ret = NAME_TEMPLATE % ("id", users_id, user.first_name, user.last_name)
            else:
                bot_id = abs(users_id)
                to_ret = NAME_TEMPLATE % ("club", bot_id, (await bot.api.groups.get_by_id(bot_id))[0].name, "")
            return to_ret
        to_ret = []
        return [
            NAME_TEMPLATE % ("id", user.id, user.first_name, user.last_name)
            for user in (await bot.api.users.get(user_ids=users_id, name_case=name_case))
        ]