from loader import bot

async def display_nicknames(users_id: list|int, name_case = 'nom') -> str:
    template = f"[id%d|%s %s]"
    # to_return = []
    # if isinstance(users_id, list):
    names = await bot.api.users.get(users_id, name_case=name_case)
    to_return = map(lambda x: template % (x.id, x.first_name, x.last_name), names)
    # for i in names:
    #     to_return.append(template % (i.id, i.first_name, i.last_name))
    return to_return