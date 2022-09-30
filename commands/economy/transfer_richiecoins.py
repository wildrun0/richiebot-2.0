from vkbottle.bot import Message
from datatypes import PeerObject, User


async def transfer_richiecoins(event: Message, peer_obj: PeerObject, params: tuple[str, User]):
    amount, to_user = params
    # print(params)
    await event.answer(f"{to_user.name}, {amount}")