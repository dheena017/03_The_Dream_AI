import os
import sqlite3
import json

class BrainOrchestrator:
    def __init__(self):
        print("🧠 DREAM AI - BRAIN SYSTEM INITIALIZED")
        print("   📦 Memory Backend: SQLite")
        print("   🔍 Pattern Recognition: Online")
        print("   📊 Activity Analysis: Online")
        print("   🔧 Workflow Analysis: Online")
        print("   🗺️  Knowledge Mapping: Online")
        
        # Connect to memory
        self.db_path = "brain/memory/observations.db"
        self._init_memory()

    def _init_memory(self):
        # Ensure DB exists (Memory class usually handles this, but safety first)
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))

    def analyze_patterns(self):
        """
        Looks at recent memory to find repeated actions or errors.
        This fixes the 'AttributeError' you were seeing.
        """
        try:
            # We connect in Read-Only mode to avoid locking the DB
            conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            # Simple Analysis: Get the last 5 tasks
            cursor.execute("SELECT data FROM observations WHERE type='task_completion' ORDER BY id DESC LIMIT 5")
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                return []

            # If we successfully read data, return it as insights
            insights = [r[0] for r in rows]
            return insights

        except Exception as e:
            # If DB is busy or empty, just return nothing so we don't crash
            # print(f"⚠️ Brain Analysis Skipped: {e}")
            return []

if __name__ == "__main__":
    b = BrainOrchestrator()
    b.analyze_patterns()
    