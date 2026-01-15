"""
FILE ACCESS MONITOR
Tracks file creation, modification, and access patterns
Learns what you're working on and how your project structure evolves
"""

import os
import subprocess
import datetime
import time
from typing import Dict, List, Set
from pathlib import Path
import json

class FileAccessMonitor:
    """Monitors file system activity to understand your workflow"""
    
    def __init__(self, watch_dirs: List[str] = None):
        self.watch_dirs = watch_dirs or [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Projects"),
            os.path.expanduser("~/My_Life_Work"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Downloads")
        ]
        self.recent_files: List[Dict] = []
        self.file_stats_cache: Dict = {}
    
    def get_recently_modified_files(self, limit: int = 20, minutes: int = 60) -> List[Dict]:
        """Get files modified in the last N minutes"""
        recent = []
        cutoff_time = time.time() - (minutes * 60)
        
        for watch_dir in self.watch_dirs:
            if not os.path.exists(watch_dir):
                continue
            
            try:
                for root, dirs, files in os.walk(watch_dir):
                    # Skip hidden directories and common non-essential folders
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
                    
                    for file in files:
                        if file.startswith('.'):
                            continue
                        
                        filepath = os.path.join(root, file)
                        try:
                            mtime = os.path.getmtime(filepath)
                            
                            if mtime > cutoff_time:
                                file_info = {
                                    "path": filepath,
                                    "name": file,
                                    "extension": os.path.splitext(file)[1],
                                    "modified_time": datetime.datetime.fromtimestamp(mtime).isoformat(),
                                    "size_bytes": os.path.getsize(filepath),
                                    "timestamp": datetime.datetime.now().isoformat()
                                }
                                recent.append(file_info)
                        except (OSError, PermissionError):
                            continue
            except Exception as e:
                print(f"Error scanning {watch_dir}: {e}")
        
        # Sort by modification time, newest first
        recent.sort(key=lambda x: x["modified_time"], reverse=True)
        return recent[:limit]
    
    def get_active_project_folders(self) -> List[Dict]:
        """Identify which project folders have recent activity"""
        projects = {}
        
        for watch_dir in self.watch_dirs:
            if not os.path.exists(watch_dir):
                continue
            
            try:
                # Look for top-level directories with recent modifications
                for item in os.listdir(watch_dir):
                    item_path = os.path.join(watch_dir, item)
                    if os.path.isdir(item_path) and not item.startswith('.'):
                        try:
                            # Get the most recently modified file in this directory
                            for root, dirs, files in os.walk(item_path):
                                dirs[:] = [d for d in dirs if not d.startswith('.')]
                                for file in files:
                                    filepath = os.path.join(root, file)
                                    mtime = os.path.getmtime(filepath)
                                    
                                    if item not in projects or mtime > projects[item]["last_activity"]:
                                        projects[item] = {
                                            "path": item_path,
                                            "last_activity": mtime,
                                            "last_activity_iso": datetime.datetime.fromtimestamp(mtime).isoformat()
                                        }
                        except (OSError, PermissionError):
                            continue
            except Exception as e:
                continue
        
        # Sort by activity
        sorted_projects = sorted(projects.items(), key=lambda x: x[1]["last_activity"], reverse=True)
        return [{"name": name, **info} for name, info in sorted_projects[:10]]
    
    def get_file_type_distribution(self) -> Dict:
        """Understand what types of files you work with"""
        file_types = {}
        
        files = self.get_recently_modified_files(limit=100, minutes=24*60)  # Last 24 hours
        
        for file_info in files:
            ext = file_info["extension"] or "no_extension"
            if ext not in file_types:
                file_types[ext] = {"count": 0, "total_size": 0}
            
            file_types[ext]["count"] += 1
            file_types[ext]["total_size"] += file_info["size_bytes"]
        
        return file_types
    
    def detect_file_operations(self) -> Dict:
        """Detect ongoing file operations"""
        try:
            # Use lsof to see which files are currently open
            result = subprocess.check_output(["lsof", "-c", "python", "-c", "code", "-c", "vim", "-c", "node"], 
                                            stderr=subprocess.DEVNULL).decode("utf-8")
            
            open_files = []
            for line in result.split("\n")[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 9 and "/" in line:
                        open_files.append({
                            "command": parts[0],
                            "file": parts[-1],
                            "timestamp": datetime.datetime.now().isoformat()
                        })
            
            return {
                "open_files": open_files[:20],
                "total_open": len(open_files),
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def observe(self) -> Dict:
        """Get current file system activity snapshot"""
        return {
            "recent_files": self.get_recently_modified_files(),
            "active_projects": self.get_active_project_folders(),
            "file_types": self.get_file_type_distribution(),
            "current_operations": self.detect_file_operations(),
            "timestamp": datetime.datetime.now().isoformat()
        }


if __name__ == "__main__":
    monitor = FileAccessMonitor()
    print("📁 File Access Monitor Started")
    
    data = monitor.observe()
    print(f"\n--- File Activity ---")
    print(f"Recent Files: {len(data['recent_files'])}")
    for f in data['recent_files'][:3]:
        print(f"  - {f['name']} ({f['extension']})")
    
    print(f"\nActive Projects: {len(data['active_projects'])}")
    for p in data['active_projects'][:3]:
        print(f"  - {p['name']}")
