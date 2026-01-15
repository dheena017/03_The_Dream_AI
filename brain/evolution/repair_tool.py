import os
import subprocess
import shutil

def verify_and_evolve(new_code_file, target_script):
    print(f"🧬 EVOLUTION: Testing patch {new_code_file}...")
    
    # 1. Syntax Check
    check = subprocess.run(['python3', '-m', 'py_compile', new_code_file], capture_output=True)
    
    if check.returncode == 0:
        print("✅ Syntax Validated. Backing up system...")
        shutil.copy(target_script, target_script + ".bak")
        
        # 2. The 'Human' Swap
        # In a real evolution, we'd merge logic. 
        # Here we prepare the bridge to accept the new timeout logic.
        print(f"🚀 Phase 3: System {target_script} is ready for evolution.")
        return True
    else:
        print("❌ Evolution Rejected: New code would crash the brain.")
        return False

if __name__ == "__main__":
    # Test with the AI's latest dream
    verify_and_evolve("brain/generated/task_445509_939.py", "brain/bridge_no_flask.py")
