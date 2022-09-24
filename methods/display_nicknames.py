from __future__ import annotations
from aiocache import cached
from datatypes.user import User, set_user


# Функция возвращает строки (или list-объекты) класса Users, где name = '[id1|Павел Дуров] в нужном name_case
@cached(ttl=120)
async def display_nicknames(users_id: tuple|int, name_case: tuple|str = 'nom') -> list[User] | User:
    if isinstance(name_case, tuple):
        return ([
            await set_user(uid, ncs, do_not_save=True) for uid, ncs in zip(users_id, name_case)
        ])
    else:
        if isinstance(users_id, str): #if only one
            return await set_user(users_id, name_case, do_not_save=True)
        return [await set_user(uid, name_case, do_not_save=True) for uid in users_id]