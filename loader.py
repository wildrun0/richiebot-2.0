from handlers import LoggingHandler
from vkbottle.bot import Bot
from vkbottle import CtxStorage

ctx_storage = CtxStorage()

lh = LoggingHandler(name="RICHIEBOT")
logger = lh.logger

from settings.config import BOT_TOKEN
from tasks import TaskManager
from pytz import timezone

tz = timezone("Europe/Moscow")
TIME_FORMAT = "%d.%m.%y %H:%M:%S"

daily_tasks = TaskManager()
bot = Bot(token=BOT_TOKEN)

# functions execution logging
from aiopathlib import AsyncPath
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

AsyncPath.async_write = lh.listen_func(AsyncPath.async_write)
BaseMessageMin.answer = lh.listen_func(BaseMessageMin.answer)