from sql_commands import databaseManager

class tagger():

    def __init__(self, dbm:databaseManager) -> None:
        self.db = dbm
        