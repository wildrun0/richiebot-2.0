import logging
import logging.handlers as handlers

from pathlib import Path
from settings.config import DEBUG_STATUS


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        my_context = kwargs.pop('id', self.extra['id'])
        if my_context:
            return '%s - %s' % (my_context, msg), kwargs
        else:
            return '%s' % (msg), kwargs


class CustomFormatter(logging.Formatter):
    __slots__ = 'grey', 'yellow', 'red', 'blue', 'bold_red', 'reset', 'format_str'
    def __init__(self, name):
        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        blue = "\x1b[36;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        self.format_str = f"%(asctime)s - [{name}] - %(levelname)5s - %(message)s (%(filename)s:%(lineno)d)"

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


class LoggingHandler:
    __slots__ = 'log_name', 'logs_folder', 'log_path', 'logs_folder', 'logger'
    def __init__(self, name):
        self.log_name = "richiebot.log"
        self.logs_folder = Path("logs")
        self.log_path = Path(self.logs_folder, self.log_name)
        self.logs_folder.mkdir(exist_ok=True)
        
        log_level = DEBUG_STATUS and logging.DEBUG or logging.INFO
        customformat = CustomFormatter(name)
        
        logging.getLogger("vkbottle").setLevel(logging.INFO)
        logging.getLogger("aiocache").setLevel(logging.INFO)
        
        self.logger = logging.getLogger(__name__)
        self.logger = CustomAdapter(self.logger, {"id": ''})

        logging.getLogger().handlers.clear()
        
        filehandler = handlers.TimedRotatingFileHandler(self.log_path, when="midnight", interval=1, encoding="utf8", delay=DEBUG_STATUS)
        filehandler.suffix = "%Y-%m-%d"
        filehandler.setFormatter(
            logging.Formatter(customformat.format_str)
        )
        
        console_stream = logging.StreamHandler()
        console_stream.setFormatter(customformat)
        
        logging.basicConfig(encoding='utf-8', level=log_level, handlers=[
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
                log_arg = repr(args[1])
            else:
                log_arg = args[0]
            logging.debug(f"{f_name}() run: {log_arg}", stacklevel=3)
            return f
        return wrapper