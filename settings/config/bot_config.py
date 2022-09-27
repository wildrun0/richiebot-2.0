import logging
import configparser

DEFAULT_SETTINGS_FILE = "settings.ini"

config = configparser.ConfigParser()
config.read(DEFAULT_SETTINGS_FILE)

if not config.sections():
    config.add_section("BOT_INFO")
    config['BOT_INFO']['TOKEN'] = 'token'
    config['BOT_INFO']['ID'] = '-id'
    
    config.add_section("DEBUG")
    config['DEBUG']["ENABLED"] = "False"

    with open(DEFAULT_SETTINGS_FILE, 'w') as configfile:    # save
        config.write(configfile)
    logging.critical(f"{DEFAULT_SETTINGS_FILE} файл не найден! Создаю новый...")
    logging.critical("Прежде чем использовать бота, необходимо ввести токен в BOT_TOKEN= и BOT_ID=")
    exit()
else:
    BOT_TOKEN = config.get("BOT_INFO", "TOKEN")
    BOT_ID = config.getint("BOT_INFO", "ID")
    DEBUG_STATUS = config.getboolean("DEBUG", "ENABLED")
