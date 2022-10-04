from datetime import timedelta, timezone
from pathlib import Path as SyncPath

from vkbottle import CtxStorage
from vkbottle.bot import Bot

from settings import LoggingHandler
from settings.config import BOT_TOKEN, DEBUG_STATUS, PEERS_DEFAULT_FOLDER

ctx_storage = CtxStorage()

lh = LoggingHandler(name="RICHIEBOT")
logger = lh.logger

peers_folder = SyncPath(PEERS_DEFAULT_FOLDER)
peers_folder.mkdir(exist_ok=True)

tz = timezone(timedelta(hours=3), name='МСК')
TIME_FORMAT = "%d.%m.%y %H:%M:%S"

bot = Bot(token=BOT_TOKEN)

from tasks import TaskManager
task_manager = TaskManager()

# functions execution logging
if DEBUG_STATUS:
    from anyio import Path
    from vkbottle.tools.dev.mini_types.base import BaseMessageMin

    Path.write_bytes = lh.listen_func(Path.write_bytes)
    BaseMessageMin.answer = lh.listen_func(BaseMessageMin.answer)