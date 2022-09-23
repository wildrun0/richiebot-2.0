from vkbottle import LoopWrapper
from .do_backups import BackupManger

"""
Хочу оправдаться за этот мерзкий дизайн ход - я хочю чтобы все фоновые процессы
которые должны исполнятся по расписанию, имели свой "центр" откуда они запускаются
поэтому вот както так.....
"""

backupmanager = BackupManger()

class TaskManager():
    lw = LoopWrapper()


    @lw.interval(seconds=3600) # every hour
    async def run_backups():
        await backupmanager.backup()