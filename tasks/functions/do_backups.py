import os
import shutil

from settings.config import BACKUPS_AMOUNT
from aiofiles.os import wrap
from pathlib import Path
from loader import log
from typing import Literal
from datetime import datetime, timedelta


copytree = wrap(shutil.copytree)
class BackupManger:
    __slots__ = 'last_backup', 'dirs_to_backup', 'default_folder', 'date_format', 'frequency_days', 'startup_date'
    def __init__(self):
        self.last_backup = None
        self.dirs_to_backup = ["peers"]
        self.default_folder = Path("backups")
        self.default_folder.mkdir(exist_ok=True)
        self.date_format = "%d.%m.%Y"

        self.frequency_days = {
            "monthly":  2592000,   #do not recommend at all. Бот столько не проработает без крашей)
            "weekly":   604800,
            "daily":    86400,
            "hourly":   3600
        }
        log.info("BackupManager initialized")


    def _del_last(self):
        oldest_backup = min(self.default_folder.resolve().glob('**/*'), key=os.path.getctime)
        log.warning(f"Deleting oldest backup '{oldest_backup}'")
        shutil.rmtree(oldest_backup)


    async def _backup(self):
        start_time = datetime.timestamp(datetime.now())
        log.info("backup in process..")
        backup_folder_name = datetime.strftime(self.startup_date, self.date_format)
        new_backup_folder = Path(self.default_folder, backup_folder_name)

        for folder in self.dirs_to_backup:
            src = Path(folder)
            dst = Path(new_backup_folder, folder)
            await copytree(src, dst)

        end_time = datetime.timestamp(datetime.now())
        log.warning(f"backup done, elapsed time: {end_time - start_time:.2f} sec.")
        self.last_backup = datetime.now()
        backups_in_folder = len(list(self.default_folder.glob('*')))
        if backups_in_folder > BACKUPS_AMOUNT:
            self._del_last()


    async def check_for_backup(self, frequency: Literal["monthly", "weekly", "daily", "hourly"] = "daily"):
        self.startup_date = datetime.now()
        gap_seconds = self.frequency_days[frequency]
        self.date_format = '%d.%m.%Y %H-%M' if gap_seconds < 86400 else self.date_format
        if not self.last_backup:
            if not next(os.scandir(self.default_folder), None):
                log.warning("No backups found!")
                gap = timedelta(seconds=gap_seconds)
                self.last_backup = self.startup_date - gap # типа вчера был бэкап, нада новый будет!!
            else:
                backups_sorted = sorted(
                    list(Path(self.default_folder).rglob('[0-9]*.[0-9]*.*[0-9]*')),
                    key=lambda x: Path.stat(x).st_mtime, reverse=True
                )
                self.last_backup = datetime.fromtimestamp(backups_sorted[0].stat().st_mtime)
        log.info(f"Checking last backup time: {self.last_backup.strftime(self.date_format)}")
        backup_gap = (self.startup_date - self.last_backup)
        if (backup_gap.total_seconds() >= gap_seconds):
            await self._backup()
        else:
            log.info("No backup needed")
