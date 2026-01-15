"""
MISSION CONTROL DASHBOARD
Live visualization of AI's thoughts, actions, and learning
"""

from flask import Flask, render_template, jsonify, request
import os
import json
from datetime import datetime
import sqlite3

app = Flask(__name__)

class DashboardData:
    """Collects data from the AI system"""
    
    def __init__(self):
        self.db_path = "brain/memory/observations.db"
        
    def get_recent_tasks(self, limit=10):
        """Get recent completed tasks"""
        completed_dir = "brain/memory/completed"
        if not os.path.exists(completed_dir):
            return []
        
        files = []
        for f in os.listdir(completed_dir):
            if f.startswith("task_smart_"):
                path = os.path.join(completed_dir, f)
                files.append({
                    'name': f,
                    'time': datetime.fromtimestamp(os.path.getctime(path)).strftime("%H:%M:%S"),
                    'size': os.path.getsize(path)
                })
        
        return sorted(files, key=lambda x: x['time'], reverse=True)[:limit]
    
    def get_wisdom_log(self, limit=10):
        """Get recent wisdom entries"""
        wisdom_path = "brain/wisdom.txt"
        if not os.path.exists(wisdom_path):
            return []
        
        with open(wisdom_path, 'r') as f:
            lines = f.readlines()
        
        return [line.strip() for line in lines[-limit:]][::-1]
    
    def get_current_mode(self):
        """Read current AI mode from bridge.py"""
        try:
            with open("brain/bridge.py", 'r') as f:
                for line in f:
                    if 'AI_MODE =' in line:
                        mode = line.split('=')[1].strip().strip('"').strip("'")
                        return mode
        except:
            return "unknown"
        return "sysadmin"
    
    def get_task_queue(self):
        """Get pending tasks"""
        tasks_path = "brain/tasks.txt"
        if not os.path.exists(tasks_path):
            return []
        
        with open(tasks_path, 'r') as f:
            tasks = [line.strip() for line in f.readlines() if line.strip()]
        
        return tasks
    
    def get_system_stats(self):
        """Get system statistics"""
        stats = {
            'completed_tasks': len(os.listdir("brain/memory/completed")) if os.path.exists("brain/memory/completed") else 0,
            'generated_scripts': len(os.listdir("brain/generated")) if os.path.exists("brain/generated") else 0,
            'memory_size': 0,
            'observations': 0
        }
        
        # Count observations from DB
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM observations")
            stats['observations'] = cursor.fetchone()[0]
            conn.close()
        except:
            pass
        
        # Get memory size
        if os.path.exists(self.db_path):
            stats['memory_size'] = os.path.getsize(self.db_path) / (1024 * 1024)  # MB
        
        return stats
    
    def get_live_log(self, lines=20):
        """Get live brain activity log"""
        log_path = "brain/brain.log"
        if not os.path.exists(log_path):
            return ["No log yet"]
        
        try:
            with open(log_path, 'r') as f:
                all_lines = f.readlines()
            
            # Get last N lines
            recent = all_lines[-lines:]
            return [line.rstrip() for line in recent]
        except:
            return ["Could not read log"]

data_collector = DashboardData()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """Get current AI status"""
    return jsonify({
        'mode': data_collector.get_current_mode(),
        'stats': data_collector.get_system_stats(),
        'recent_tasks': data_collector.get_recent_tasks(5),
        'wisdom': data_collector.get_wisdom_log(5),
        'queue': data_collector.get_task_queue(),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/live-log')
def api_live_log():
    """Get live brain activity"""
    lines = request.args.get('lines', 20, type=int)
    return jsonify({
        'log': data_collector.get_live_log(lines),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/switch_mode', methods=['POST'])
def api_switch_mode():
    """Hot-swap AI mode without restart"""
    new_mode = request.json.get('mode', 'sysadmin')
    
    # Update bridge.py
    try:
        with open("brain/bridge.py", 'r') as f:
            content = f.read()
        
        # Find and replace AI_MODE line
        import re
        pattern = r'AI_MODE = ["\'].*?["\']'
        replacement = f'AI_MODE = "{new_mode}"'
        content = re.sub(pattern, replacement, content)
        
        with open("brain/bridge.py", 'w') as f:
            f.write(content)
        
        return jsonify({'status': 'success', 'mode': new_mode, 'message': 'Mode updated. Restart required.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/command', methods=['POST'])
def api_command():
    """Send interactive command to AI"""
    command = request.json.get('command', '')
    
    if not command:
        return jsonify({'status': 'error', 'message': 'No command provided'})
    
    # Write to tasks.txt
    try:
        with open("brain/tasks.txt", 'a') as f:
            f.write(f"INTERACTIVE: {command}\n")
        
        return jsonify({'status': 'success', 'message': f'Command queued: {command}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    print("🖥️  MISSION CONTROL DASHBOARD")
    print("=" * 60)
    print("📡 Dashboard: http://localhost:5000")
    print("🎯 Monitoring AI brain activity...")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=False)
