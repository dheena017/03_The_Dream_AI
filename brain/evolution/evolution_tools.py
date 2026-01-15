"""
BRAIN EVOLUTION WITH TOOLS
Upgraded evolution orchestrator that uses tools instead of just templates
Enables the Brain to take actions and make improvements dynamically
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json

try:
    from .tools import ToolRegistry, ToolExecutor
except ImportError:
    from tools import ToolRegistry, ToolExecutor


class EvolutionToolEngine:
    """Engine that uses tools to evolve the Brain"""
    
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.tool_executor = ToolExecutor(self.tool_registry)
        self.evolution_history: List[Dict] = []
        self.improvements_applied: List[Dict] = []
    
    def analyze_and_improve(self, code: str, context: Dict = None) -> Dict:
        """
        Analyze code and generate improvements using tools
        Instead of just templates, actually use tools to generate solutions
        """
        improvement_plan = {
            "timestamp": datetime.now().isoformat(),
            "original_code_length": len(code),
            "analysis": {},
            "improvements": [],
            "tool_calls": []
        }
        
        # Step 1: Analyze code performance using tool
        perf_result = self.tool_registry.call_tool(
            "analyze_code_performance",
            code=code
        )
        improvement_plan["analysis"]["performance"] = perf_result
        improvement_plan["tool_calls"].append({
            "tool": "analyze_code_performance",
            "success": perf_result["success"]
        })
        
        # Step 2: Find patterns using tool
        pattern_result = self.tool_registry.call_tool(
            "find_code_patterns",
            code=code
        )
        improvement_plan["analysis"]["patterns"] = pattern_result
        improvement_plan["tool_calls"].append({
            "tool": "find_code_patterns",
            "success": pattern_result["success"]
        })
        
        # Step 3: Generate optimized code using tool
        if perf_result["success"] and perf_result["result"]["issues_found"] > 0:
            opt_result = self.tool_registry.call_tool(
                "generate_optimized_code",
                code=code,
                optimization_type="general"
            )
            improvement_plan["improvements"].append({
                "type": "optimization",
                "original": code,
                "improved": opt_result["result"],
                "tool_used": "generate_optimized_code"
            })
            improvement_plan["tool_calls"].append({
                "tool": "generate_optimized_code",
                "success": opt_result["success"]
            })
        
        # Step 4: Refactor for readability
        refactor_result = self.tool_registry.call_tool(
            "refactor_code_section",
            code=code,
            style="pep8"
        )
        improvement_plan["improvements"].append({
            "type": "refactoring",
            "original": code,
            "improved": refactor_result["result"],
            "tool_used": "refactor_code_section"
        })
        improvement_plan["tool_calls"].append({
            "tool": "refactor_code_section",
            "success": refactor_result["success"]
        })
        
        self.evolution_history.append(improvement_plan)
        return improvement_plan
    
    def learn_from_observations(self, observations: List[Dict]) -> Dict:
        """
        Learn from observations using tools
        Extract insights, build models, and create suggestions
        """
        learning_result = {
            "timestamp": datetime.now().isoformat(),
            "observation_count": len(observations),
            "insights": [],
            "models": [],
            "suggestions": []
        }
        
        # Process each observation
        for obs in observations:
            # Use tool to learn from observation
            learn_result = self.tool_registry.call_tool(
                "learn_from_observation",
                observation=obs
            )
            
            if learn_result["success"]:
                learning_result["insights"].extend(
                    learn_result["result"].get("insights", [])
                )
        
        # Build pattern model if we have observations
        if observations:
            model_result = self.tool_registry.call_tool(
                "build_pattern_model",
                observations=observations
            )
            
            if model_result["success"]:
                learning_result["models"].append(model_result["result"])
        
        # Create improvement suggestions based on learning
        if learning_result["insights"]:
            suggestion = self._generate_improvement_suggestion(
                learning_result["insights"],
                observations
            )
            learning_result["suggestions"].append(suggestion)
        
        self.evolution_history.append(learning_result)
        return learning_result
    
    def _generate_improvement_suggestion(self, insights: List[Dict], 
                                        observations: List[Dict]) -> Dict:
        """Generate actionable improvements based on insights"""
        
        # Analyze insights to determine what needs improvement
        improvement_areas = {}
        for insight in insights:
            area = insight.get("type", "unknown")
            improvement_areas[area] = improvement_areas.get(area, 0) + 1
        
        # Create suggestion using tool
        suggestion_context = {
            "title": "Performance Improvement Suggestion",
            "description": f"Based on {len(insights)} insights from observations",
            "priority": "high" if len(insights) > 5 else "medium",
            "steps": [
                "Analyze current behavior patterns",
                "Identify optimization opportunities",
                "Implement improvements",
                "Monitor for effectiveness"
            ],
            "benefit": "Optimized system performance and responsiveness"
        }
        
        suggestion_result = self.tool_registry.call_tool(
            "create_improvement_suggestion",
            context=suggestion_context
        )
        
        return suggestion_result["result"]
    
    def apply_improvement(self, improvement: Dict) -> Dict:
        """Apply an improvement and track it"""
        application_result = {
            "improvement_id": improvement.get("id"),
            "timestamp": datetime.now().isoformat(),
            "status": "applied",
            "before": improvement.get("original"),
            "after": improvement.get("improved"),
            "metrics": {
                "before_length": len(improvement.get("original", "")),
                "after_length": len(improvement.get("improved", ""))
            }
        }
        
        self.improvements_applied.append(application_result)
        return application_result
    
    def validate_improvement(self, solution: Dict, requirements: Dict = None) -> Dict:
        """Validate that an improvement meets requirements"""
        
        if requirements is None:
            requirements = {
                "functionality": "preserved",
                "readability": "improved",
                "performance": "optimized"
            }
        
        validation_result = self.tool_registry.call_tool(
            "validate_solution",
            solution=solution,
            requirements=requirements
        )
        
        return validation_result["result"]
    
    def get_evolution_report(self) -> Dict:
        """Generate report on Brain evolution"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_evolution_steps": len(self.evolution_history),
            "improvements_applied": len(self.improvements_applied),
            "tool_statistics": self.tool_registry.get_statistics(),
            "recent_executions": self.tool_registry.get_execution_history(5),
            "improvement_timeline": self.improvements_applied[-5:] if self.improvements_applied else []
        }
        
        return report
    
    def get_available_tools(self) -> List[Dict]:
        """Get list of available tools for improvement"""
        return self.tool_registry.get_tools()
    
    def register_custom_tool(self, name: str, func, description: str, category: str):
        """Register a custom tool for brain evolution"""
        self.tool_registry.register_tool(name, func, description, category=category)


