import os
import logging
import aioshutil

from pathlib import Path
from typing import Literal
from datetime import datetime, timedelta


class BackupManger():
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
        logging.info("BackupManager initialized")


    async def _backup(self):
        start_time = datetime.timestamp(datetime.now())
        logging.info("backup in process..")
        backup_folder_name = datetime.strftime(self.startup_date, self.date_format)
        new_backup_folder = Path(self.default_folder, backup_folder_name)

        for folder in self.dirs_to_backup:
            await aioshutil.copytree(Path(folder), Path(new_backup_folder, folder))

        end_time = datetime.timestamp(datetime.now())
        logging.warning(f"backup done, elapsed time: {end_time - start_time:.2f} sec.")
        self.last_backup = datetime.now()


    async def check_for_backup(self, frequency: Literal["monthly", "weekly", "daily", "hourly"] = "daily"):
        self.startup_date = datetime.now()
        gap_seconds = self.frequency_days[frequency]
        self.date_format = '%d.%m.%Y %H-%M' if gap_seconds < 86400 else self.date_format
        if not self.last_backup:
            if not next(os.scandir(self.default_folder), None):
                logging.warning("No backups found!")
                gap = timedelta(seconds=gap_seconds)
                self.last_backup = self.startup_date - gap # типа вчера был бэкап, нада новый будет!!
            else:
                backups_sorted = sorted(
                    list(Path(self.default_folder).rglob('[0-9]*.[0-9]*.*[0-9]*')), 
                    key=lambda x: Path.stat(x).st_mtime, reverse=True
                )
                self.last_backup = datetime.fromtimestamp(backups_sorted[0].stat().st_mtime)
        logging.debug(f"Checking last backup time: {self.last_backup.strftime(self.date_format)}")
        backup_gap = (self.startup_date - self.last_backup)
        if (backup_gap.total_seconds() >= gap_seconds):
            await self._backup()
        else:
            logging.debug("No backup needed")