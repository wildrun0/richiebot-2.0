import logging
import logging.handlers as handlers

from pathlib import Path

from config import BOT_ID
from time import time


class CustomFormatter(logging.Formatter):
    def __init__(self, name):
        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        blue = "\x1b[36;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        self.format_str = f"%(asctime)s - [{name}] - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

        self.FORMATS = {
            logging.DEBUG: blue + self.format_str + reset,
            logging.INFO: grey + self.format_str + reset,
            logging.WARNING: yellow + self.format_str + reset,
            logging.ERROR: red + self.format_str + reset,
            logging.CRITICAL: bold_red + self.format_str + reset
        }


    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class LoggingHandler():
    def __init__(self, name):
        self.default_log_name = "richiebot.log"
        self.default_logs_folder = Path("logs")
        self.latest_log_path = Path(self.default_logs_folder, self.default_log_name)
        self.default_logs_folder.mkdir(exist_ok=True)
        customformat = CustomFormatter(name)
        
        logging.getLogger("vkbottle").setLevel(logging.INFO)
        logging.getLogger("aiocache").setLevel(logging.INFO)
        
        logging.getLogger().handlers.clear()
        
        filehandler = handlers.TimedRotatingFileHandler(self.latest_log_path, when="midnight", interval=1, encoding="utf8")
        filehandler.suffix = "%Y-%m-%d"
        filehandler.setFormatter(
            logging.Formatter(customformat.format_str)
        )
        
        console_stream = logging.StreamHandler()
        console_stream.setFormatter(customformat)
        
        logging.basicConfig(encoding='utf-8', level=logging.DEBUG, handlers=[
            console_stream,
            filehandler
        ])
        logging.captureWarnings(True)

    @staticmethod
    def listen_func(func):
        async def wrapper(*args, **kwargs):
            f_name = func.__name__
            f = await func(*args, **kwargs)            
            if f_name == "answer":
                # from loader import peers_handler
                log_arg = args[1]
                # peer_id = str(args[0].peer_id)
                # cmid = f.conversation_message_id
                # await peers_handler.messages.write(
                #     message_text="", cmid = cmid, peer_id = peer_id, user_id = str(BOT_ID), date = time()
                # )   # нет смысла записывать текст, эти сообщения записываются только для дальнейшей очистки
            else:
                log_arg = args[0]
            logging.debug(f"{f_name}() run: {log_arg}", stacklevel=3)
            return f
        return wrapper