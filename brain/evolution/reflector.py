import os
from datetime import datetime

class Reflector:
    def __init__(self):
        # Dynamically find paths so it works on any machine
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.wisdom_path = os.path.join(base_dir, "brain/wisdom.txt")
        self.gen_path = os.path.join(base_dir, "brain/generated")

    def reflect(self):
        print("🧐 Reflector: Analyzing performance...")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if generated folder exists
        if not os.path.exists(self.gen_path):
            os.makedirs(self.gen_path)

        # LOGIC: Check recent files
        files = sorted(os.listdir(self.gen_path), key=lambda x: os.path.getctime(os.path.join(self.gen_path, x)))
        
        if not files:
            insight = f"[{timestamp}] CRITICAL: No output files generated. Architecture failure."
        else:
            latest_file = files[-1]
            insight = f"[{timestamp}] SUCCESS: Evolution stable. Latest creation: {latest_file}"

        try:
            with open(self.wisdom_path, "a") as f:
                f.write(insight + "\n")
            print(f"📚 Wisdom recorded: {insight}")
        except Exception as e:
            print(f"❌ Failed to write wisdom: {e}")

# Module-level helper for the Bridge
def reflect():
    r = Reflector()
    r.reflect()