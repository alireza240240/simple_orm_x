

import sqlite3

class Database:
    _instance = None

    def __new__(cls , db_name="data.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect(db_name)
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance
        
    @classmethod    
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        
        return cls._instance