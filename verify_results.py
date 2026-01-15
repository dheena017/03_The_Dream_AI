import json
import os
import subprocess
import time

def verify_results():
    print("="*60)
    print("🧠 VERIFICATION REPORT")
    print("="*60)

    # 1. Check Skill Library
    skill_index_path = "brain/skills/skill_index.json"
    skills_found = []

    if os.path.exists(skill_index_path):
        try:
            with open(skill_index_path, "r") as f:
                index = json.load(f)
            skills = index.get("skills", [])
            print(f"✅ Skills Learned: {len(skills)}")
            skills_found = skills
        except Exception as e:
            print(f"❌ Error reading skill index: {e}")
    else:
        print("❌ Skill index not found.")

    # 2. Functional Verification of Specific Skills
    print("\n🔬 Correctness Check:")

    test_cases = {
        "calculate_50__50": "100",
        "calculate_10__10": "100",
        "write_a_script_to_reverse_the_string_verification": "noitacifirev"
    }

    verified_count = 0

    for skill in skills_found:
        skill_name = skill['name']
        skill_path = os.path.join("brain/skills", f"{skill_name}.py")

        if skill_name in test_cases:
            expected = test_cases[skill_name]
            print(f"  Testing {skill_name} (Expected contains: '{expected}')...")

            try:
                result = subprocess.run(['python3', skill_path], capture_output=True, text=True, timeout=5)
                output = result.stdout.strip()

                if expected in output:
                    print(f"    ✅ PASS: Output was '{output}'")
                    verified_count += 1
                else:
                    print(f"    ❌ FAIL: Output was '{output}'")
            except Exception as e:
                print(f"    ❌ FAIL: Execution error {e}")

    if verified_count == 0 and len(skills_found) > 0:
        print("  ⚠️ No deterministic test cases were found in learned skills yet.")
        print("  Running a random sample skill for manual check:")
        sample = skills_found[-1]
        path = os.path.join("brain/skills", f"{sample['name']}.py")
        print(f"  Running {sample['name']}:")
        try:
            res = subprocess.run(['python3', path], capture_output=True, text=True, timeout=5)
            print(f"    Output: {res.stdout.strip()}")
        except:
            print("    Failed to run.")

    # 3. Check Logs for Self-Correction and Evaluation
    log_path = "brain/bridge_output.log"
    if not os.path.exists(log_path):
        log_path = "brain/brain.log"

    if os.path.exists(log_path):
        print("\n🔍 Log Analysis:")
        with open(log_path, "r") as f:
            logs = f.read()

        # Check for specific keywords
        keywords = {
            "Reflecting on recent performance": "Self-Evaluation (Reflector)",
            "SCHOLAR: Fix identified": "Self-Correction (Scholar)",
            "SURGEON: Code modified successfully": "Self-Correction (Surgeon)",
            "RECOVERY SUCCESSFUL": "Successful Recovery",
            "Self-Improvement Task": "Evolution Engine"
        }

        for phrase, feature in keywords.items():
            count = logs.count(phrase)
            if count > 0:
                print(f"  ✅ {feature} detected: {count} times")
            else:
                print(f"  ⚪ {feature} not detected in this run")

    else:
        print("❌ Log file not found.")

if __name__ == "__main__":
    verify_results()
