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


    @lw.interval(seconds=21600) # 4 times at day
    async def run_backups():
        await backupmanager.backup()