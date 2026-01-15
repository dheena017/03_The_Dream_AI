"""
WORKFLOW ANALYZER
Understands your development workflows and project patterns
"""

import datetime
from typing import Dict, List, Set
from collections import defaultdict, Counter

try:
# AI REFACTORING NEEDED: This function is too complex - see improvements above
# AI REFACTORING NEEDED: This function is too complex - see improvements above
# AI REFACTORING NEEDED: This function is too complex - see improvements above
    from .observation_memory import ObservationMemory
except ImportError:
    from observation_memory import ObservationMemory


class WorkflowAnalyzer:
    """Analyzes your project and development workflows"""
    
    def __init__(self, memory: ObservationMemory):
        """TODO: Add description"""
        self.memory = memory
    
    def detect_active_projects(self, hours: int = 24*7) -> List[Dict]:
        """
        Identify projects you're currently working on
        Based on file activity patterns
        """
        observations = self.memory.get_observations(limit=1000, hours=hours)
        
        projects = defaultdict(lambda: {
            "files": set(),
            "extensions": Counter(),
            "last_activity": None,
            "file_count": 0
        })
        
        for obs in observations:
            files = obs.get("sensors", {}).get("files", {})
            
            for file_info in files.get("recent_files", []):
                path = file_info.get("path", "")
                ext = file_info.get("extension", "")
                
                # Extract project name from path
                # e.g., /home/user/Projects/my_project/file.py -> my_project
                path_parts = path.split("/")
                
                # Find project directory (usually 2-3 levels deep)
                for i, part in enumerate(path_parts):
                    if part in ["Projects", "My_Life_Work", "work", "dev"]:
                        if i + 1 < len(path_parts):
                            project_name = path_parts[i + 1]
                            projects[project_name]["files"].add(path)
                            projects[project_name]["extensions"][ext] += 1
                            projects[project_name]["last_activity"] = file_info.get("modified_time")
                            break
        
        # Convert to list and sort by activity
        project_list = []
        for name, data in projects.items():
            if len(data["files"]) > 0:
                project_list.append({
                    "name": name,
                    "file_count": len(data["files"]),
                    "primary_languages": data["extensions"].most_common(3),
                    "last_activity": data["last_activity"]
                })
        
        return sorted(project_list, key=lambda x: x["last_activity"], reverse=True)
    
    def analyze_coding_workflow(self, hours: int = 24*7) -> Dict:
        """
        Understand your coding workflow
        - How often you edit vs test vs research
        - Tool switching patterns during coding
        """
        observations = self.memory.get_observations(limit=1000, hours=hours)
        
        workflow_stats = {
            "coding_sessions": 0,
            "avg_session_length": 0,
            "typical_workflow": [],
            "tools_used_while_coding": Counter(),
            "research_to_coding_ratio": 0
        }
        
        coding_apps = ["code", "vim", "nano", "python", "node", "editor"]
        research_apps = ["firefox", "chrome", "browser", "documentation"]
        
        current_session = None
        session_tools = []
        
        for obs in observations:
            screen = obs.get("sensors", {}).get("screen", {})
            active_app = screen.get("active_window", {}).get("app_name", "").lower()
            
            is_coding = any(app in active_app for app in coding_apps)
            
            if is_coding:
                if not current_session:
                    current_session = {
                        "start": obs.get("timestamp"),
                        "tools": Counter()
                    }
                
                current_session["tools"][active_app] += 1
                session_tools.append(active_app)
            else:
                if current_session:
                    workflow_stats["coding_sessions"] += 1
                    current_session = None
        
        return workflow_stats
    
    def detect_development_patterns(self) -> Dict:
        """
        Identify your development patterns
        - When do you code most?
        - How long do sessions last?
        - What's your testing frequency?
        """
        timeline = self.memory.get_activity_timeline(hours=24*7)
        
        patterns = {
            "peak_coding_hours": [],
            "average_session_length": 0,
            "test_frequency": 0,
            "commit_frequency": 0
        }
        
        hourly_activity = defaultdict(int)
        
        for entry in timeline:
            app = entry.get("app", "").lower() if entry.get("app") else ""
            
            # Track coding hours
            if any(x in app for x in ["code", "vim", "python", "node", "editor"]):
                try:
                    time_obj = datetime.datetime.fromisoformat(entry["timestamp"])
                    hourly_activity[time_obj.hour] += 1
                except:
                    pass
        
        if hourly_activity:
            patterns["peak_coding_hours"] = sorted(
                hourly_activity.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        
        return patterns
    
    def identify_file_patterns(self, hours: int = 24*7) -> Dict:
        """
        Identify patterns in file modifications
        - Most frequently edited files
        - File types you work with
        - Project structure patterns
        """
        observations = self.memory.get_observations(limit=1000, hours=hours)
        
        patterns = {
            "most_edited_files": Counter(),
            "file_type_distribution": Counter(),
            "directory_hierarchy": defaultdict(int),
            "file_edit_frequency": {}
        }
        
        for obs in observations:
            files = obs.get("sensors", {}).get("files", {})
            
            for file_info in files.get("recent_files", []):
                path = file_info.get("path", "")
                ext = file_info.get("extension", "")
                
                patterns["most_edited_files"][path] += 1
                patterns["file_type_distribution"][ext] += 1
                
                # Extract directory structure
                parts = path.split("/")
                if len(parts) > 3:
                    parent_dir = "/".join(parts[-3:-1])
                    patterns["directory_hierarchy"][parent_dir] += 1
        
        return {
            "top_edited_files": patterns["most_edited_files"].most_common(10),
            "file_types": patterns["file_type_distribution"].most_common(10),
            "common_directories": patterns["directory_hierarchy"]
        }
    
    def predict_next_coding_task(self) -> Dict:
        """
        Predict what you might work on next based on patterns
        """
        projects = self.detect_active_projects()
        active_project = projects[0] if projects else None
        
        if not active_project:
            return {"prediction": "No active projects detected"}
        
        return {
            "likely_next_project": active_project["name"],
            "primary_languages": [lang for lang, _ in active_project.get("primary_languages", [])],
            "last_worked": active_project.get("last_activity"),
            "confidence": 0.7
        }
    
    def get_workflow_report(self) -> Dict:
        """Complete workflow analysis report"""
        return {
            "active_projects": self.detect_active_projects(),
            "coding_workflow": self.analyze_coding_workflow(),
            "development_patterns": self.detect_development_patterns(),
            "file_patterns": self.identify_file_patterns(),
            "next_task_prediction": self.predict_next_coding_task(),
            "timestamp": datetime.datetime.now().isoformat()
        }


if __name__ == "__main__":
    memory = ObservationMemory()
    analyzer = WorkflowAnalyzer(memory)
    
    print("🔧 Workflow Analyzer")
    print("\nActive Projects:")
    projects = analyzer.detect_active_projects()
    for proj in projects[:3]:
        print(f"  - {proj['name']} ({proj['file_count']} files)")
    
    print("\nFile Patterns:")
    patterns = analyzer.identify_file_patterns()
    print(f"  Top File Types: {dict(patterns['file_types'][:3])}")


























# ✅ Reviewed by AI - 2026-01-14T11:58:45.083640Z
# Complexity: 26 | Status: OPTIMAL


# ✅ Reviewed by AI - 2026-01-14T12:01:21.127324Z
# Complexity: 26 | Status: OPTIMAL


# ✅ Reviewed by AI - 2026-01-14T12:01:45.717244Z
# Complexity: 26 | Status: OPTIMAL
