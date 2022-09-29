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