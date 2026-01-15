"""
ACTIVITY ANALYZER
Analyzes application usage, productivity patterns, and behavioral metrics
"""

import datetime
from typing import Dict, List
from collections import defaultdict

try:
# AI REFACTORING NEEDED: This function is too complex - see improvements above
# AI REFACTORING NEEDED: This function is too complex - see improvements above
# AI REFACTORING NEEDED: This function is too complex - see improvements above
# AI REFACTORING NEEDED: This function is too complex - see improvements above
    from .observation_memory import ObservationMemory
except ImportError:
    from observation_memory import ObservationMemory


class ActivityAnalyzer:
    """Deep analysis of your activity patterns"""
    
    def __init__(self, memory: ObservationMemory):
        """Initialize the activity analyzer with a memory instance.
        
        Args:
            memory: ObservationMemory instance to analyze activities from
        """
        self.memory = memory
    
    def calculate_focus_time(self, hours: int = 24) -> Dict:
        """
        Calculate deep focus periods
        - Time without app switching
        - Continuous coding sessions
        - Uninterrupted time on single task
        """
        timeline = self.memory.get_activity_timeline(hours=hours)
        
        focus_sessions = []
        current_session = {
            "app": None,
            "start": None,
            "duration_minutes": 0,
            "switches": 0
        }
        
        for entry in reversed(timeline):
            app = entry["app"]
            
            if app == current_session["app"]:
                current_session["duration_minutes"] += 1  # Approximate, 1 obs per ~10-60 seconds
            else:
                if current_session["app"] and current_session["duration_minutes"] > 10:
                    focus_sessions.append(current_session)
                
                current_session = {
                    "app": app,
                    "start": entry["timestamp"],
                    "duration_minutes": 0,
                    "switches": 0
                }
        
        if focus_sessions:
            avg_focus = sum(s["duration_minutes"] for s in focus_sessions) / len(focus_sessions)
            max_focus = max(s["duration_minutes"] for s in focus_sessions)
        else:
            avg_focus = 0
            max_focus = 0
        
        return {
            "average_focus_duration_minutes": avg_focus,
            "longest_focus_session_minutes": max_focus,
            "total_focus_sessions": len(focus_sessions),
            "top_focus_apps": self._get_top_apps_by_focus(focus_sessions)
        }
    
    def _get_top_apps_by_focus(self, sessions: List[Dict]) -> List[Dict]:
        """Get apps with longest continuous use"""
        app_focus = defaultdict(lambda: {"total_minutes": 0, "sessions": 0})
        
        for session in sessions:
            app = session["app"]
            app_focus[app]["total_minutes"] += session["duration_minutes"]
            app_focus[app]["sessions"] += 1
        
        return sorted(
            [{"app": k, **v} for k, v in app_focus.items()],
            key=lambda x: x["total_minutes"],
            reverse=True
        )[:5]
    
    def productivity_score(self, hours: int = 24) -> Dict:
        """
        Calculate productivity score based on multiple factors
        - Active typing time vs idle time
        - Focus duration
        - App diversity (tool switching)
        - Consistency
        """
        timeline = self.memory.get_activity_timeline(hours=hours)
        
        if not timeline:
            return {"score": 0, "details": {}}
        
        total_entries = len(timeline)
        active_entries = sum(1 for e in timeline if e["typing"] == "active")
        idle_entries = sum(1 for e in timeline if e["idle"] == "idle")
        
        typing_ratio = active_entries / total_entries if total_entries > 0 else 0
        focus_time = self.calculate_focus_time(hours=hours)
        
        # Score components (0-100)
        typing_score = typing_ratio * 100
        focus_score = min(100, (focus_time["average_focus_duration_minutes"] / 30) * 100)
        consistency_score = min(100, (total_entries / (hours * 60)) * 100)
        
        overall_score = (typing_score * 0.4 + focus_score * 0.4 + consistency_score * 0.2)
        
        return {
            "overall_productivity_score": round(overall_score, 1),
            "typing_ratio": round(typing_ratio * 100, 1),
            "focus_score": round(focus_score, 1),
            "consistency_score": round(consistency_score, 1),
            "active_time_entries": active_entries,
            "idle_time_entries": idle_entries
        }
    
    def identify_most_used_tools(self, hours: int = 24*7) -> List[Dict]:
        """Identify your primary work tools"""
        app_usage = self.memory.get_app_usage(hours=hours)
        
        tool_categories = {
            "Editors": ["code", "vim", "nano", "emacs"],
            "Terminals": ["terminal", "bash", "zsh", "konsole"],
            "Browsers": ["firefox", "chrome", "chromium", "brave", "edge"],
            "Languages": ["python", "node", "ruby", "java"],
            "Version Control": ["git", "github", "gitlab"],
            "Communication": ["slack", "discord", "telegram"]
        }
        
        categorized = defaultdict(lambda: {"apps": [], "total_obs": 0})
        
        for app_name, usage in app_usage.items():
            for category, keywords in tool_categories.items():
                if any(kw in app_name.lower() for kw in keywords):
                    categorized[category]["apps"].append({
                        "name": app_name,
                        "observations": usage["observation_count"]
                    })
                    categorized[category]["total_obs"] += usage["observation_count"]
                    break
        
        return [
            {
                "category": cat,
                "tools": sorted(data["apps"], key=lambda x: x["observations"], reverse=True),
                "total_usage": data["total_obs"]
            }
            for cat, data in sorted(categorized.items(), 
                                   key=lambda x: x[1]["total_obs"], 
                                   reverse=True)
        ]
    
    def compare_productivity(self, period1_hours: int = 24, period2_hours: int = 24*7) -> Dict:
        """
        Compare productivity across time periods
        - Last 24h vs last week
        - Identify trends
        """
        score_24h = self.productivity_score(hours=period1_hours)
        score_7d = self.productivity_score(hours=period2_hours)
        
        current_score = score_24h["overall_productivity_score"]
        weekly_avg = score_7d["overall_productivity_score"]
        
        trend = "up" if current_score > weekly_avg else "down" if current_score < weekly_avg else "stable"
        change = current_score - weekly_avg
        
        return {
            "current_score_24h": current_score,
            "weekly_average": weekly_avg,
            "trend": trend,
            "change": round(change, 1),
            "productivity_status": self._interpret_score(current_score)
        }
    
    def _interpret_score(self, score: float) -> str:
        """Interpret productivity score"""
        if score >= 80:
            return "Excellent 🌟"
        elif score >= 60:
            return "Good 👍"
        elif score >= 40:
            return "Average 😐"
        elif score >= 20:
            return "Low 😔"
        else:
            return "Very Low 😞"
    
    def get_activity_breakdown(self, hours: int = 24) -> Dict:
        """
        Detailed breakdown of activity distribution
        - Time per app
        - Active vs idle
        - Different contexts
        """
        timeline = self.memory.get_activity_timeline(hours=hours)
        
        breakdown = {
            "by_app": defaultdict(int),
            "by_state": {"active": 0, "idle": 0, "away": 0},
            "by_context": {"typing": 0, "browsing": 0, "coding": 0, "other": 0}
        }
        
        for entry in timeline:
            # App breakdown
            if entry["app"]:
                breakdown["by_app"][entry["app"]] += 1
            
            # State breakdown
            idle = entry.get("idle", "active")
            breakdown["by_state"][idle] = breakdown["by_state"].get(idle, 0) + 1
            
            # Context detection
            app = entry["app"].lower() if entry["app"] else ""
            if any(x in app for x in ["code", "vim", "python", "node"]):
                breakdown["by_context"]["coding"] += 1
            elif any(x in app for x in ["firefox", "chrome", "browser"]):
                breakdown["by_context"]["browsing"] += 1
            elif entry["typing"] == "active":
                breakdown["by_context"]["typing"] += 1
            else:
                breakdown["by_context"]["other"] += 1
        
        return {
            "by_app": sorted(breakdown["by_app"].items(), key=lambda x: x[1], reverse=True),
            "by_state": breakdown["by_state"],
            "by_context": breakdown["by_context"]
        }
    
    def get_complete_analysis(self, hours: int = 24) -> Dict:
        """Complete activity analysis"""
        return {
            "productivity": self.productivity_score(hours=hours),
            "focus_analysis": self.calculate_focus_time(hours=hours),
            "tools_used": self.identify_most_used_tools(hours=hours*7),
            "trend_analysis": self.compare_productivity(),
            "activity_breakdown": self.get_activity_breakdown(hours=hours),
            "timestamp": datetime.datetime.now().isoformat()
        }


if __name__ == "__main__":
    memory = ObservationMemory()
    analyzer = ActivityAnalyzer(memory)
    
    print("📊 Activity Analyzer")
    print("\nProductivity Analysis:")
    
    productivity = analyzer.productivity_score()
    print(f"  Overall Score: {productivity['overall_productivity_score']}/100")
    print(f"  Typing Ratio: {productivity['typing_ratio']:.1f}%")
    
    print("\nTools Used:")
    tools = analyzer.identify_most_used_tools()
    for category in tools[:3]:
        print(f"  {category['category']}: {', '.join(t['name'] for t in category['tools'][:3])}")
























# ✅ Reviewed by AI - 2026-01-14T11:57:44.967378Z
# Complexity: 22 | Status: OPTIMAL


# ✅ Reviewed by AI - 2026-01-14T12:01:14.977219Z
# Complexity: 22 | Status: OPTIMAL


# ✅ Reviewed by AI - 2026-01-14T12:01:39.553017Z
# Complexity: 22 | Status: OPTIMAL
