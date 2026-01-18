"""
BRIDGE - THE NEURAL CONNECTION (UPGRADED)
Connects Eyes (observation) to Brain (learning)
Now using SmartDeveloper for intelligent task processing
WITH SELF-EVOLUTION CAPABILITY
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from brain.brain import BrainOrchestrator
from brain.evolution.smart_developer import SmartDeveloper
from brain.evolution.self_evolution import SelfEvolutionEngine
from brain.observation_memory import ObservationMemory
from brain.skill_library import SkillLibrary
from brain.scholar import Scholar
from brain.surgeon import Surgeon
from datetime import datetime

# Import modules
from brain.evolution import innovator
from brain.memory import learner
from brain.evolution import reflector
from brain.runner import Runner

from typing import Dict
import threading
import time


# Simple log writer for live dashboard
class BrainLogger:
    """Writes output to both console and log file for dashboard viewing"""
    
    def __init__(self):
        self.log_file = "brain/brain.log"
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Ensure log file exists"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            open(self.log_file, 'w').close()
    
    def log(self, message: str):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        output = f"[{timestamp}] {message}"
        
        # Print to console
        print(output)
        
        # Write to log file
        try:
            with open(self.log_file, 'a') as f:
                f.write(output + '\n')
        except:
            pass


class Bridge:
    """Neural bridge between Eyes and Brain"""
    
    def __init__(self):
        self.logger = BrainLogger()
        self.logger.log("🧠 DREAM AI - BRAIN SYSTEM INITIALIZED")
        self.brain = BrainOrchestrator()
        self.memory = ObservationMemory()
        
        # 🎯 PRIME DIRECTIVE: Set AI's purpose/focus
        # Options: "sysadmin", "python_learner", "researcher"
        AI_MODE = "researcher"  # ← CHANGE THIS TO SWITCH MODES
        
        # Initialize Innovator instance with mode
        self.innovator = innovator.Innovator(mode=AI_MODE)
        self.logger.log("💡 Innovator: ENABLED")
        
        # Initialize Skill Library
        self.skill_library = SkillLibrary()
        self.logger.log(f"📚 Skill Library: {len(self.skill_library.get_all_skills())} skills loaded")
        
        self.developer = SmartDeveloper()
        self.evolution_engine = SelfEvolutionEngine()  # 👈 NEW: Self-evolution
        self.scholar = Scholar()
        self.surgeon = Surgeon()
        
        # Initialize runner
        self.runner = Runner()
            
        self.observation_count = 0
        self.learning_updates = 0
        self.autonomous_active = False
        
        self.logger.log("   📦 Memory Backend: SQLite")
        self.logger.log("   🔍 Pattern Recognition: Online")
        self.logger.log("   📊 Activity Analysis: Online")
        self.logger.log("   🔧 Workflow Analysis: Online")
        self.logger.log("   🗺️  Knowledge Mapping: Online")
        self.logger.log("   🧬 Self-Evolution: ENABLED")
        self.logger.log("")
        self.logger.log("🧠 DREAM AI - BRIDGE SYSTEM STARTED")
        self.logger.log("   Eyes → Brain Neural Connection Active")
        self.logger.log("   Self-Evolution Engine Ready")
    
    def process_observation(self, observation: Dict):
        """
        Receive observation from Eyes
        Pass to Brain for learning
        """
        try:
            # Brain processes and learns from observation
            self.brain.process_observation(observation)
            
            # Store in memory
            self.memory.store_observation(observation)
            
            self.observation_count += 1
            
            # Learn patterns every 10 observations
            if self.observation_count % 10 == 0:
                insights = self.brain.analyze_patterns()
                self.learning_updates += 1
                
        except Exception as e:
            print(f"❌ Bridge Error: {e}")
            import traceback
            traceback.print_exc()
    
    def process_task(self, task: str):
        """Process a command/task - routes to self-evolution or standard processing"""
        output = []
        output.append(f"📩 NEW TASK RECEIVED: {task}")
        output.append("🧠 BRAIN ACTIVATED. Thinking...")
        for line in output:
            self.logger.log(line)
        
        # CHECK 0: Do we already know how to do this? (Skill Library)
        existing_skill = self.skill_library.find_skill(task)
        if existing_skill:
            output.append(f"💡 Using learned skill from library!")
            print("\n".join(output))
            
            # Execute the skill directly
            if self.runner:
                try:
                    output.append(f"🏃 Running: {existing_skill}")
                    execution_result = self.runner.run_code(existing_skill)
                    output.append("📤 OUTPUT:")
                    output.append(execution_result)
                    
                    # Reflect on performance
                    try:
                        output.append("🧐 Reflecting on recent performance...")
                        ref = reflector.Reflector()
                        ref.reflect()
                    except Exception as e:
                        output.append(f"⚠️  Reflection skipped: {e}")
                    
                    result_msg = "\n".join(output)
                    print(result_msg)
                    return {"status": "success", "output": result_msg, "script": existing_skill, "execution": execution_result}
                except Exception as e:
                    output.append(f"⚠️  Skill execution failed: {e}")
        
        # CHECK 1: Is this a self-improvement task?
        if self.evolution_engine.analyzer.is_self_improvement_task(task):
            output.append("🧬 DETECTED: Self-Improvement Task!")
            output.append("🔬 Routing to Self-Evolution Engine...")
            print("\n".join(output))
            
            # Process with self-evolution
            evolution_result = self.process_self_improvement_task(task)
            
            return {
                "status": "success",
                "type": "self_improvement",
                "output": evolution_result,
                "script": None,
                "execution": None
            }
        
        # CHECK 2: If not self-improvement, process normally
        try:
            # 1. Generate Code using Smart Developer
            script_path = self.developer.generate_solution(task)
            output.append(f"📝 Generated: {script_path}")
            
            if script_path:
                # 2. Check if file was created
                if os.path.exists(script_path):
                    output.append(f"✅ JOB DONE. File created: {script_path}")
                    
                    # 3. Execute if runner is available and enabled
                    execution_result = None
                    runner_enabled_path = os.path.join(os.path.dirname(__file__), "RUNNER_ENABLED")
                    if self.runner and os.path.exists(runner_enabled_path):
                        output.append("🏃 RUNNER: Executing task...")
                        execution_result = self.runner.execute_task(script_path)

                        # === SELF-CORRECTION LOOP ===
                        if execution_result and ("❌" in execution_result or "Traceback" in execution_result):
                            output.append("\n💥 CRASH DETECTED - ACTIVATING IMMUNE SYSTEM")
                            output.append("   Switching to 'Scholar' mode for research...")

                            # 1. Scholar researches the error
                            fix_plan = self.scholar.research_error(execution_result, script_path)
                            output.append(f"🎓 SCHOLAR: Fix identified -> {fix_plan.get('type')}")

                            # 2. Surgeon applies the fix
                            if fix_plan.get('action') != 'log_only':
                                success = self.surgeon.apply_fix(script_path, fix_plan)
                                if success:
                                    output.append("🩺 SURGEON: Code modified successfully.")

                                    # 3. Retry execution
                                    output.append("🏃 RUNNER: Retrying fixed code...")
                                    execution_result = self.runner.execute_task(script_path)
                                    if "❌" not in execution_result and "Traceback" not in execution_result:
                                        output.append("✅ RECOVERY SUCCESSFUL!")
                                    else:
                                        output.append("⚠️  Recovery failed on retry.")
                                else:
                                    output.append("❌ Surgeon could not apply fix.")
                        # ============================

                        if execution_result:
                            output.append(f"📤 OUTPUT:\n{execution_result}")
                    else:
                        if not os.path.exists(runner_enabled_path):
                            output.append(f"⚠️  Runner Disabled (create {runner_enabled_path} to enable).")
                        else:
                            output.append("⚠️  Runner not available.")
                    
                    # 4. Reflect on performance
                    try:
                        output.append("🧐 Reflecting on recent performance...")
                        ref = reflector.Reflector()
                        ref.reflect()
                    except Exception as e:
                        output.append(f"⚠️  Reflection skipped: {e}")
                    
                    # 5. Save successful tasks to Skill Library
                    if execution_result and "❌" not in execution_result:
                        self.skill_library.add_skill(script_path, task)
                    
                    result_msg = "\n".join(output)
                    print(result_msg)
                    return {"status": "success", "output": result_msg, "script": script_path, "execution": execution_result}
                else:
                    output.append(f"❌ Error: Script file not created")
                    error_msg = "\n".join(output)
                    print(error_msg)
                    return {"status": "error", "output": error_msg}
            else:
                output.append("❌ Error: No script path returned")
                error_msg = "\n".join(output)
                print(error_msg)
                return {"status": "error", "output": error_msg}
                
        except Exception as e:
            output.append(f"❌ Task Processing Error: {e}")
            import traceback
            tb = traceback.format_exc()
            output.append(tb)
            error_msg = "\n".join(output)
            print(error_msg)
            return {"status": "error", "output": error_msg, "error": str(e)}
    
    def process_self_improvement_task(self, task: str):
        """Process a self-improvement task using evolution engine"""
        try:
            print("\n" + "="*60)
            print("🧬 SELF-IMPROVEMENT ENGINE ACTIVATED")
            print("="*60)
            
            # Route to evolution engine
            evolution_result = self.evolution_engine.process_self_improvement_task(task)
            
            # Create a report summarizing what will happen
            report = {
                'task': task,
                'analysis': evolution_result['requirements'],
                'research_plan': evolution_result['research_plan'],
                'learning_plan': evolution_result['learning_plan'],
                'implementation': evolution_result['implementation'],
                'summary_document': evolution_result['summary_document']
            }
            
            print("="*60)
            print("✅ Self-Improvement Task Queued for Execution")
            print("="*60 + "\n")
            
            return report
            
        except Exception as e:
            print(f"❌ Self-Improvement Error: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "error": str(e)}
    
    def autonomous_loop(self):
        """Autonomous mode - processes tasks from inbox"""
        print("🤖 AUTONOMOUS MODE: ENABLED")
        print("🤖 AUTONOMOUS MODE ENGAGED - Digital Employee Online")
        print("📬 Task Inbox: brain/tasks.txt")
        
        print("🧠 INNOVATOR MODULE: CONNECTED")
        
        while self.autonomous_active:
            try:
                # Check for tasks file
                if os.path.exists("brain/tasks.txt"):
                    with open("brain/tasks.txt", "r") as f:
                        tasks = f.readlines()
                    
                    if tasks:
                        current_task = tasks[0].strip()
                        if current_task:
                            self.process_task(current_task)
                            
                            # Remove completed task
                            remaining = tasks[1:]
                            with open("brain/tasks.txt", "w") as f:
                                f.writelines(remaining)
                    else:
                        print("💤 Inbox empty. Dreaming of improvements...")
                        
                        # Let innovator suggest tasks
                        print("💤 INNOVATOR: Reading Wisdom...")
                        self.innovator.run_autonomy()
                else:
                    # Create empty tasks file
                    with open("brain/tasks.txt", "w") as f:
                        f.write("")
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                print(f"❌ Autonomous Loop Error: {e}")
                time.sleep(10)
    
    def get_status(self) -> Dict:
        """Get current system status"""
        return {
            "observations_processed": self.observation_count,
            "learning_updates": self.learning_updates,
            "memory_stats": self.memory.get_memory_stats(),
            "autonomous_mode": self.autonomous_active
        }


# Global bridge instance
bridge = Bridge()


# Flask integration (if available)
try:
    from flask import Flask, request, jsonify
    
    # Use absolute path for templates
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app = Flask(__name__, template_folder=template_dir)
    
    @app.route('/brain-log', methods=['POST'])
    def brain_log():
        """Receive observation from Eyes"""
        observation = request.json
        bridge.process_observation(observation)
        return jsonify({"status": "received"})
    
    @app.route('/command', methods=['POST'])
    def command():
        """Receive command/task"""
        data = request.json
        task = data.get('task')
        result = bridge.process_task(task)
        return jsonify({"status": result})
    
    @app.route('/status', methods=['GET'])
    def status():
        """Get system status"""
        return jsonify(bridge.get_status())
    
    def run_flask():
        """Run Flask server"""
        print("   📡 Listening on http://localhost:3000")
        print("   🧬 Phase 3: Self-Evolving Mode ACTIVE")
        app.run(host='localhost', port=3000, debug=False)
    
except ImportError:
    print("⚠️  Flask not installed. Install with: pip install flask")
    app = None
    
    def run_flask():
        print("❌ Flask not available - running in offline mode")
        while True:
            time.sleep(60)


if __name__ == '__main__':
    # Start Autonomous Thread if enabled
    if os.path.exists("brain/AUTONOMOUS_ENABLED"):
        bridge.autonomous_active = True
        autonomous_thread = threading.Thread(target=bridge.autonomous_loop, daemon=True)
        autonomous_thread.start()
    
    # Start Flask server (or idle loop)
    if app:
        run_flask()
    else:
        print("Running in background mode...")
        while True:
            time.sleep(60)
