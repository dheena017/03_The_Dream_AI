"""
SKILL LIBRARY - Permanent Memory System
Converts generated code into reusable skills that the AI remembers forever
"""

import os
import json
import shutil
from datetime import datetime

class SkillLibrary:
    """Manages permanent skills learned by the AI"""
    
    def __init__(self):
        self.library_path = "brain/skills"
        self.index_path = os.path.join(self.library_path, "skill_index.json")
        self.ensure_structure()
        
    def ensure_structure(self):
        """Create skill library directories"""
        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)
        
        if not os.path.exists(self.index_path):
            with open(self.index_path, 'w') as f:
                json.dump({"skills": [], "version": "1.0"}, f, indent=2)
    
    def add_skill(self, script_path, task_description):
        """Add a generated script to the permanent skill library"""
        if not os.path.exists(script_path):
            return False
        
        # Generate skill name from task
        skill_name = self._generate_skill_name(task_description)
        skill_file = os.path.join(self.library_path, f"{skill_name}.py")
        
        # Check if skill already exists
        if self.skill_exists(skill_name):
            print(f"📚 Skill '{skill_name}' already in library - updating...")
        
        # Copy script to library
        shutil.copy(script_path, skill_file)
        
        # Update index
        self._update_index(skill_name, task_description)
        
        print(f"✅ Skill added to library: {skill_name}")
        return True
    
    def _generate_skill_name(self, task):
        """Generate a clean skill name from task description"""
        # Remove common prefixes
        clean = task.lower()
        for prefix in ["autonomous_task:", "interactive:", "find python code to"]:
            clean = clean.replace(prefix, "")
        
        # Clean up and create name
        clean = clean.strip()
        words = clean.split()[:4]  # First 4 words
        name = "_".join(words)
        
        # Remove special characters
        name = "".join(c if c.isalnum() or c == '_' else '_' for c in name)
        return name
    
    def _update_index(self, skill_name, description):
        """Update the skill index"""
        with open(self.index_path, 'r') as f:
            index = json.load(f)
        
        # Check if skill already exists in index
        existing = next((s for s in index['skills'] if s['name'] == skill_name), None)
        
        if existing:
            # Update existing skill
            existing['last_used'] = datetime.now().isoformat()
            existing['use_count'] += 1
        else:
            # Add new skill
            index['skills'].append({
                'name': skill_name,
                'description': description,
                'created': datetime.now().isoformat(),
                'last_used': datetime.now().isoformat(),
                'use_count': 1
            })
        
        with open(self.index_path, 'w') as f:
            json.dump(index, f, indent=2)
    
    def skill_exists(self, skill_name):
        """Check if a skill exists in the library"""
        skill_file = os.path.join(self.library_path, f"{skill_name}.py")
        return os.path.exists(skill_file)
    
    def find_skill(self, task):
        """Try to find an existing skill that matches the task"""
        skill_name = self._generate_skill_name(task)
        
        if self.skill_exists(skill_name):
            skill_path = os.path.join(self.library_path, f"{skill_name}.py")
            print(f"💡 Found existing skill in library: {skill_name}")
            return skill_path
        
        return None
    
    def get_all_skills(self):
        """Get list of all skills in library"""
        with open(self.index_path, 'r') as f:
            index = json.load(f)
        return index['skills']
    
    def get_stats(self):
        """Get library statistics"""
        skills = self.get_all_skills()
        return {
            'total_skills': len(skills),
            'most_used': max(skills, key=lambda s: s['use_count']) if skills else None,
            'newest': max(skills, key=lambda s: s['created']) if skills else None
        }
