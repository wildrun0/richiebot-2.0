import os
import psutil
from methods.decorators.peer_manager import peers_objs
from datatypes.user.get_user import cached_users
from vkbottle.bot import Message


process = psutil.Process(os.getpid())
async def stat(event: Message, peer_obj, params) -> None:
    threads = process.num_threads()
    memory_usage = round(process.memory_info()[0] / 2**20, 2) #in MB
    memory_percent = round(process.memory_percent(), 2)
    
    cpu_usage = process.cpu_percent()
    
    await event.answer(f"""
        ⚠️☣️Вам не нужно это использовать☣️⚠️
        memory_used = {memory_usage}MB
        memory_usage = {memory_percent}%
        cpu_usage = {cpu_usage}%
        threads = {threads}
        peers_in_memory = {len(peers_objs)}
        users_in_memory = {len(cached_users)}
    """)