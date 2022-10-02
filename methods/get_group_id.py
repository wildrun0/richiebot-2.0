from loader import bot


async def get_group_id(nickname: str) -> int:
    return -(await bot.api.groups.get_by_id(
        group_id=nickname
    ))[0].id
