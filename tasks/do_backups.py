import aioshutil
import logging
from datetime import datetime, timedelta
from utilities import Utils as utils
from pathlib import Path


class BackupManger():
    def __init__(self):
        self.last_backup = None
        self.dirs_to_backup = ["peers"]
        self.default_folder = Path("backups")
        self.default_folder.mkdir(exist_ok=True)
        self.date_format = "%d.%m.%Y"
        self.startup_date = datetime.today().date()


    async def _backup(self):
        start_time = datetime.timestamp(datetime.now())
        logging.info("backup in process..")
        backup_folder_name = datetime.strftime(self.startup_date, self.date_format)
        new_backup_folder = Path(self.default_folder, backup_folder_name)

        for folder in self.dirs_to_backup:
            await aioshutil.copytree(Path(folder), Path(new_backup_folder, folder))

        end_time = datetime.timestamp(datetime.now())
        logging.info(f"backup done, elapsed time: {end_time - start_time:.2f} sec.")
        self.last_backup = datetime.today().date()


    async def backup(self):
        if utils.dir_empty(self.default_folder): # можно было бы просто проверить len(backups_sorted) но это наибыстрейший (!) способ
            logging.info("No backups found!")
            gap = timedelta(days=1)
            self.last_backup = self.startup_date - gap # типа вчера был бэкап, нада новый будет!!
        else:
            backups_sorted = sorted(
                list(Path(self.default_folder).rglob('[0-9]*.[0-9]*.*[0-9]*')), 
                key=lambda x: Path.stat(x).st_mtime, reverse=False
            )
            self.last_backup = datetime.strptime(backups_sorted[0].name, self.date_format).date()
            logging.info(f"Last backup time: {self.last_backup}")

        if (self.startup_date - self.last_backup).days >= 1:
            await self._backup()