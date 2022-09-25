from vkbottle.bot import Bot
from config import BOT_TOKEN
from tasks import TaskManager
from handlers import LoggingHandler
import pytz

tz = pytz.timezone("Europe/Moscow")
TIME_FORMAT = "%d.%m.%y %H:%M:%S"

lh = LoggingHandler(name="RICHIEBOT")

# functions execution logging
from aiopathlib import AsyncPath
AsyncPath.async_write = lh.listen_func(AsyncPath.async_write)

from vkbottle.tools.dev.mini_types.base import BaseMessageMin
BaseMessageMin.answer = lh.listen_func(BaseMessageMin.answer)

daily_tasks = TaskManager()

bot = Bot(token=BOT_TOKEN)