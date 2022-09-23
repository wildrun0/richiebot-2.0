from vkbottle.bot import Bot
from config import BOT_TOKEN
from tasks import TaskManager
from handlers import LoggingHandler, PeerHandler

lh = LoggingHandler(name="RICHIEBOT")

# functions execution logging
from aiopathlib import AsyncPath
AsyncPath.write_json= lh.listen_func(AsyncPath.write_json)

from vkbottle.tools.dev.mini_types.base import BaseMessageMin
BaseMessageMin.answer = lh.listen_func(BaseMessageMin.answer)


daily_tasks = TaskManager()
peers_handler = PeerHandler()

bot = Bot(token=BOT_TOKEN)