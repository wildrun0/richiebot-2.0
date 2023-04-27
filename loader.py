from datetime import timedelta, timezone
from pathlib import Path as SyncPath

from settings import LoggingHandler
from settings.config import BOT_TOKEN, DEBUG_STATUS, PEERS_DEFAULT_FOLDER

lh = LoggingHandler(name="RICHIEBOT")
log = lh.logger

from vkbottle import CtxStorage
from vkbottle.bot import Bot

ctx_storage = CtxStorage()


peers_folder = SyncPath(PEERS_DEFAULT_FOLDER)
peers_folder.mkdir(exist_ok=True)

tz = timezone(timedelta(hours=3), name='МСК') # UTC + 3H
TIME_FORMAT = "%d.%m.%y %H:%M:%S"

bot = Bot(token=BOT_TOKEN)

from tasks import TaskManager
task_manager = TaskManager()

# functions execution logging
if DEBUG_STATUS:
    from anyio import Path
    from vkbottle.bot import Message

    Path.write_bytes = lh.listen_func(Path.write_bytes)
    Message.answer = lh.listen_func(Message.answer)
