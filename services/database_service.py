from database.sqlite_manager import SQLiteManager


class DatabaseService:

    def __init__(self):

        self.db = SQLiteManager()

        self.db.crear_base()