"""
Dream AI - Eyes System
Complete observation module for "The Digital Descendant"

This system monitors:
✓ Screen Activity - What applications you use, window changes
✓ Input Activity - Typing patterns, mouse movement, idle time (privacy-first)
✓ File Access - Project activity, file modifications, workflows
✓ Browser History - Topics you research, domains you visit

All data flows to the Brain via a central coordinator.
Privacy-first: No keystroke recording, no screenshot storage.
"""

__version__ = "1.0.0"
__author__ = "Dream AI"
__description__ = "Observation system for autonomous learning AI"

from screen_activity import ScreenActivityTracker
from input_tracker import InputTracker
from file_monitor import FileAccessMonitor
from browser_history import BrowserHistoryCapture
from coordinator import SensorCoordinator

__all__ = [
    'ScreenActivityTracker',
    'InputTracker',
    'FileAccessMonitor',
    'BrowserHistoryCapture',
    'SensorCoordinator',
]


# Quick test function
def quick_test():
    """Run a quick test of all sensors"""
    print("🧪 Testing Dream AI Eyes System\n")
    
    print("1️⃣  Screen Activity:")
    screen = ScreenActivityTracker()
    data = screen.observe()
    print(f"   Active App: {data['active_window']['app_name']}")
    
    print("\n2️⃣  Input Activity:")
    input_t = InputTracker()
    data = input_t.observe()
    print(f"   Typing Intensity: {data['typing_intensity']['typing_intensity']}")
    print(f"   Idle Status: {data['idle_time']['idle_status']}")
    
    print("\n3️⃣  File Access:")
    files = FileAccessMonitor()
    data = files.observe()
    print(f"   Recent Files: {len(data['recent_files'])}")
    print(f"   Active Projects: {len(data['active_projects'])}")
    
    print("\n4️⃣  Browser History:")
    browser = BrowserHistoryCapture()
    data = browser.observe()
    print(f"   Browsers Found: {data['browsers_found']}")
    print(f"   Recent Visits: {len(data['recent_visits'])}")
    
    print("\n✅ All systems operational!")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        quick_test()
    else:
        print(__doc__)
