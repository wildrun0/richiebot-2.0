from asyncio import sleep
from datetime import datetime

from loader import bot, ctx_storage, logger
from settings.config import BACKUP_TIME, BENEFIT_TIME_H

from tasks.functions import BackupManger, give_benefits

backupmanager = BackupManger()
lw = bot.loop_wrapper

class TaskManager:
    @lw.interval(seconds=3600) # every hour scanning for backups
    async def run_backups():
        await backupmanager.check_for_backup(frequency=BACKUP_TIME)


    async def calc_benefit_time():
        """
        Считаем секунды от инициализации до назначенного часа для 
        раздачи пособий
        """
        while 1:
            curr_time = datetime.now()
            day_gap = 0 if curr_time.hour < BENEFIT_TIME_H else 1
            elasted = datetime(
                curr_time.year, 
                curr_time.month, 
                curr_time.day + day_gap, 
                BENEFIT_TIME_H, 0, 0
            )
            sleep_time = (elasted - curr_time).seconds
            logger.debug(f"Now sleep for {sleep_time} s.", id=__name__)
            await sleep(sleep_time)
            await give_benefits()


    async def onshutdown():
        from datatypes import User
        logger.warning("Shutting down...", id=__name__)
        for obj in ctx_storage.storage.values():
            if isinstance(obj, User):
                # убираем тайм-ауты, т.к. ключи являются хэшами
                # которые не будут актуальны при следующем запуске
                for peer_instance in obj.peers.values():
                    peer_instance.timeouts.clear()
            await obj.save()
        logger.info("BYE :'(", id=__name__)


    lw.on_startup.append(run_backups())
    lw.on_shutdown.append(onshutdown())
    lw.add_task(calc_benefit_time)
