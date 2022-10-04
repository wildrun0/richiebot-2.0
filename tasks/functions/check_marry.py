from asyncio import sleep

from datatypes import PeerObject
from datatypes.peer import marriage_pending
from datatypes.user import get_user
from loader import bot, ctx_storage


async def check_marry(peer_id: int, marriages_timeout: int, marriage: marriage_pending):
    await sleep(marriages_timeout)
    peer_obj: PeerObject = ctx_storage.get(peer_id)
    if marriage in peer_obj.data.marriages.marriages_pending:
        offended_by = marriage.user1
        offender_name = (await get_user(offended_by, peer_id)).get_nickname(peer_id)

        ignored_by = marriage.user2
        ignore_name = (await get_user(ignored_by, peer_id)).get_nickname(peer_id)

        peer_obj.data.marriages.marriages_pending.remove(marriage)
        await bot.api.messages.send(
            peer_id=peer_id,
            random_id=0, 
            message=f"{offender_name}, {ignore_name} не ответил на ваше предложение. Брак не состоялся."
        )