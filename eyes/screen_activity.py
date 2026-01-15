"""
SCREEN ACTIVITY TRACKER
Monitors which application is focused, window titles, and screen activity
"""

import subprocess
import datetime
import time
from typing import Dict, List

class ScreenActivityTracker:
    """Tracks what's currently on your screen"""
    
    def __init__(self):
        self.previous_window = None
        self.activity_log: List[Dict] = []
    
    def get_active_window(self) -> Dict:
        """Get the currently focused window"""
        try:
            # Get window ID and name using xdotool
            window_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode("utf-8").strip()
            window_name = subprocess.check_output(["xdotool", "getwindowname", window_id]).decode("utf-8").strip()
            
            # Extract app name from window title
            app_name = window_name.split(" - ")[0] if " - " in window_name else window_name
            
            return {
                "window_id": window_id,
                "window_title": window_name,
                "app_name": app_name,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "window_id": "unknown",
                "window_title": "Error reading window",
                "app_name": "System Idle",
                "timestamp": datetime.datetime.now().isoformat(),
                "error": str(e)
            }
    
    def get_screen_focus_changes(self) -> List[Dict]:
        """Detect when user switches between applications"""
        current_window = self.get_active_window()
        
        if current_window["window_id"] != self.previous_window:
            event = {
                "event_type": "focus_change",
                "from": self.previous_window,
                "to": current_window["app_name"],
                "timestamp": current_window["timestamp"],
                "full_data": current_window
            }
            self.activity_log.append(event)
            self.previous_window = current_window["window_id"]
            return [event]
        
        return []
    
    def get_screenshot_metadata(self) -> Dict:
        """Get screen resolution and display info"""
        try:
            output = subprocess.check_output(["xrandr"]).decode("utf-8")
            lines = output.split("\n")
            
            for line in lines:
                if " connected" in line and "primary" in line:
                    # Extract resolution like "1920x1080+0+0"
                    parts = line.split()
                    resolution = parts[2].split("+")[0]
                    return {
                        "resolution": resolution,
                        "status": "connected",
                        "timestamp": datetime.datetime.now().isoformat()
                    }
            
            return {"resolution": "unknown", "status": "disconnected"}
        except Exception as e:
            return {"error": str(e)}
    
    def observe(self) -> Dict:
        """Get current screen state"""
        return {
            "active_window": self.get_active_window(),
            "display_info": self.get_screenshot_metadata(),
            "focus_changes": self.get_screen_focus_changes(),
            "timestamp": datetime.datetime.now().isoformat()
        }


if __name__ == "__main__":
    tracker = ScreenActivityTracker()
    print("🖥️  Screen Activity Tracker Started")
    
    for i in range(5):
        data = tracker.observe()
        print(f"\n--- Observation {i+1} ---")
        print(f"Active App: {data['active_window']['app_name']}")
        print(f"Window: {data['active_window']['window_title']}")
        time.sleep(2)
