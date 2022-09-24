import logging
from environs import Env

env = Env()
env.read_env()

try:
    BOT_TOKEN = env.str("BOT_TOKEN")
    BOT_ID = env.str("BOT_ID")
    DEBUG_STATUS = env.str("DEBUG")
except:
    logging.critical(".env файл не найден! Создаю новый...")
    logging.critical("Прежде чем использовать бота, необходимо ввести токен в BOT_TOKEN= и BOT_ID=")

    with open(".env", "w") as f:
        f.write("BOT_TOKEN=token\nBOT_ID = -ID\nDEBUG=False")