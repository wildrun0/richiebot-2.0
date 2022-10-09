from asyncio import sleep

from datatypes import PeerObject
from loader import ctx_storage, bot


async def check_casino(peer_id: int, sleep_time: int):
    await sleep(sleep_time)
    peer_obj: PeerObject = ctx_storage.get(peer_id)
    if peer_obj.data.casino.game:
        peer_obj.data.casino.game = None
        await peer_obj.save()
    await bot.api.messages.send(
        peer_id = peer_id,
        random_id = 0,
        message = f"Тайм-аут! Казино так и не было запущено :("
    )
