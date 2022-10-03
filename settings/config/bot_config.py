import logging
import configparser

DEFAULT_SETTINGS_FILE = "settings.ini"

config = configparser.ConfigParser()
config.read(DEFAULT_SETTINGS_FILE)

if not config.sections():
    config.add_section("SETTINGS")
    config['SETTINGS']['TOKEN'] = 'token'
    config['SETTINGS']['ID'] = '-id'
    config['SETTINGS']['BACKUP_TIME'] = 'daily'
    config["SETTINGS"]["; = Принимаемые значения: 'hourly', 'daily', 'weekly', 'monthly'"] = ""
    config["SETTINGS"]["PEERS_DEFAULT_FOLDER"] = "peers/"
    config["SETTINGS"]["; = Папка, где будут хранится основные профили бесед"] = ""
    
    config.add_section("LIMITS")
    config['LIMITS']["MAX_GREETING_LENGTH"] = "140"
    config["LIMITS"]["; = Макс. длина(символов) в приветствиях"] = ""

    config['LIMITS']["MAX_RULES_LENGTH"] = "300"
    config["LIMITS"]["; = Макс.длина(символов) в правилах"] = ""

    config['LIMITS']["MAX_NICKNAME_LENGTH"] = "30"
    config["LIMITS"]["; = Макс.длина(символов) в кличках"] = ""

    config.add_section("DEBUG")
    config['DEBUG']["ENABLED"] = "False"    

    with open(DEFAULT_SETTINGS_FILE, 'w', encoding="utf8") as configfile:
        config.write(configfile)

    logging.critical(f"{DEFAULT_SETTINGS_FILE} файл не найден! Создаю новый...")
    logging.critical("Прежде чем использовать бота, необходимо ввести токен в BOT_TOKEN= и BOT_ID=")
    exit()
else:
    BOT_TOKEN = config.get("SETTINGS", "TOKEN")
    if BOT_TOKEN == "token":
        logging.critical("Прежде чем использовать бота, необходимо ввести токен в BOT_TOKEN= и BOT_ID=")
        exit()
    
    BOT_ID = config.getint("SETTINGS", "ID")
    if BOT_ID == "-id":
        logging.critical("Прежде чем использовать бота, необходимо ввести BOT_ID= (отрицательное число)")
        exit()

    BACKUP_TIME = config.get("SETTINGS", "BACKUP_TIME")
    PEERS_DEFAULT_FOLDER = config.get("SETTINGS", "PEERS_DEFAULT_FOLDER")
    
    DEBUG_STATUS = config.getboolean("DEBUG", "ENABLED")
    
    MAX_GREETING_LENGTH = config.getint("LIMITS", "MAX_GREETING_LENGTH")
    MAX_RULES_LENGTH = config.getint("LIMITS", "MAX_RULES_LENGTH")
    MAX_NICKNAME_LENGTH = config.getint("LIMITS", "MAX_NICKNAME_LENGTH")