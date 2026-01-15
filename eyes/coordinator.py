"""
SENSOR COORDINATOR
Central hub that orchestrates all observation systems (eyes) and sends data to the brain
Coordinates screen tracking, input monitoring, file access, browser history, and web search
"""

import sys
import os
import json
import datetime
import time
import requests
from typing import Dict, List

# Import all sensor modules
sys.path.insert(0, os.path.dirname(__file__))
from screen_activity import ScreenActivityTracker
from input_tracker import InputTracker
from file_monitor import FileAccessMonitor
from browser_history import BrowserHistoryCapture
from google_search import GoogleSearchCapability


class SensorCoordinator:
    """Master controller for all observation systems"""
    
    def __init__(self, brain_url: str = "http://localhost:3000/brain-log", 
                 google_api_key: str = None, google_search_engine_id: str = None):
        self.brain_url = brain_url
        
        # Initialize all sensors
        self.screen_tracker = ScreenActivityTracker()
        self.input_tracker = InputTracker()
        self.file_monitor = FileAccessMonitor()
        self.browser_capture = BrowserHistoryCapture()
        
        # Initialize Google Search capability
        self.search_capability = GoogleSearchCapability(
            api_key=google_api_key or os.getenv("GOOGLE_API_KEY"),
            search_engine_id=google_search_engine_id or os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        )
        
        self.observation_count = 0
        self.failed_sends = 0
        
        print("🧠 DREAM AI - EYES SYSTEM INITIALIZED")
        print(f"   📡 All Sensors Online")
        print(f"   🔍 Google Search: {'✅ Enabled' if self.search_capability.is_available else '⚠️  Fallback (DuckDuckGo)'}")
        print(f"   🎯 Brain Target: {brain_url}")
        print(f"   ⏰ Monitoring Started: {datetime.datetime.now().isoformat()}")
    
    def collect_observation(self, include_browser: bool = False) -> Dict:
        """
        Collect data from all sensors
        This is what the AI "perceives" about your activity
        """
        observation = {
            "observation_id": self.observation_count,
            "timestamp": datetime.datetime.now().isoformat(),
            "sensors": {}
        }
        
        try:
            # SENSOR 1: Screen Activity
            observation["sensors"]["screen"] = self.screen_tracker.observe()
        except Exception as e:
            observation["sensors"]["screen"] = {"error": str(e)}
        
        try:
            # SENSOR 2: Input Activity
            observation["sensors"]["input"] = self.input_tracker.observe()
        except Exception as e:
            observation["sensors"]["input"] = {"error": str(e)}
        
        try:
            # SENSOR 3: File Access
            observation["sensors"]["files"] = self.file_monitor.observe()
        except Exception as e:
            observation["sensors"]["files"] = {"error": str(e)}
        
        try:
            # SENSOR 4: Browser History (run less frequently)
            if include_browser:
                observation["sensors"]["browser"] = self.browser_capture.observe()
        except Exception as e:
            observation["sensors"]["browser"] = {"error": str(e)}
        
        return observation
    
    def search_web(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search the web for information
        Brain can request searches when learning about topics
        """
        try:
            results = self.search_capability.search(query, max_results=max_results)
            return results
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def send_observation_to_brain(self, observation: Dict) -> bool:
        """Send observation data to the brain for processing"""
        try:
            response = requests.post(
                self.brain_url,
                json=observation,
                timeout=5
            )
            
            if response.status_code == 200:
                self.observation_count += 1
                return True
            else:
                print(f"❌ Brain rejected observation: {response.status_code}")
                self.failed_sends += 1
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to brain at {self.brain_url}")
            print(f"   💡 Make sure server.js is running!")
            self.failed_sends += 1
            return False
        except Exception as e:
            print(f"❌ Error sending to brain: {e}")
            self.failed_sends += 1
            return False
    
    def run_observation_cycle(self, interval_seconds: int = 10, browser_every_n_cycles: int = 6):
        """
        Main loop: continuously observe and report
        Interval: how often to collect (default 10 seconds)
        Browser: check browser history less frequently (every 60 seconds by default)
        """
        cycle = 0
        
        print(f"\n🔍 Starting observation cycles (every {interval_seconds}s)")
        print(f"🌐 Browser history checked every {interval_seconds * browser_every_n_cycles}s\n")
        
        try:
            while True:
                cycle += 1
                include_browser = (cycle % browser_every_n_cycles == 0)
                
                # Collect all sensor data
                observation = self.collect_observation(include_browser=include_browser)
                
                # Show what we see
                screen_data = observation["sensors"].get("screen", {})
                input_data = observation["sensors"].get("input", {})
                
                print(f"[Cycle {cycle}] ", end="")
                
                if "active_window" in screen_data:
                    app = screen_data["active_window"].get("app_name", "?")
                    print(f"👁️  App: {app[:20]:20s}", end=" | ")
                
                if "idle_time" in input_data:
                    idle = input_data["idle_time"].get("idle_status", "?")
                    print(f"⌨️  {idle:8s}", end=" | ")
                
                if "recent_files" in observation["sensors"].get("files", {}):
                    files_count = len(observation["sensors"]["files"]["recent_files"])
                    print(f"📁 Files: {files_count:2d}", end=" | ")
                
                # Send to brain
                sent = self.send_observation_to_brain(observation)
                print(f"{'✅ Brain' if sent else '❌ Offline'}", end="")
                
                print()  # Newline
                
                # Wait for next cycle
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print(f"\n\n🛑 Observation stopped")
            print(f"   📊 Cycles completed: {cycle}")
            print(f"   ✅ Successful sends: {cycle - self.failed_sends}")
            print(f"   ❌ Failed sends: {self.failed_sends}")


def main():
    """Start the Dream AI observation system"""
    
    # You can customize these settings
    brain_url = os.getenv("DREAM_AI_BRAIN", "http://localhost:3000/brain-log")
    observation_interval = int(os.getenv("DREAM_AI_INTERVAL", "10"))
    browser_check_frequency = int(os.getenv("DREAM_AI_BROWSER_FREQ", "6"))
    
    coordinator = SensorCoordinator(brain_url=brain_url)
    
    # Run the observation loop
    coordinator.run_observation_cycle(
        interval_seconds=observation_interval,
        browser_every_n_cycles=browser_check_frequency
    )


if __name__ == "__main__":
    main()
