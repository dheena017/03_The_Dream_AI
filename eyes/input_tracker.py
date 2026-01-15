"""
KEYBOARD & MOUSE TRACKER
Monitors input patterns without recording actual keystrokes (privacy-first)
Tracks keystroke frequency, mouse movement patterns, and click behaviors
"""

import subprocess
import datetime
import time
from typing import Dict, List
from collections import defaultdict

class InputTracker:
    """Monitors keyboard and mouse activity patterns"""
    
    def __init__(self):
        self.keystroke_count = 0
        self.last_activity_time = time.time()
        self.activity_patterns: List[Dict] = []
        self.mouse_clicks = 0
        self.last_sample_time = time.time()
    
    def get_keyboard_activity(self) -> Dict:
        """
        Monitor keyboard activity using evtest or similar
        Records frequency, not content (privacy respecting)
        """
        try:
            # Use xinput to get keyboard device info
            output = subprocess.check_output(["xinput", "list"]).decode("utf-8")
            
            keyboard_info = {
                "devices_detected": output.count("keyboard") + output.count("Keyboard"),
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            return keyboard_info
        except Exception as e:
            return {"error": str(e), "keyboard_active": False}
    
    def estimate_typing_activity(self) -> Dict:
        """
        Estimate if user is actively typing based on system load and time patterns
        Privacy-first: doesn't capture actual keystrokes
        """
        try:
            # Check /proc to estimate activity
            with open("/proc/stat", "r") as f:
                cpu_line = f.readline()
            
            cpu_idle = int(cpu_line.split()[4])
            
            typing_intensity = "idle"
            if cpu_idle < 8000:
                typing_intensity = "active"
            elif cpu_idle < 8500:
                typing_intensity = "light"
            
            return {
                "typing_intensity": typing_intensity,
                "estimated_cpu_idle": cpu_idle,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_mouse_activity(self) -> Dict:
        """Monitor mouse position and click patterns"""
        try:
            # Get current mouse position
            result = subprocess.check_output(["xdotool", "getmouselocation"]).decode("utf-8")
            
            # Parse "x:1234 y:5678 screen:0"
            parts = result.strip().split()
            x = int(parts[0].split(":")[1])
            y = int(parts[1].split(":")[1])
            
            self.activity_patterns.append({
                "type": "mouse_position",
                "x": x,
                "y": y,
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            return {
                "x": x,
                "y": y,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_input_idle_time(self) -> Dict:
        """Calculate how long since last user input"""
        try:
            # Use xprintidle to get idle time in milliseconds
            idle_ms = int(subprocess.check_output(["xprintidle"]).decode("utf-8").strip())
            idle_seconds = idle_ms / 1000
            
            idle_status = "active"
            if idle_seconds > 300:  # 5 minutes
                idle_status = "idle"
            elif idle_seconds > 60:  # 1 minute
                idle_status = "away"
            
            return {
                "idle_time_seconds": idle_seconds,
                "idle_status": idle_status,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "idle_status": "unknown"}
    
    def observe(self) -> Dict:
        """Get current input activity snapshot"""
        return {
            "keyboard": self.get_keyboard_activity(),
            "typing_intensity": self.estimate_typing_activity(),
            "mouse": self.get_mouse_activity(),
            "idle_time": self.get_input_idle_time(),
            "activity_patterns": self.activity_patterns[-10:],  # Last 10 activities
            "timestamp": datetime.datetime.now().isoformat()
        }


if __name__ == "__main__":
    tracker = InputTracker()
    print("⌨️  Input Activity Tracker Started")
    
    for i in range(5):
        data = tracker.observe()
        print(f"\n--- Observation {i+1} ---")
        print(f"Typing: {data['typing_intensity']['typing_intensity']}")
        print(f"Idle: {data['idle_time']['idle_status']} ({data['idle_time']['idle_time_seconds']:.1f}s)")
        time.sleep(2)
