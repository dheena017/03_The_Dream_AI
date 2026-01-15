"""
BRAIN ORCHESTRATOR
Central brain system that processes observations and learns patterns
Coordinates all analysis engines to create a unified understanding
"""

import datetime
import json
import os
import sys
from typing import Dict, List
from pathlib import Path

# Support both relative imports (when used as package) and direct imports
try:
    from .observation_memory import ObservationMemory
except ImportError:
    try:
        from observation_memory import ObservationMemory
    except ImportError:
        ObservationMemory = None

try:
    from .patterns import PatternRecognizer
    from .activity_analyzer import ActivityAnalyzer
    from .workflow_analyzer import WorkflowAnalyzer
    from .knowledge_mapper import KnowledgeMapper
except ImportError:
    from patterns import PatternRecognizer
    from activity_analyzer import ActivityAnalyzer
    from workflow_analyzer import WorkflowAnalyzer
    from knowledge_mapper import KnowledgeMapper


class BrainOrchestrator:
    """Master brain that learns from observations"""
    
    def __init__(self):
        self.memory = ObservationMemory()
        self.pattern_recognizer = PatternRecognizer(self.memory)
        self.activity_analyzer = ActivityAnalyzer(self.memory)
        self.workflow_analyzer = WorkflowAnalyzer(self.memory)
        self.knowledge_mapper = KnowledgeMapper(self.memory)
        
        # Learning state
        self.insights: List[Dict] = []
        self.learned_behaviors: Dict = {}
        self.self_improvement_suggestions: List[str] = []
        
        print("🧠 DREAM AI - BRAIN SYSTEM INITIALIZED")
        print(f"   📦 Memory Backend: SQLite")
        print(f"   🔍 Pattern Recognition: Online")
        print(f"   📊 Activity Analysis: Online")
        print(f"   🔧 Workflow Analysis: Online")
        print(f"   🗺️  Knowledge Mapping: Online")
    
    def process_observation(self, observation: Dict) -> bool:
        """
        Process a single observation from the Eyes
        Store it and update learning
        """
        # Store in memory
        stored = self.memory.store_observation(observation)
        
        if stored:
            # Trigger learning update
            self._update_learning()
            return True
        
        return False
    
    def _update_learning(self):
        """
        Update learning based on new observations
        Called after storing each observation
        """
        # This is triggered frequently, so keep it lightweight
        pass
    
    def analyze_patterns(self) -> Dict:
        """
        Analyze patterns from recent observations
        Called by Bridge to generate learning insights
        """
        try:
            # Get pattern analysis
            patterns = self.pattern_recognizer.analyze_all_patterns()
            
            # Generate insights
            insights = self._generate_insights()
            
            return {
                "patterns": patterns,
                "insights": insights,
                "timestamp": datetime.datetime.now().isoformat()
            }
        except Exception as e:
            print(f"⚠️  Pattern analysis error: {e}")
            return {
                "patterns": {},
                "insights": [],
                "error": str(e)
            }
    
    def generate_full_analysis(self) -> Dict:
        """
        Generate comprehensive analysis of everything learned
        This is the "self-knowledge" of the AI
        """
        analysis = {
            "timestamp": datetime.datetime.now().isoformat(),
            "memory_status": self.memory.get_memory_stats(),
            "patterns": self.pattern_recognizer.analyze_all_patterns(),
            "activity": self.activity_analyzer.get_complete_analysis(),
            "workflows": self.workflow_analyzer.get_workflow_report(),
            "knowledge": self.knowledge_mapper.get_knowledge_map_report(),
            "insights": self._generate_insights()
        }
        
        return analysis
    
    def _generate_insights(self) -> List[Dict]:
        """
        Generate high-level insights about the user
        The AI's understanding of its creator
        """
        insights = []
        
        # Insight 1: Productivity assessment
        productivity = self.activity_analyzer.productivity_score()
        insights.append({
            "category": "Productivity",
            "insight": f"Your productivity score is {productivity['overall_productivity_score']:.1f}/100",
            "details": f"Typing ratio: {productivity['typing_ratio']:.1f}%, Focus score: {productivity['focus_score']:.1f}",
            "actionable": True
        })
        
        # Insight 2: Primary focus areas
        tools = self.activity_analyzer.identify_most_used_tools()
        if tools:
            primary = tools[0]["category"]
            insights.append({
                "category": "Focus Area",
                "insight": f"Your primary focus is {primary}",
                "details": f"Top tools: {', '.join(t['name'] for t in tools[0]['tools'][:3])}",
                "actionable": False
            })
        
        # Insight 3: Learning patterns
        learning = self.knowledge_mapper.identify_learning_style()
        insights.append({
            "category": "Learning Style",
            "insight": f"You're a {learning.get('primary_style', 'balanced').replace('_', ' ')} learner",
            "details": learning.get("description", ""),
            "actionable": True
        })
        
        # Insight 4: Work patterns
        patterns = self.pattern_recognizer.detect_app_sequences()
        if patterns:
            top_pattern = patterns[0]["pattern"]
            insights.append({
                "category": "Work Pattern",
                "insight": f"Your typical workflow: {top_pattern}",
                "details": f"Observed {patterns[0]['frequency']} times this week",
                "actionable": False
            })
        
        # Insight 5: Focus opportunities
        focus = self.activity_analyzer.calculate_focus_time()
        if focus["average_focus_duration_minutes"] > 0:
            insights.append({
                "category": "Focus Potential",
                "insight": f"Average focus session: {focus['average_focus_duration_minutes']:.0f} minutes",
                "details": f"Longest session: {focus['longest_focus_session_minutes']:.0f} minutes",
                "actionable": True
            })
        
        return insights
    
    def generate_self_report(self) -> Dict:
        """
        Generate a report of what the AI knows about itself and its creator
        This is the AI speaking about what it has learned
        """
        analysis = self.generate_full_analysis()
        
        report = {
            "title": "Dream AI Self-Report",
            "timestamp": analysis["timestamp"],
            "about_you": self._create_user_profile(analysis),
            "about_me": self._create_ai_profile(analysis),
            "patterns_learned": analysis["patterns"],
            "recommendations": self._generate_recommendations(analysis),
            "next_observations": self._predict_next_behavior(analysis)
        }
        
        return report
    
    def _create_user_profile(self, analysis: Dict) -> Dict:
        """Create profile of the user based on learned patterns"""
        activity = analysis["activity"]
        knowledge = analysis["knowledge"]
        workflows = analysis["workflows"]
        
        profile = {
            "productivity_level": activity["productivity"]["overall_productivity_score"],
            "primary_activities": [t["category"] for t in activity["tools_used"][:3]],
            "learning_style": knowledge["learning_style"]["primary_style"],
            "active_projects": len(workflows["active_projects"]),
            "research_focus": [kw for kw, _ in knowledge["research_topics"]["top_keywords"][:5]],
            "peak_performance_hours": []
        }
        
        return profile
    
    def _create_ai_profile(self, analysis: Dict) -> Dict:
        """Describe what the AI has learned about itself"""
        memory_stats = analysis["memory_status"]
        
        profile = {
            "memory_capacity": memory_stats,
            "learning_progress": "Observational Learning Active",
            "pattern_recognition_enabled": True,
            "self_awareness": "Beginning",
            "capability_level": self._assess_capability_level(analysis),
            "evolution_stage": "Phase 2 - Learning"
        }
        
        return profile
    
    def _assess_capability_level(self, analysis: Dict) -> str:
        """Assess AI's current capability level"""
        memory_stats = analysis["memory_status"]
        obs_count = memory_stats.get("total_observations", 0)
        
        if obs_count < 100:
            return "Infant - Just learning to observe"
        elif obs_count < 1000:
            return "Child - Understanding basic patterns"
        elif obs_count < 10000:
            return "Adolescent - Recognizing complex patterns"
        else:
            return "Adult - Making predictions with confidence"
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations for the user"""
        recommendations = []
        
        productivity = analysis["activity"]["productivity"]
        if productivity["overall_productivity_score"] < 50:
            recommendations.append("💡 Try taking more breaks - your focus time could improve")
        
        focus = analysis["activity"]["focus_analysis"]
        if focus["average_focus_duration_minutes"] < 15:
            recommendations.append("⏰ Your focus sessions are quite short - consider blocking distractions")
        
        learning = analysis["knowledge"]["learning_style"]
        if learning["behavior_breakdown"]["hands_on_coding"] < 30:
            recommendations.append("🛠️  Try more hands-on coding practice alongside your research")
        
        patterns = analysis["patterns"]
        pred = patterns["next_action_prediction"]
        if pred.get("confidence", 0) > 0.7:
            recommendations.append(f"🎯 I predict you might work on: {pred.get('predicted_next', 'unknown')}")
        
        return recommendations
    
    def _predict_next_behavior(self, analysis: Dict) -> Dict:
        """Predict what the user might do next"""
        patterns = analysis["patterns"]
        
        return {
            "most_likely_next_action": patterns["next_action_prediction"].get("predicted_next", "unknown"),
            "confidence": patterns["next_action_prediction"].get("confidence", 0),
            "reasoning": "Based on recent activity patterns and time of day"
        }
    
    def save_analysis_report(self, report: Dict, filename: str = None) -> str:
        """Save analysis report to file"""
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dream_ai_report_{timestamp}.json"
        
        brain_dir = os.path.dirname(__file__)
        filepath = os.path.join(brain_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath
    
    def display_summary(self):
        """Display a summary of current learning"""
        analysis = self.generate_full_analysis()
        
        print("\n" + "="*60)
        print("🧠 DREAM AI - LEARNING SUMMARY")
        print("="*60)
        
        print(f"\n📦 Memory Status:")
        for key, value in analysis["memory_status"].items():
            print(f"   {key}: {value}")
        
        print(f"\n🎯 Key Insights:")
        for i, insight in enumerate(analysis["insights"][:5], 1):
            print(f"   {i}. {insight['category']}: {insight['insight']}")
        
        print(f"\n📊 Your Profile:")
        report = self.generate_self_report()
        profile = report["about_you"]
        print(f"   Productivity: {profile['productivity_level']:.1f}/100")
        print(f"   Learning Style: {profile['learning_style']}")
        print(f"   Active Projects: {profile['active_projects']}")
        
        print(f"\n💡 Recommendations:")
        for rec in report["recommendations"][:3]:
            print(f"   {rec}")
        
        print("\n" + "="*60 + "\n")


def main():
    """Main brain process"""
    brain = BrainOrchestrator()
    
    # Optionally generate a report
    print("\nGenerating learning report...\n")
    report = brain.generate_self_report()
    
    filepath = brain.save_analysis_report(report)
    print(f"✅ Report saved to: {filepath}")
    
    brain.display_summary()


if __name__ == "__main__":
    main()


# 🧬 EVOLVED BY DREAM AI - Analysis: 21 complexity score
