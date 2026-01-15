"""
BROWSER HISTORY CAPTURE
Monitors browsing patterns to understand your information gathering behavior
Captures browser history from Firefox, Chrome, Brave, etc.
"""

import os
import sqlite3
import datetime
import time
from typing import Dict, List
from pathlib import Path
import json

class BrowserHistoryCapture:
    """Monitors and learns from your browsing patterns"""
    
    def __init__(self):
        self.browsers = self._find_browsers()
        self.history_cache: List[Dict] = []
    
    def _find_browsers(self) -> Dict[str, str]:
        """Find installed browsers and their data directories"""
        home = os.path.expanduser("~")
        browsers = {
            "firefox": os.path.join(home, ".mozilla/firefox"),
            "chrome": os.path.join(home, ".config/google-chrome"),
            "chromium": os.path.join(home, ".config/chromium"),
            "brave": os.path.join(home, ".config/BraveSoftware/Brave-Browser"),
            "edge": os.path.join(home, ".config/microsoft-edge")
        }
        
        # Filter to only installed browsers
        installed = {}
        for browser, path in browsers.items():
            if os.path.exists(path):
                installed[browser] = path
        
        return installed
    
    def get_firefox_history(self, limit: int = 50) -> List[Dict]:
        """Extract browsing history from Firefox"""
        try:
            profile_path = os.path.join(self.browsers.get("firefox", ""), "Profiles")
            if not os.path.exists(profile_path):
                return []
            
            # Find the default profile
            profiles = [d for d in os.listdir(profile_path) if d.endswith(".default-release")]
            if not profiles:
                return []
            
            db_path = os.path.join(profile_path, profiles[0], "places.sqlite")
            if not os.path.exists(db_path):
                return []
            
            # Copy database (Firefox locks it)
            import tempfile
            import shutil
            temp_db = tempfile.mktemp()
            shutil.copy(db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Query recent history
            query = """
                SELECT title, url, visit_date FROM moz_historyvisits
                JOIN moz_places ON moz_historyvisits.place_id = moz_places.id
                ORDER BY visit_date DESC LIMIT ?
            """
            
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            
            history = []
            for title, url, visit_date in results:
                # Firefox stores timestamps in microseconds
                visit_time = datetime.datetime.fromtimestamp(visit_date / 1000000)
                history.append({
                    "browser": "firefox",
                    "title": title,
                    "url": url,
                    "visit_time": visit_time.isoformat(),
                    "timestamp": datetime.datetime.now().isoformat()
                })
            
            conn.close()
            os.remove(temp_db)
            
            return history
        except Exception as e:
            return []
    
    def get_chrome_history(self, limit: int = 50) -> List[Dict]:
        """Extract browsing history from Chrome/Chromium"""
        try:
            chrome_path = self.browsers.get("chromium") or self.browsers.get("chrome")
            if not chrome_path:
                return []
            
            db_path = os.path.join(chrome_path, "Default", "History")
            if not os.path.exists(db_path):
                return []
            
            # Copy database (Chrome locks it)
            import tempfile
            import shutil
            temp_db = tempfile.mktemp()
            shutil.copy(db_path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            query = """
                SELECT title, url, last_visit_time FROM urls
                ORDER BY last_visit_time DESC LIMIT ?
            """
            
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            
            history = []
            for title, url, last_visit_time in results:
                # Chrome stores timestamps as microseconds since 1601-01-01
                # Convert to Unix timestamp
                windows_epoch = 116444736000000000  # 100-nanosecond intervals since 1601
                visit_time = datetime.datetime.fromtimestamp((last_visit_time - windows_epoch) / 10000000)
                
                history.append({
                    "browser": "chromium",
                    "title": title,
                    "url": url,
                    "visit_time": visit_time.isoformat(),
                    "timestamp": datetime.datetime.now().isoformat()
                })
            
            conn.close()
            os.remove(temp_db)
            
            return history
        except Exception as e:
            return []
    
    def analyze_browsing_patterns(self) -> Dict:
        """Analyze what topics/domains you research"""
        all_history = self.get_firefox_history(100) + self.get_chrome_history(100)
        
        domains = {}
        topics = {}
        
        for visit in all_history:
            url = visit["url"]
            title = visit["title"] or ""
            
            # Extract domain
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc
                if domain:
                    if domain not in domains:
                        domains[domain] = {"count": 0, "titles": []}
                    domains[domain]["count"] += 1
                    if title:
                        domains[domain]["titles"].append(title)
            except:
                pass
            
            # Extract keywords from title
            keywords = title.lower().split()
            for keyword in keywords:
                if len(keyword) > 3 and keyword not in ['the', 'and', 'for', 'from', 'with', 'this', 'that']:
                    if keyword not in topics:
                        topics[keyword] = 0
                    topics[keyword] += 1
        
        return {
            "top_domains": sorted(domains.items(), key=lambda x: x[1]["count"], reverse=True)[:10],
            "top_topics": sorted(topics.items(), key=lambda x: x[1], reverse=True)[:20],
            "total_history_entries": len(all_history),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def get_current_browser_tab(self) -> Dict:
        """Try to detect what browser tab is currently active (if possible)"""
        try:
            # This is browser-dependent and may not always work
            # For now, return placeholder
            return {
                "note": "Browser tab detection requires browser extensions",
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def observe(self) -> Dict:
        """Get current browsing activity snapshot"""
        return {
            "recent_visits": self.get_firefox_history(20) or self.get_chrome_history(20),
            "browsing_patterns": self.analyze_browsing_patterns(),
            "active_tab": self.get_current_browser_tab(),
            "browsers_found": list(self.browsers.keys()),
            "timestamp": datetime.datetime.now().isoformat()
        }


if __name__ == "__main__":
    browser = BrowserHistoryCapture()
    print("🌐 Browser History Capture Started")
    
    data = browser.observe()
    print(f"\n--- Browser Activity ---")
    print(f"Browsers Found: {data['browsers_found']}")
    print(f"Recent Visits: {len(data['recent_visits'])}")
    for visit in data['recent_visits'][:3]:
        print(f"  - {visit['title'][:50]} ({visit['browser']})")
    
    print(f"\nBrowsing Patterns:")
    patterns = data['browsing_patterns']
    print(f"  Top Domains: {len(patterns['top_domains'])}")
    print(f"  Top Topics: {len(patterns['top_topics'])}")
