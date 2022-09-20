# from functools import lru_cache
import enum
from aiocache import cached
from loader import bot
from datatypes import User


template = f"[id%d|%s %s]"

def set_user(x: int) -> User:
    return User(template % (x.id, x.first_name, x.last_name), x.sex)


# @lru_cache(maxsize=100)
# Функция возвращает строки (или map-объекты) типа '[id1|Павел Дуров] для дальнейшей вставки в сообщение

@cached(ttl=60)
async def display_nicknames(users_id: tuple|int, name_case: tuple|str = 'nom') -> map|str:
    if isinstance(name_case, tuple):
        return ([
            set_user((
                await bot.api.users.get(usr, name_case=name_case[enum], fields=['Sex'])
            )[0]) for enum, usr in enumerate(users_id)
        ])
    else:
        names = await bot.api.users.get(users_id, name_case=name_case, fields=['Sex'])
        if isinstance(users_id, str): #if only one
            return set_user(names[0])
        to_return = map(set_user, names)
    return to_return