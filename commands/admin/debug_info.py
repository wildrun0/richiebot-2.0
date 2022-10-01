import os
import textwrap
import psutil
from loader import ctx_storage
from vkbottle.bot import Message


process = psutil.Process(os.getpid())
async def debug_info(event: Message, peer_obj, params) -> None:
    threads = process.num_threads()
    memory_usage = round(process.memory_info()[0] / 2**20, 2) #in MB
    memory_percent = round(process.memory_percent(), 2)
    
    cpu_usage = process.cpu_percent()
    stats = f"""
    ⚠️☣️Вам не нужно это использовать☣️⚠️
    memory_used = {memory_usage}MB
    memory_usage = {memory_percent}%
    cpu_usage = {cpu_usage}%
    threads = {threads}
    objects_in_memory = {len(ctx_storage.storage)}
    """
    await event.answer(textwrap.dedent(stats))