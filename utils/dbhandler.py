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
        if os.path.exists(self.file):
            self._connection = sqlite3.connect(self.file)
            cursor = self._connection.cursor()
            self.data.update(json.loads(cursor.execute("SELECT data FROM microdb").fetchone()[0]))
        else:
            self._connection = sqlite3.connect(self.file)
            cursor = self._connection.cursor()
            cursor.execute("CREATE TABLE microdb (id INT KEY, data TEXT)")
            self.data['members'] = {}
            cursor.execute("INSERT INTO microdb (id,data) VALUES (?,?)",(1,json.dumps(self.data)))
            self.sync()
    
    def sync(self):
        cursor = self._connection.cursor()
        cursor.execute("UPDATE microdb SET data = ? WHERE id = ?",(json.dumps(self.data),1))
        self._connection.commit()
    
    def disconnect(self):
        self.sync()
        self._connection.close()