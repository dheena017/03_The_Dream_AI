import time
import sys
import os
from pathlib import Path

# 1. Ensure 'brain' directory is in Python path so we can import 'utils'
current_dir = Path(__file__).parent.absolute()
sys.path.append(str(current_dir))

# 2. Attempt import
try:
    from utils.sanitizer import sanitize_file
except ImportError:
    print("❌ Error: Could not import 'utils.sanitizer'.")
    print("   Make sure 'brain/utils/sanitizer.py' exists.")
    sys.exit(1)

# 3. Define Directory
GEN_DIR = Path("brain/generated")

def run_immune_system():
    # Safety: immune scanner off by default to avoid unexpected edits.
    immune_enabled = False
    try:
        if os.getenv('DREAM_AI_IMMUNE', '0') == '1':
            immune_enabled = True
        else:
            if Path('brain/IMMUNE_ENABLED').exists():
                immune_enabled = True
    except Exception:
        immune_enabled = False

    if not immune_enabled:
        print("🛡️ Immune System is disabled by default. Enable with DREAM_AI_IMMUNE=1 or create brain/IMMUNE_ENABLED.")
        return

    # Ensure the directory exists
    GEN_DIR.mkdir(parents=True, exist_ok=True)

    print("🛡️  Dream AI Immune System Active")
    print(f"   Watching: {GEN_DIR}")
    print("   (Press Ctrl+C to stop)")
    
    while True:
        try:
            # Check all .py files in generated directory
            # We list them first to avoid modifying the list while iterating
            files = list(GEN_DIR.glob("*.py"))
            
            for py_file in files:
                # sanitize_file returns True if it had to clean something
                if sanitize_file(str(py_file)):
                    print(f"   🦠 Neutralized non-code elements in {py_file.name}")
            
            # Wait 2 seconds before next scan
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n🛡️  Immune System standing down.")
            break
        except Exception as e:
            print(f"⚠️  Immune System error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_immune_system()