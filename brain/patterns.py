"""
PATTERN RECOGNITION ENGINE
Identifies behavioral patterns, routines, and learnable sequences
"""

import datetime
from typing import Dict, List, Set, Tuple
from collections import Counter, defaultdict

try:
# AI REFACTORING NEEDED: This function is too complex - see improvements above
# AI REFACTORING NEEDED: This function is too complex - see improvements above
    from .observation_memory import ObservationMemory
except ImportError:
    try:
        from observation_memory import ObservationMemory
    except ImportError:
        ObservationMemory = None


class PatternRecognizer:
    """Identifies meaningful patterns in your behavior"""
    
    def __init__(self, memory: ObservationMemory):
        """Function docstring - AI auto-generated"""
        self.memory = memory
    
    def detect_app_sequences(self, min_sequence_length: int = 2) -> List[Dict]:
        """
        Identify common app switching patterns
        Example: "You usually go code → browser → code"
        """
        timeline = self.memory.get_activity_timeline(hours=24*7)  # Last week
        
        sequences = []
        current_sequence = []
        last_app = None
        
        for entry in reversed(timeline):  # Chronological order
            app = entry["app"]
            
            if app != last_app and app:
                current_sequence.append(app)
                if len(current_sequence) > 1 and app == last_app:
                    current_sequence.pop()
                last_app = app
        
        # Find repeating sequences
        sequence_patterns = Counter()
        for i in range(len(current_sequence) - min_sequence_length):
            pattern = tuple(current_sequence[i:i + min_sequence_length])
            sequence_patterns[pattern] += 1
        
        # Return top patterns
        for pattern, count in sequence_patterns.most_common(10):
            if count > 2:  # Only patterns seen 3+ times
                sequences.append({
                    "pattern": " → ".join(pattern),
                    "frequency": count,
                    "confidence": min(1.0, count / 10)
                })
        
        return sequences
    
    def detect_work_sessions(self, idle_threshold: int = 300) -> List[Dict]:
        """
        Identify distinct work sessions based on idle time
        Sessions separated by > 5 minutes of inactivity
        """
        timeline = self.memory.get_activity_timeline(hours=24*7)
        
        sessions = []
        current_session = {
            "start": None,
            "end": None,
            "apps": defaultdict(int),
            "typing_percentage": 0
        }
        
        typing_count = 0
        total_count = 0
        
        for i, entry in enumerate(reversed(timeline)):
            idle_seconds = entry.get("idle", "0")
            try:
                idle = float(idle_seconds) if idle_seconds else 0
            except:
                idle = 0
            
            # Start new session if idle > threshold
            if idle > idle_threshold:
                if current_session["start"]:
                    current_session["end"] = entry["timestamp"]
                    if total_count > 0:
                        current_session["typing_percentage"] = (typing_count / total_count) * 100
                    sessions.append(current_session)
                
                current_session = {
                    "start": None,
                    "end": None,
                    "apps": defaultdict(int),
                    "typing_percentage": 0
                }
                typing_count = 0
                total_count = 0
            else:
                if not current_session["start"]:
                    current_session["start"] = entry["timestamp"]
                
                # Track app usage in session
                if entry["app"]:
                    current_session["apps"][entry["app"]] += 1
                
                # Track typing
                if entry["typing"] == "active":
                    typing_count += 1
                total_count += 1
        
        return sessions[:20]  # Top 20 sessions
    
    def identify_learning_patterns(self) -> Dict:
        """
        Identify how you learn
        - Search patterns before coding
        - Documentation visits
        - Tutorial consumption
        """
        app_usage = self.memory.get_app_usage(hours=24*7)
        
        patterns = {
            "coding_to_research_ratio": None,
            "browser_research_patterns": [],
            "learning_workflow": None
        }
        
        # Simple heuristic: identify learning workflows
        coding_apps = ["code", "vim", "python", "node", "terminal", "bash"]
        research_apps = ["firefox", "chrome", "chromium", "brave"]
        
        coding_time = sum(v["observation_count"] for k, v in app_usage.items() 
                         if any(c in k.lower() for c in coding_apps))
        research_time = sum(v["observation_count"] for k, v in app_usage.items() 
                           if any(r in k.lower() for r in research_apps))
        
        if coding_time + research_time > 0:
            ratio = coding_time / (coding_time + research_time)
            patterns["coding_to_research_ratio"] = ratio
        
        return patterns
    
    def predict_next_action(self) -> Dict:
        """
        Simple prediction: what will you do next?
        Based on current app and time of day
        """
        timeline = self.memory.get_activity_timeline(hours=24*2)
        
        if not timeline:
            return {"prediction": "No data available", "confidence": 0}
        
        current_app = timeline[0]["app"] if timeline else None
        current_hour = datetime.datetime.now().hour
        
        # Simple pattern matching
        next_apps_after_current = Counter()
        
        for i in range(len(timeline) - 1):
            if timeline[i]["app"] == current_app:
                next_app = timeline[i+1]["app"]
                if next_app and next_app != current_app:
                    next_apps_after_current[next_app] += 1
        
        if next_apps_after_current:
            predicted_app, frequency = next_apps_after_current.most_common(1)[0]
            return {
                "current_app": current_app,
                "predicted_next": predicted_app,
                "confidence": min(1.0, frequency / 5),
                "based_on": f"{frequency} observations"
            }
        
        return {"prediction": "Insufficient pattern data", "confidence": 0}
    
    def get_daily_rhythm(self) -> Dict:
        """
        Understand your daily patterns
        - Most productive hours
        - Break patterns
        - Focus duration
        """
        timeline = self.memory.get_activity_timeline(hours=24*7)
        
        hourly_activity = defaultdict(lambda: {"active": 0, "idle": 0, "typing": 0})
        
        for entry in timeline:
            try:
                time_obj = datetime.datetime.fromisoformat(entry["timestamp"])
                hour = time_obj.hour
                
                if entry["idle"] == "active":
                    hourly_activity[hour]["active"] += 1
                elif entry["idle"] == "idle":
                    hourly_activity[hour]["idle"] += 1
                
                if entry["typing"] == "active":
                    hourly_activity[hour]["typing"] += 1
            except:
                pass
        
        return {
            f"hour_{hour:02d}": activity 
            for hour, activity in sorted(hourly_activity.items())
        }
    
    def analyze_all_patterns(self) -> Dict:
        """Comprehensive pattern analysis"""
        return {
            "app_sequences": self.detect_app_sequences(),
            "work_sessions": self.detect_work_sessions(),
            "learning_patterns": self.identify_learning_patterns(),
            "next_action_prediction": self.predict_next_action(),
            "daily_rhythm": self.get_daily_rhythm(),
            "timestamp": datetime.datetime.now().isoformat()
        }


if __name__ == "__main__":
    memory = ObservationMemory()
    recognizer = PatternRecognizer(memory)
    
    print("🧠 Pattern Recognition Engine")
    print("\nAnalyzing patterns...")
    
    patterns = recognizer.analyze_all_patterns()
    
    print(f"\nTop App Sequences:")
    for seq in patterns["app_sequences"][:3]:
        print(f"  {seq['pattern']} (seen {seq['frequency']} times)")
    
    print(f"\nNext Action Prediction:")
    pred = patterns["next_action_prediction"]
    print(f"  You might: {pred.get('predicted_next', 'Unknown')}")
    print(f"  Confidence: {pred.get('confidence', 0):.1%}")


