from vkbottle.bot import Bot
from config import BOT_TOKEN
from tasks import TaskManager
from handlers import LoggingHandler, PeerHandler

lh = LoggingHandler(name="RICHIEBOT")
daily_tasks = TaskManager()
peers_handler = PeerHandler()

bot = Bot(token=BOT_TOKEN)
