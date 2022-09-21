from __future__ import annotations
from aiocache import cached
from datatypes import set_user
from datatypes import User


# Функция возвращает строки (или map-объекты) типа '[id1|Павел Дуров] для дальнейшей вставки в сообщение
@cached(ttl=300)
async def display_nicknames(users_id: tuple|int, name_case: tuple|str = 'nom') -> list[User] | User:
    if isinstance(name_case, tuple):
        return ([
            await set_user(uid, ncs) for uid, ncs in zip(users_id, name_case)
        ])
    else:
        if isinstance(users_id, str): #if only one
            return await set_user(users_id)
        return [await set_user(uid) for uid in users_id]