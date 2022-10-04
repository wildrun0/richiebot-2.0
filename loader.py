from settings import LoggingHandler
from vkbottle.bot import Bot
from vkbottle import CtxStorage

ctx_storage = CtxStorage()

lh = LoggingHandler(name="RICHIEBOT")
logger = lh.logger

from settings.config import BOT_TOKEN
from datetime import timedelta, timezone

tz = timezone(timedelta(hours=3), name='МСК')
TIME_FORMAT = "%d.%m.%y %H:%M:%S"

bot = Bot(token=BOT_TOKEN)

from tasks import TaskManager
task_manager = TaskManager()

# functions execution logging
from anyio import Path
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

Path.write_bytes = lh.listen_func(Path.write_bytes)
BaseMessageMin.answer = lh.listen_func(BaseMessageMin.answer)