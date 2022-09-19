from loader import bot


async def display_nicknames(users_id: list|int, name_case: list|str = 'nom') -> list|str:
    template = f"[id%d|%s %s]"
    if isinstance(name_case, list):
        to_return = []
        for enum, usr in enumerate(users_id):
            x = (await bot.api.users.get(usr, name_case=name_case[enum]))[0]
            to_return.append(template % (x.id, x.first_name, x.last_name))
        return to_return
    names = await bot.api.users.get(users_id, name_case=name_case)
    to_return = map(lambda x: template % (x.id, x.first_name, x.last_name), names)
    return to_return