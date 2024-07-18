import sqlite3
import threading
import time
import os
from django.conf import settings
from django.db import connections


class BackupManager:
    """
    Singleton class to manage database backups in a separate background thread.

    This class ensures that only one instance of the backup thread runs,
    performing periodic backups of the database to a specified local path.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        Creates a new instance of the BackupManager class if one does not already exist.
        Uses a lock to ensure thread-safe singleton instantiation.

        :return: The singleton instance of BackupManager.
        :rtype: BackupManager
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(BackupManager, cls).__new__(cls)
                    cls._instance._init_thread()
        return cls._instance

    def _init_thread(self):
        """
        Initializes the backup thread and starts it.
        The thread runs the backup_database method as a daemon.
        """
        self.backup_thread = threading.Thread(target=self.backup_database, daemon=True)
        self.backup_thread.start()

    def backup_database(self):
        """
        Performs periodic backups of the database to a local path.
        This method runs in a continuous loop, creating a backup every hour.

        The backup is saved as a SQL dump file in the 'backup' directory
        within the project's base directory.
        """

        while True:
            print("backing up database")
            db_path = os.path.join(settings.BASE_DIR, "backup")
            if not os.path.exists(db_path):
                os.makedirs(db_path)

            with connections["default"].cursor() as cursor:
                with open(os.path.join(db_path, "backup.sql"), "w") as f:
                    for line in connections["default"].connection.iterdump():
                        f.write(f"{line}\n")

            time.sleep(10)  # Backup every hour
