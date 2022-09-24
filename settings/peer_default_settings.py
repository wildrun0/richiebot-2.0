peer_default_dict = {
    "greeting": None,
    "rules": None,
    "admins": [],
    "clans": {},
    "ban_list": {
            # "397717739":  [320750004, ban_timestamp]
    },
    "commands_timeouts":{
        "richie_who_whom":  300,
        "richie_infa":      300,
        "richie_kosti":     300,
        "richie_casino":    300,
        "richie_song":      300,
        "richie_primer":    300,
        "richie_roulette":  300,
        "richie_duel":      300,
        "richie_clan_duel": 300
    },
    "marriages":{
        "marriage_timeout": 180,
        "marriages_pending": [
            # [u1, u2, timestamp]
        ],
        "couples": [
            # u1, u2
        ]
    },
    "voteban":{
        "bans_pending": [
            # [user_to_ban, votes INT , voted users list]
        ],
        "min_ban_votes": 10
    },
    "last_kicked": [
        #uid, timestamp
    ],
    "warns":{
        "max_warns": 5,
        "users":{
            # 397717739: warn_count
        }
    },
    "mute":{
        "users":{
            # 39717739: до скольки мут(timestamp)
        }
    }
}