class DynamicImprover:
    """Make real-time improvements to code and systems"""
    
    def __init__(self, engine: EvolutionToolEngine = None):
        self.engine = engine or EvolutionToolEngine()
        self.active_improvements: Dict = {}
    
    def improve_function(self, function_code: str, context: Dict = None) -> Dict:
        """Improve a specific function"""
        result = self.engine.analyze_and_improve(function_code, context)
        
        best_improvement = max(
            result.get("improvements", []),
            key=lambda x: len(x.get("original", "")) - len(x.get("improved", "")),
            default=None
        )
        
        if best_improvement:
            self.engine.apply_improvement(best_improvement)
            return {
                "original": best_improvement["original"],
                "improved": best_improvement["improved"],
                "improvement_type": best_improvement["type"],
                "applied": True
            }
        
        return {"applied": False, "reason": "No improvements found"}
    
    def improve_workflow(self, observations: List[Dict]) -> Dict:
        """Improve workflow based on observations"""
        learning = self.engine.learn_from_observations(observations)
        
        return {
            "insights_gained": len(learning["insights"]),
            "suggestions": learning["suggestions"],
            "models_created": len(learning["models"]),
            "next_steps": self._get_next_steps(learning)
        }
    
    def _get_next_steps(self, learning: Dict) -> List[str]:
        """Determine next steps based on learning"""
        suggestions = learning.get("suggestions", [])
        
        if not suggestions:
            return ["Continue monitoring for patterns", "Collect more observations"]
        
        next_steps = []
        for suggestion in suggestions:
            if "steps" in suggestion:
                next_steps.extend(suggestion["steps"])
        
        return next_steps


if __name__ == "__main__":
    # Test the tools-based evolution system
    engine = EvolutionToolEngine()
    
    print("🧠 BRAIN EVOLUTION WITH TOOLS - TEST")
    print("\n" + "="*50)
    
    # Test 1: Code analysis and improvement
    print("\n1️⃣  Testing Code Analysis and Improvement")
    print("-" * 50)
    
    test_code = """
result = ""
for item in items:
    result += str(item) + ", "
"""
    
    improvement_plan = engine.analyze_and_improve(test_code)
    print(f"Improvements found: {len(improvement_plan['improvements'])}")
    for imp in improvement_plan['improvements']:
        print(f"  - {imp['type']}: {imp['tool_used']}")
    
    # Test 2: Learning from observations
    print("\n2️⃣  Testing Learning from Observations")
    print("-" * 50)
    
    test_observations = [
        {
            "timestamp": datetime.now().isoformat(),
            "sensors": {
                "screen": {
                    "active_window": {"app_name": "VSCode"}
                },
                "input": {
                    "idle_time": {"idle_status": "active"}
                }
            }
        },
        {
            "timestamp": datetime.now().isoformat(),
            "sensors": {
                "screen": {
                    "active_window": {"app_name": "Chrome"}
                },
                "input": {
                    "idle_time": {"idle_status": "active"}
                }
            }
        }
    ]
    
    learning_result = engine.learn_from_observations(test_observations)
    print(f"Insights extracted: {len(learning_result['insights'])}")
    print(f"Suggestions generated: {len(learning_result['suggestions'])}")
    
    # Test 3: Tool registry
    print("\n3️⃣  Testing Tool Registry")
    print("-" * 50)
    
    tools = engine.get_available_tools()
    print(f"Total tools available: {len(tools)}")
    
    categories = {}
    for tool in tools:
        cat = tool.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    print("Tools by category:")
    for cat, count in categories.items():
        print(f"  - {cat}: {count}")
    
    # Test 4: Evolution report
    print("\n4️⃣  Evolution Report")
    print("-" * 50)
    
    report = engine.get_evolution_report()
    print(f"Total evolution steps: {report['total_evolution_steps']}")
    print(f"Improvements applied: {report['improvements_applied']}")
    print(f"Tool statistics: {report['tool_statistics']['total_executions']} executions")
