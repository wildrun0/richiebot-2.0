import textwrap

from datatypes import PeerObject
from datatypes.user import get_user, timeout_struct
from vkbottle.bot import Message


def timeout_manager(func):
    async def wrapper(*args, **kwargs):
        f_hash = str(hash(func))

        event: Message = args[0]
        peer_obj: PeerObject = args[1]
        peer_id = event.peer_id
        
        caller = await get_user(event.from_id, peer_id)
        caller_timeouts = caller.peers[str(peer_id)].timeouts

        fname = func.__name__
        if f_hash in caller_timeouts:
            command_timeout = caller_timeouts[f_hash]
            if event.date >= command_timeout.due_date:
                del command_timeout
            else:
                if not command_timeout.shadowbanned:
                    m, s = divmod(command_timeout.due_date - event.date, 60)
                    await event.answer(textwrap.dedent(f"""
                        🚫 {caller.get_nickname(peer_id)}, таймаут!
                        {m} мин, {s} сек. осталось
                    """))
                    command_timeout.shadowbanned = True
                return False
        f = await func(*args, **kwargs)
        if fname in (commands_timeouts := peer_obj.data.commands_timeouts).__struct_fields__:
            timeout_int: int = commands_timeouts.__getattribute__(fname)
            caller_timeouts[f_hash] = timeout_struct(event.date + timeout_int)
        return f
    return wrapper