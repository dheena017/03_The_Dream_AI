import os
import glob
from pathlib import Path

GEN_DIR = Path("brain/generated")
BACKUP_DIR = Path("backups")

def perform_lobotomy():
    print("🧠 STARTING BRAIN SURGERY...")

    # 1. Clean up the generated task scripts
    print(f"   🧹 Sweeping {GEN_DIR}...")
    files = list(GEN_DIR.glob("*.py"))
    
    # Delete ALL old scripts to prevent accumulation
    for f in files:
        try:
            os.remove(f)
            print(f"      ❌ Removed: {f.name}")
        except Exception as e:
            print(f"      ⚠️ Failed to remove {f.name}: {e}")

    # 2. Clean up Backups - Keep only the 2 most recent
    print(f"   🗑️  Cleaning Backups in {BACKUP_DIR}...")
    if BACKUP_DIR.exists():
        backups = sorted(
            [d for d in BACKUP_DIR.iterdir() if d.is_dir()],
            key=lambda d: d.stat().st_mtime,
            reverse=True  # Most recent first
        )
        
        # Keep only the newest 2 backups
        to_delete = backups[2:]
        
        for b in to_delete:
            try:
                import shutil
                shutil.rmtree(b)
                print(f"      ❌ Deleted backup: {b.name}")
            except Exception as e:
                print(f"      ⚠️ Failed to delete {b.name}: {e}")
        
        print(f"      ✅ Kept {min(2, len(backups))} most recent backups")

    print("✨ Surgery Complete. Brain reset to stable state.")

if __name__ == "__main__":
    perform_lobotomy()