import os
import psutil

from vkbottle.bot import Message


process = psutil.Process(os.getpid())
async def stat(event: Message, peer_obj, params) -> None:
    memory_usage = round(process.memory_info()[0] / 2**20, 2) #in MB
    memory_percent = round(process.memory_percent(), 2)
    
    cpu_usage = process.cpu_percent()
    
    await event.answer(f"memory_usage = {memory_usage}MB\nmemory_percent = {memory_percent}\ncpu_usage = {cpu_usage}")