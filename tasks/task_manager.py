from asyncio import sleep
from datetime import datetime

from datatypes import PeerObject
from loader import bot, ctx_storage, log
from settings.config import BACKUP_TIME, BENEFIT_TIME_H

from tasks.functions import BackupManger, give_benefits

backupmanager = BackupManger()
lw = bot.loop_wrapper

class TaskManager:
    @lw.interval(hours=1) # every hour scanning for backups
    async def run_backups():
        await backupmanager.check_for_backup(frequency=BACKUP_TIME)


    # @lw.timer(seconds=10)
    @lw.interval(hours=2)
    async def cleanup_msgs():
        """
        Очищаем из бесед сообщения, которым больше одной недели
        """
        curr_timestamp = datetime.timestamp(datetime.now())
        for obj in ctx_storage.storage.values():
            if isinstance(obj, PeerObject):
                peer_msgs = obj.messages.data.users
                total_removed = 0
                for user in peer_msgs.values():
                    outdated_msgs = [
                        message
                        for message in user.messages
                        if (curr_timestamp - message.date) >= 604800
                    ]
                    total_removed += len(outdated_msgs)
                    user.messages = [m for m in user.messages if m not in outdated_msgs]
                log.debug(f"Removed {total_removed} msgs", id=obj.peer_id)
                total_removed and await obj.save()


    async def calc_benefit_time():
        """
        Считаем секунды от инициализации до назначенного часа для
        раздачи пособий
        """
        while 1:
            curr_time = datetime.now()
            day_gap = 0 if curr_time.hour < BENEFIT_TIME_H else 1
            try:
                elasted = datetime(
                    curr_time.year,
                    curr_time.month,
                    curr_time.day + day_gap,
                    BENEFIT_TIME_H, 0, 0
                )
            except ValueError:
                 elasted = datetime(
                    curr_time.year,
                    curr_time.month + 1,
                    1,
                    BENEFIT_TIME_H, 0, 0
                )
            sleep_time = (elasted - curr_time).seconds
            log.debug(f"Now sleep for {sleep_time} s.", id=__name__)
            await sleep(sleep_time)
            await give_benefits()
            log.info(f"Раздача пособий", id=__name__)


    async def onshutdown():
        from datatypes import User
        log.warning("Shutting down...")
        for obj in ctx_storage.storage.values():
            if isinstance(obj, User):
                # убираем тайм-ауты, т.к. ключи являются хэшами
                # которые не будут актуальны при следующем запуске
                for peer_instance in obj.peers.values():
                    peer_instance.timeouts.clear()
            else:
                obj: PeerObject
                obj.data.marriages.marriages_pending.clear()
                obj.data.casino.game = None
            await obj.save()
        log.info("BYE :'(")


    lw.on_startup.append(run_backups())
    lw.on_shutdown.append(onshutdown())
    lw.add_task(calc_benefit_time)
