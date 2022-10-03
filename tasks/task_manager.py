from loader import bot, ctx_storage, logger
from settings.config import BACKUP_TIME

from tasks.functions import BackupManger

backupmanager = BackupManger()
lw = bot.loop_wrapper

class TaskManager:
    @lw.interval(seconds=3600) # every hour scanning for backups
    async def run_backups():
        await backupmanager.check_for_backup(frequency=BACKUP_TIME)


    async def onstartup(self):
        await self.run_backups()


    async def onshutdown():
        from datatypes import User
        logger.warning("Shutting down...")
        for obj in ctx_storage.storage.values():
            if isinstance(obj, User):
                # убираем тайм-ауты, т.к. ключи являются хэшами
                # которые не будут актуальны при следующем запуске
                for peer_instance in obj.peers.values():
                    peer_instance.timeouts.clear()
            await obj.save()
        logger.info("BYE :'(")


    lw.on_startup.append(run_backups())
    lw.on_shutdown.append(onshutdown())