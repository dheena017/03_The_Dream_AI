#!/usr/bin/env python3
"""
DREAM AI - MASTER LAUNCHER
Starts all components of the AI system simultaneously
"""

import subprocess
import time
import sys
import os
import signal

class AILauncher:
    def __init__(self):
        self.processes = []
        
    def start_component(self, name, command):
        """Start a component as a subprocess"""
        print(f"🚀 Starting {name}...")
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            self.processes.append({'name': name, 'process': process})
            print(f"✅ {name} started (PID: {process.pid})")
            return process
        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
            return None
    
    def stop_all(self):
        """Stop all components"""
        print("\n🛑 Shutting down all components...")
        for comp in self.processes:
            try:
                comp['process'].terminate()
                comp['process'].wait(timeout=5)
                print(f"✅ {comp['name']} stopped")
            except:
                comp['process'].kill()
                print(f"⚠️  {comp['name']} force killed")
    
    def run(self):
        """Main launcher loop"""
        print("=" * 60)
        print("🧠 DREAM AI - AUTONOMOUS SYSTEM LAUNCHER")
        print("=" * 60)
        print()
        
        # Check if ports are available
        import socket
        for port, name in [(3000, "Brain"), (5000, "Dashboard")]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            if result == 0:
                print(f"⚠️  Port {port} ({name}) is already in use!")
                print(f"   Kill existing process: lsof -ti:{port} | xargs kill -9")
                print()
                sock.close()
                sys.exit(1)
            sock.close()
        
        # Start components in order
        self.start_component("Brain (Bridge)", "python3 brain/bridge.py")
        time.sleep(2)  # Let brain initialize
        
        self.start_component("Dashboard", "python3 dashboard.py")
        time.sleep(1)
        
        print()
        print("=" * 60)
        print("✅ ALL SYSTEMS ONLINE")
        print("=" * 60)
        print()
        print("📡 Brain API:     http://localhost:3000")
        print("🖥️  Dashboard:     http://localhost:5000")
        print()
        print("🎯 AI Mode: Check dashboard for current mode")
        print("💡 Control: Use dashboard to switch modes or send commands")
        print()
        print("Press Ctrl+C to stop all components...")
        print("=" * 60)
        print()
        
        try:
            # Monitor components
            while True:
                time.sleep(1)
                
                # Check if any process died
                for comp in self.processes:
                    if comp['process'].poll() is not None:
                        print(f"⚠️  {comp['name']} stopped unexpectedly!")
                        
        except KeyboardInterrupt:
            print("\n\n🛑 Shutdown signal received...")
            self.stop_all()
            print("\n✅ All components stopped. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    launcher = AILauncher()
    launcher.run()
