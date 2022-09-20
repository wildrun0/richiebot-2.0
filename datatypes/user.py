from __future__ import annotations
from dataclasses import dataclass
from loader import bot
from aiocache import cached

NAME_TEMPLATE = f"[id%d|%s %s]"

@dataclass
class User:
    name: str # [id1|Павел Дуров]
    sex: int = 2


@cached(ttl=120)
async def set_user(user_id: int, name_case: str = 'nom') -> User:
    x = (await bot.api.users.get(user_id, name_case=name_case, fields=['Sex']))[0]            
    return User(NAME_TEMPLATE % (x.id, x.first_name, x.last_name), x.sex)