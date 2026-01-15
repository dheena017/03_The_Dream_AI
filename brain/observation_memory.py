"""
OBSERVATION MEMORY SYSTEM
Stores and retrieves observations for pattern analysis
Uses SQLite for persistent storage and fast queries
"""

import sqlite3
import json
import datetime
from typing import Dict, List, Optional
from pathlib import Path
import os
import threading
import time


class ObservationMemory:
    """Persistent storage for all observations from the Eyes system"""
    
    def __init__(self, db_path: str = None):
        """Initialize memory storage"""
        if db_path is None:
            # Default to brain directory
            brain_dir = os.path.dirname(__file__)
            os.makedirs(brain_dir, exist_ok=True)
            db_path = os.path.join(brain_dir, "observations.db")
        
        self.db_path = db_path
        self._db_lock = threading.RLock()  # Recursive lock for thread safety
        self._connection_pool = None
        self._init_database()
    
    def _get_connection(self, timeout: float = 30.0) -> sqlite3.Connection:
        """Get a database connection with proper configuration"""
        max_retries = 5
        retry_delay = 0.1
        
        for attempt in range(max_retries):
            try:
                conn = sqlite3.connect(self.db_path, timeout=timeout, check_same_thread=False)
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA busy_timeout=30000")
                conn.execute("PRAGMA synchronous=NORMAL")
                conn.execute("PRAGMA cache_size=10000")
                conn.execute("PRAGMA temp_store=MEMORY")
                return conn
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() and attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                raise
        
        raise sqlite3.OperationalError("Database locked - could not acquire connection after retries")
    
    def _init_database(self):
        """Create database schema if it doesn't exist"""
        with self._db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
        
        # Main observations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observation_id INTEGER UNIQUE,
                timestamp TEXT NOT NULL,
                raw_data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_obs_timestamp ON observations(timestamp)")
        
        # Extracted data for faster queries
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS screen_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observation_id INTEGER NOT NULL,
                app_name TEXT,
                window_title TEXT,
                timestamp TEXT,
                FOREIGN KEY(observation_id) REFERENCES observations(observation_id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_screen_app ON screen_activity(app_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_screen_time ON screen_activity(timestamp)")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS input_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observation_id INTEGER NOT NULL,
                typing_intensity TEXT,
                idle_status TEXT,
                idle_seconds REAL,
                timestamp TEXT,
                FOREIGN KEY(observation_id) REFERENCES observations(observation_id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_input_time ON input_activity(timestamp)")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observation_id INTEGER NOT NULL,
                file_path TEXT,
                file_extension TEXT,
                file_size INTEGER,
                operation TEXT,
                timestamp TEXT,
                FOREIGN KEY(observation_id) REFERENCES observations(observation_id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_path ON file_activity(file_path)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_time ON file_activity(timestamp)")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS browser_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observation_id INTEGER NOT NULL,
                domain TEXT,
                page_title TEXT,
                url TEXT,
                timestamp TEXT,
                FOREIGN KEY(observation_id) REFERENCES observations(observation_id)
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_browser_domain ON browser_activity(domain)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_browser_time ON browser_activity(timestamp)")
        
        conn.commit()
        conn.close()
    
    def store_observation(self, observation: Dict) -> bool:
        """Store a complete observation"""
        with self._db_lock:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    conn = self._get_connection()
                    cursor = conn.cursor()
                    
                    obs_id = observation.get("observation_id")
                    timestamp = observation.get("timestamp")
                    raw_data = json.dumps(observation)
                    
                    # Use transaction for atomic operation
                    cursor.execute("BEGIN IMMEDIATE")
                    
                    # Store raw observation
                    cursor.execute("""
                        INSERT OR REPLACE INTO observations (observation_id, timestamp, raw_data)
                        VALUES (?, ?, ?)
                    """, (obs_id, timestamp, raw_data))
                    
                    # Extract and store structured data
                    self._extract_screen_data(cursor, obs_id, observation, timestamp)
                    self._extract_input_data(cursor, obs_id, observation, timestamp)
                    self._extract_file_data(cursor, obs_id, observation, timestamp)
                    self._extract_browser_data(cursor, obs_id, observation, timestamp)
                    
                    conn.commit()
                    conn.close()
                    return True
                except sqlite3.IntegrityError:
                    # Observation already stored
                    try:
                        conn.close()
                    except:
                        pass
                    return False
                except sqlite3.OperationalError as e:
                    try:
                        conn.rollback()
                        conn.close()
                    except:
                        pass
                    if "locked" in str(e).lower() and attempt < max_retries - 1:
                        time.sleep(0.1 * (2 ** attempt))
                        continue
                    print(f"Error storing observation (attempt {attempt + 1}/{max_retries}): {e}")
                    return False
                except Exception as e:
                    try:
                        conn.close()
                    except:
                        pass
                    print(f"Error storing observation: {e}")
                    return False
            
            return False
    
    def _extract_screen_data(self, cursor, obs_id, observation, timestamp):
        """Extract screen activity data"""
        try:
            screen = observation.get("sensors", {}).get("screen", {})
            active_window = screen.get("active_window", {})
            
            app_name = active_window.get("app_name")
            window_title = active_window.get("window_title")
            
            if app_name or window_title:
                cursor.execute("""
                    INSERT INTO screen_activity 
                    (observation_id, app_name, window_title, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (obs_id, app_name, window_title, timestamp))
        except Exception as e:
            pass
    
    def _extract_input_data(self, cursor, obs_id, observation, timestamp):
        """Extract input activity data"""
        try:
            input_data = observation.get("sensors", {}).get("input", {})
            typing = input_data.get("typing_intensity", {})
            idle = input_data.get("idle_time", {})
            
            typing_intensity = typing.get("typing_intensity")
            idle_status = idle.get("idle_status")
            idle_seconds = idle.get("idle_time_seconds")
            
            if typing_intensity or idle_status:
                cursor.execute("""
                    INSERT INTO input_activity
                    (observation_id, typing_intensity, idle_status, idle_seconds, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (obs_id, typing_intensity, idle_status, idle_seconds, timestamp))
        except Exception as e:
            pass
    
    def _extract_file_data(self, cursor, obs_id, observation, timestamp):
        """Extract file activity data"""
        try:
            files = observation.get("sensors", {}).get("files", {})
            recent = files.get("recent_files", [])
            
            for file_info in recent[:10]:  # Store top 10 recent files
                cursor.execute("""
                    INSERT INTO file_activity
                    (observation_id, file_path, file_extension, file_size, operation, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    obs_id,
                    file_info.get("path"),
                    file_info.get("extension"),
                    file_info.get("size_bytes"),
                    "modified",
                    timestamp
                ))
        except Exception as e:
            pass
    
    def _extract_browser_data(self, cursor, obs_id, observation, timestamp):
        """Extract browser activity data"""
        try:
            browser = observation.get("sensors", {}).get("browser", {})
            visits = browser.get("recent_visits", [])
            
            for visit in visits[:10]:  # Store top 10 recent visits
                cursor.execute("""
                    INSERT INTO browser_activity
                    (observation_id, domain, page_title, url, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    obs_id,
                    visit.get("browser"),
                    visit.get("title"),
                    visit.get("url"),
                    timestamp
                ))
        except Exception as e:
            pass
    
    def get_observations(self, limit: int = 100, hours: int = 24) -> List[Dict]:
        """Get recent observations"""
        with self._db_lock:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
            
            try:
                cursor.execute("""
                    SELECT raw_data FROM observations
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (cutoff_time.isoformat(), limit))
                
                results = []
                for row in cursor.fetchall():
                    results.append(json.loads(row["raw_data"]))
                
                return results
            finally:
                conn.close()
    
    def get_app_usage(self, hours: int = 24) -> Dict:
        """Analyze which apps you use most"""
        with self._db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
            
            try:
                cursor.execute("""
                    SELECT app_name, COUNT(*) as count, 
                           MIN(timestamp) as first_seen, MAX(timestamp) as last_seen
                    FROM screen_activity
                    WHERE timestamp > ? AND app_name IS NOT NULL
                    GROUP BY app_name
                    ORDER BY count DESC
                """, (cutoff_time.isoformat(),))
                
                results = {}
                for row in cursor.fetchall():
                    app_name, count, first_seen, last_seen = row
                    results[app_name] = {
                        "observation_count": count,
                        "first_seen": first_seen,
                        "last_seen": last_seen
                    }
                
                return results
            finally:
                conn.close()
    
    def get_activity_timeline(self, hours: int = 24) -> List[Dict]:
        """Get chronological timeline of your activity"""
        with self._db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
            
            try:
                cursor.execute("""
                    SELECT timestamp, app_name, typing_intensity, idle_status
                    FROM screen_activity
                    LEFT JOIN input_activity USING (timestamp)
                    WHERE timestamp > ?
                    ORDER BY timestamp DESC
                """, (cutoff_time.isoformat(),))
                
                results = []
                for row in cursor.fetchall():
                    timestamp, app_name, typing, idle = row
                    results.append({
                        "timestamp": timestamp,
                        "app": app_name,
                        "typing": typing,
                        "idle": idle
                    })
                
                return results
            finally:
                conn.close()
    
    def get_memory_stats(self) -> Dict:
        """Get statistics about stored memory"""
        with self._db_lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute("SELECT COUNT(*) FROM observations")
                obs_count = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT app_name) FROM screen_activity")
                unique_apps = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT domain) FROM browser_activity")
                unique_domains = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(DISTINCT file_path) FROM file_activity")
                unique_files = cursor.fetchone()[0]
                
                cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM observations")
                min_time, max_time = cursor.fetchone()
                
                return {
                    "total_observations": obs_count,
                    "unique_applications": unique_apps,
                    "unique_domains": unique_domains,
                    "unique_files": unique_files,
                    "memory_span": f"{min_time} to {max_time}" if min_time else "No data"
                }
            finally:
                conn.close()


if __name__ == "__main__":
    memory = ObservationMemory()
    print("📦 Observation Memory System")
    print(f"Database: {memory.db_path}")
    
    stats = memory.get_memory_stats()
    print(f"\nMemory Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
