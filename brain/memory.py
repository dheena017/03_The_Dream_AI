import sqlite3
import datetime
import os
import json

class ObservationMemory:
    def __init__(self, db_path="brain/memory/observations.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # FIX: Check same thread false allows multiple connections
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        
        # FIX: WAL Mode prevents 'Database Locked' errors
        self.conn.execute("PRAGMA journal_mode=WAL;") 
        
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                type TEXT,
                data TEXT
            )
        ''')
        self.conn.commit()

    def store_observation(self, type, data):
        try:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(data, dict):
                data = json.dumps(data)
            self.cursor.execute("INSERT INTO observations (timestamp, type, data) VALUES (?, ?, ?)", (ts, type, str(data)))
            self.conn.commit()
        except Exception as e:
            print(f"⚠️ Memory Error: {e}")

    def get_recent_observations(self, limit=10):
        self.cursor.execute("SELECT * FROM observations ORDER BY id DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()
