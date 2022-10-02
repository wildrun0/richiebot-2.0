from loader import bot


async def get_user_id(nickname: str) -> int:
    return (await bot.api.users.get(
        user_ids=nickname
    ))[0].id