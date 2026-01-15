import requests
import sys
from datetime import datetime

def get_status():
    try:
        # Connect to the running bridge
        print("🔌 Connecting to Dream AI Bridge (port 3000)...")
        
        # 1. Get Evolution Status
        evo_res = requests.get("http://localhost:3000/evolution-status")
        evo_data = evo_res.json()
        
        # 2. Get Autonomous Status
        auto_res = requests.get("http://localhost:3000/autonomous-status")
        auto_data = auto_res.json()

        print("\n🧠 DREAM AI STATUS REPORT")
        print("========================")
        print(f"🕒 Time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"🧬 Evolution System: {evo_data.get('status', 'Unknown')}")
        print(f"🤖 Autonomous Mode:  {auto_data.get('status', 'Unknown')}")
        
        print("\n📝 RECENT ACTIVITY")
        # Depending on how your bridge stores data, we try to grab recent logs/tasks
        recent = evo_data.get('history', [])
        if not recent:
            print("   (No evolution history visible in current buffer)")
        else:
            for item in recent[-3:]:
                print(f"   • {item}")

        print("\n🔧 SELF-CORRECTION STATS")
        print(f"   Files Evolved: {evo_data.get('evolved_count', 0)}")
        print(f"   Errors Caught: {len(evo_data.get('errors', []))}")

    except Exception as e:
        print(f"\n❌ COMMUNICATION ERROR: {e}")
        print("Is the 'bridge.py' running in the other terminal?")

if __name__ == "__main__":
    get_status()
