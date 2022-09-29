import logging
from vkbottle import LoopWrapper
from tasks.functions import BackupManger
from settings.config import BACKUP_TIME

"""
Хочу оправдаться за этот мерзкий дизайн ход - я хочю чтобы все фоновые процессы
которые должны исполнятся по расписанию, имели свой "центр" откуда они запускаются
поэтому вот както так.....
"""

backupmanager = BackupManger()


class TaskManager():
    lw = LoopWrapper()


    @lw.interval(seconds=3600) # every hour scanning for backups
    async def run_backups():
        await backupmanager.check_for_backup(frequency=BACKUP_TIME)


    async def onstartup(self):
        await self.run_backups()


    async def onshutdown():
        logging.info("Shutting down...")
        from methods.decorators.peer_manager import peers_objs
        from datatypes.user.get_user import cached_users
        for peer_object in peers_objs.values():
            await peer_object.save()
        for user_object in cached_users.values():
            await user_object.save()
        logging.info("BYE :'(")


    lw.on_startup.append(run_backups())
    lw.on_shutdown.append(onshutdown())