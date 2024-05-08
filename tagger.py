from sql_commands import databaseManager
from os import path

class tagger():

    def __init__(self, dbm:databaseManager):
        self.db = dbm

    def tag_filetype(self,filename):
        filepath = self.db.get_filepath(filename)
        path, ext = path.splitext(filepath)
        self.db.get_filepath(filename)
        self.db.add_tag_to_file(path, filename)

    def tag_reversed(self, filename):
        self.db.add_tag_to_file("reversed", filename)
    
    def tag_duplicate(self, filename):
        self.db.add_tag_to_file("duplicate", filename)

    def tag_trim(self, filename):
        self.db.add_tag_to_file("trimmed", filename)

    def tag_rec(self, filename):
        self.db.add_tag_to_file("rec", filename)

    def tag_sped(self, filename):
        self.db.add_tag_to_file("sped up", filename)