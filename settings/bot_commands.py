import commands

UID_REGEX = "(?:\[(?:(id|club))(\d+)\|.+\])"
URL_UID_REGEX = "(?:https:\/\/vk.com\/(?:(id|club)?(\d+))?([^\s]+)?)"
CATCH_ALL_REGEX = "([\s\S]*)"

#   Параметры в неполных командах в ивентах будут приходить
#   по порядку их регекса       
#   т.е. например команда "мут @id0101010 5 лет" придет в параметрах как
#   UserDataType цифра срок
#   т.е. 010101 5 лет

#   "ричи передать 150 ричсонов @id010101"
#   придет как 150 UserDataType


administrative_commands_notfull = {
    f"ричи добавить приветствие {CATCH_ALL_REGEX}":             commands.admin.add_greetings,
    f"ричи добавить правила {CATCH_ALL_REGEX}":                 commands.admin.add_rules,
    f"!kick\s?(?:{UID_REGEX}|{URL_UID_REGEX})?":                commands.admin.kick,
    f"забанить\s?(?:{UID_REGEX}|{URL_UID_REGEX})?":             commands.admin.ban,
    f"разбанить (?:{UID_REGEX}|{URL_UID_REGEX})":               commands.admin.unban,
    f"варн\s?(?:{UID_REGEX}|{URL_UID_REGEX})?":                 commands.admin.warn,
    f"снять варны\s?(?:{UID_REGEX}|{URL_UID_REGEX})?":          commands.admin.unwarn,
    f"мут (?:{UID_REGEX}|{URL_UID_REGEX})?\s?(\d+) (год|лет|мес|нед|час|мин|сек)":  commands.admin.mute,
    f"размутить\s?(?:{UID_REGEX}|{URL_UID_REGEX})?":            commands.admin.unmute
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
    f"ричи кто\s?{CATCH_ALL_REGEX}":            commands.richie.who,
    f"ричи кого\s?{CATCH_ALL_REGEX}":           commands.richie.who,
    f"ричи добавить кличку {CATCH_ALL_REGEX}":  commands.richie.set_nickname,
    f"ричи инфа\s?{CATCH_ALL_REGEX}":           commands.richie.infa,
    f"ричи свадьба\s?с?\s?{UID_REGEX}":            commands.richie.marry,

    f"ричи баланс\s?(?:{UID_REGEX}|{URL_UID_REGEX})?":      commands.economy.balance,
    f"ричи инвентарь\s?(?:{UID_REGEX}|{URL_UID_REGEX})?":   commands.economy.inventory,
    f"ричи передать (\d+)\s?(?:ричсонов|ричкоинов)?{UID_REGEX}":commands.economy.transfer_richiecoins,

    f"ричи дуэль\s?с?\s?{UID_REGEX}":           commands.clan.solo_duel,
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
    "ричи онлайн":                  commands.richie.online,
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