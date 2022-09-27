import commands

UID_REGEX = "\[(?:(id|club))(\d+)\|.+\]"
ALL_REGEX = "([\s\S]*)"

administrative_commands_notfull = {
    f"ричи добавить приветствие {ALL_REGEX}":   commands.admin.add_greetings,
    f"ричи добавить правила {ALL_REGEX}":       commands.admin.add_rules,
    f"!kick\s?{UID_REGEX}":                       commands.admin.kick,
    f"забанить\s?(?:{UID_REGEX})?":                    commands.admin.ban,
    f"разбанить {UID_REGEX}":                   commands.admin.unban,
    f"варн\s?{UID_REGEX}":                        commands.admin.warn,
    f"снять варны\s?{UID_REGEX}":                 commands.admin.unwarn,
    f"мут (?:{UID_REGEX})?\s?(\d+) (год|лет|мес|нед|час|мин|сек)": commands.admin.mute,
    f"размутить\s?{UID_REGEX}":                   commands.admin.unmute
}

administrative_commands_full = {
    "ричи обновить пользователей":  commands.admin.renew_users_list,
    "ричи сброс":                   commands.admin.reset_bot_peer,
    "ричи очистка":                 commands.admin.clear_msgs,
    "ричи удалить правила":         commands.admin.del_rules,
    "ричи список забаненных":       commands.admin.ban_list,
    "ричи статистика":              commands.admin.stat
}

default_commands_notfull = {
    "ричи кто":                     commands.richie.who,
    "ричи кого":                    commands.richie.who,
    "ричи добавить кличку":         commands.richie.set_nickname,
    "ричи инфа":                    commands.richie.infa,
    "ричи свадьба":                 commands.richie.marry,

    "ричи баланс":                  commands.economy.balance,
    "ричи инвентарь":               commands.economy.inventory,
    "ричи передать":                commands.economy.transfer_richiecoins,

    "ричи дуэль":                   commands.clan.solo_duel,
    "ричи создать клан":            commands.clan.create,
    "ричи завербовать":             commands.clan.invite,
    "ричи пригласить":              commands.clan.invite,
    "ричи повысить":                commands.clan.status_up,
    "ричи понизить":                commands.clan.status_down,
    "ричи выгнать":                 commands.clan.kick,
    "ричи исключить":               commands.clan.kick
}

default_commands_full = {
    "ричи привет":                  commands.richie.hello,
    "ричи донат":                   commands.richie.donate,
    "ричи об авторе":               commands.richie.about,
    "ричи актив":                   commands.richie.peer_active,
    "ричи правила":                 commands.richie.view_rules,
    "ричи браки":                   commands.richie.marry_list,

    "ричи бросить кости":           commands.game.kosti,
    "ричи кости":                   commands.game.kosti,
    "ричи песня":                   commands.game.song,
    "ричи пример":                  commands.game.math,
    "ричи русская рулетка":         commands.game.roulette,

    "ричи магазин":                 commands.economy.shop,
    "ричи топ":                     commands.economy.top,
    "ричи нужно пособие":           commands.economy.benefit,

    "ричи рандом дуэль":            commands.clan.random_solo_duel,
    "ричи удалить клан":            commands.clan.delete,
    "ричи выйти из клана":          commands.clan.leave,
    "ричи о клане":                 commands.clan.about,
    "ричи раздать жалованье":       commands.clan.cash_handout,
    "ричи топ кланов":              commands.clan.top,
    "ричи дуэль кланов":            commands.clan.duel
}


admin_commands_notfull = [*administrative_commands_notfull.keys()]
admin_commands_full = [*administrative_commands_full.keys()]

all_commands_notfull = [*default_commands_notfull.keys()]
all_commands_full = [*default_commands_full.keys()]