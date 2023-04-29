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


    @lw.interval(hours=12)
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


    @lw.interval(hours=24)
    async def calc_benefit_time():
        log.debug("BENEFITS")
        await give_benefits()


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
