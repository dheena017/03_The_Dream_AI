import json
import os
from datetime import datetime

class Learner:
    def digest_code(self, filename, task_desc):
        # Check if skills.json exists, create it if not
        if not os.path.exists('brain/memory/skills.json'):
            with open('brain/memory/skills.json', 'w') as f:
                json.dump([], f)
        
        # Read existing skills from skills.json
        with open('brain/memory/skills.json', 'r') as f:
            skills = json.load(f)
        
        # Append new skill to skills list
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        skill_entry = {
            'timestamp': timestamp,
            'filename': filename,
            'task_desc': task_desc
        }
        skills.append(skill_entry)
        
        # Save updated skills list back to skills.json
        with open('brain/memory/skills.json', 'w') as f:
            json.dump(skills, f)
        
        print("🧠 LEARNER: Skill indexed.")