import msgspec
from datatypes.peer.votebans.voteban_pending import ban_pending

class voteban_struct(msgspec.Struct, omit_defaults=True):
    bans_pending:   list[ban_pending] = []
    min_ban_votes:  int = 10
