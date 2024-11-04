import sqlite3
import json
import os

class BaseHandlerV1:

    def __init__(self,*args,**kwargs):
        ...

    def connect(self):
        ...
    
    def sync(self):
        ...

class SQLiteHandler(BaseHandlerV1):

    def __init__(self, file:str, data:dict):
        self.file = file
        self.data = data
        self.connect()
    
    def connect(self):
        self._connection = sqlite3.connect(self.file)
        cursor = self._connection.cursor()

        if os.path.exists(self.file):
            self.data = json.loads(cursor.execute("SELECT * FROM microdb").fetchone()[0])
        else:
            cursor.execute("CREATE TABLE microdb (data TEXT)")
    
    def sync(self):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO microdb (data) VALUES ?",json.dumps(self.data))
        self._connection.commit()
    
    def disconnect(self):
        self.sync()
        self._connection.close()