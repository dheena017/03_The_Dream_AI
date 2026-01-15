"""
BRAIN TOOLS SYSTEM
Enables the Brain to call functions and perform actions rather than just using templates
Tools are executable functions the AI can invoke during learning and adaptation
"""

import json
import inspect
from typing import Dict, List, Any, Callable, Optional
import asyncio
from datetime import datetime


class ToolRegistry:
    """Registry of available tools that the Brain can use"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.schemas: Dict[str, Dict] = {}
        self.execution_history: List[Dict] = []
        self._register_builtin_tools()
    
    def register_tool(self, tool_name: str, func: Callable, description: str = "", 
                     parameters: Dict = None, category: str = "general"):
        """
        Register a new tool the Brain can use
        
        Args:
            tool_name: Unique name for the tool
            func: The function to execute
            description: What this tool does
            parameters: Parameter schema
            category: Tool category (analysis, code, learning, action, etc)
        """
        self.tools[tool_name] = func
        
        # Auto-generate schema from function signature
        sig = inspect.signature(func)
        params = {}
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            param_type = param.annotation if param.annotation != inspect.Parameter.empty else "any"
            params[param_name] = {
                "type": str(param_type),
                "required": param.default == inspect.Parameter.empty
            }
        
        self.schemas[tool_name] = {
            "name": tool_name,
            "description": description,
            "category": category,
            "parameters": parameters or params,
            "returns": inspect.signature(func).return_annotation or "any"
        }
    
    def _register_builtin_tools(self):
        """Register built-in tools"""
        
        # Code analysis tools
        self.register_tool(
            "analyze_code_performance",
            self._analyze_code_performance,
            "Analyze code for performance issues",
            category="analysis"
        )
        
        self.register_tool(
            "find_code_patterns",
            self._find_code_patterns,
            "Find common code patterns in given code",
            category="analysis"
        )
        
        # Code generation tools
        self.register_tool(
            "generate_optimized_code",
            self._generate_optimized_code,
            "Generate optimized version of code",
            category="code"
        )
        
        self.register_tool(
            "refactor_code_section",
            self._refactor_code_section,
            "Refactor a code section for readability",
            category="code"
        )
        
        # Learning tools
        self.register_tool(
            "learn_from_observation",
            self._learn_from_observation,
            "Extract learning insights from observations",
            category="learning"
        )
        
        self.register_tool(
            "build_pattern_model",
            self._build_pattern_model,
            "Build statistical model from patterns",
            category="learning"
        )
        
        # Action tools
        self.register_tool(
            "create_improvement_suggestion",
            self._create_improvement_suggestion,
            "Create actionable improvement suggestion",
            category="action"
        )
        
        self.register_tool(
            "validate_solution",
            self._validate_solution,
            "Validate if solution meets requirements",
            category="action"
        )
    
    def _analyze_code_performance(self, code: str) -> Dict:
        """Analyze code for performance issues"""
        issues = []
        
        # Check for common performance issues
        if "for" in code and code.count("for") > 1:
            issues.append({
                "type": "nested_loops",
                "severity": "high",
                "suggestion": "Consider using dictionary lookup or list comprehension"
            })
        
        if "+= " in code and "for" in code:
            issues.append({
                "type": "string_concatenation",
                "severity": "high",
                "suggestion": "Use list + join instead of += in loops"
            })
        
        if "SELECT" in code.upper() and "for" in code:
            issues.append({
                "type": "database_queries_in_loop",
                "severity": "high",
                "suggestion": "Batch queries outside the loop"
            })
        
        if len(code) > 1000:
            issues.append({
                "type": "function_too_long",
                "severity": "medium",
                "suggestion": "Break into smaller functions"
            })
        
        return {
            "code_length": len(code),
            "issues_found": len(issues),
            "issues": issues,
            "analysis_time": datetime.now().isoformat()
        }
    
    def _find_code_patterns(self, code: str, pattern_type: str = "all") -> Dict:
        """Find common code patterns"""
        patterns = {}
        
        # Pattern: loops
        if "for" in code or "while" in code:
            loop_count = code.count("for") + code.count("while")
            patterns["loops"] = {
                "count": loop_count,
                "description": f"Found {loop_count} loop statements"
            }
        
        # Pattern: conditionals
        if "if " in code:
            cond_count = code.count("if ")
            patterns["conditionals"] = {
                "count": cond_count,
                "description": f"Found {cond_count} conditional statements"
            }
        
        # Pattern: function definitions
        if "def " in code:
            func_count = code.count("def ")
            patterns["functions"] = {
                "count": func_count,
                "description": f"Found {func_count} function definitions"
            }
        
        # Pattern: error handling
        if "try:" in code:
            try_count = code.count("try:")
            patterns["error_handling"] = {
                "count": try_count,
                "description": f"Found {try_count} try-except blocks"
            }
        
        return {
            "patterns": patterns,
            "pattern_count": len(patterns),
            "analysis_time": datetime.now().isoformat()
        }
    
    def _generate_optimized_code(self, code: str, optimization_type: str = "general") -> str:
        """Generate optimized version of code"""
        optimized = code
        
        # Optimization: nested loops
        if "for" in code and code.count("for") > 1:
            optimized = "# OPTIMIZED: Using dictionary lookup instead of nested loops\n" + optimized
        
        # Optimization: string concatenation
        if "+= " in code and "for" in code:
            optimized = optimized.replace("result += ", "result.append(")
            optimized = "\nresult = []\n" + optimized + "\nresult = ''.join(result)\n"
        
        return optimized
    
    def _refactor_code_section(self, code: str, style: str = "pep8") -> str:
        """Refactor code section"""
        lines = code.split('\n')
        refactored = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            # Standardize indentation to 4 spaces
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces % 4 != 0:
                # Normalize to 4-space indentation
                indent_level = leading_spaces // 2
                line = "    " * indent_level + line.lstrip()
            refactored.append(line)
        
        return '\n'.join(refactored)
    
    def _learn_from_observation(self, observation: Dict) -> Dict:
        """Extract learning insights from observations"""
        insights = []
        
        # Analyze activity patterns
        if "sensors" in observation:
            sensors = observation["sensors"]
            
            if "screen" in sensors and "active_window" in sensors["screen"]:
                insights.append({
                    "type": "app_usage",
                    "value": sensors["screen"]["active_window"].get("app_name"),
                    "timestamp": observation.get("timestamp")
                })
            
            if "input" in sensors and "idle_status" in sensors["input"].get("idle_time", {}):
                insights.append({
                    "type": "activity_level",
                    "value": sensors["input"]["idle_time"]["idle_status"],
                    "timestamp": observation.get("timestamp")
                })
        
        return {
            "insights_extracted": len(insights),
            "insights": insights,
            "learning_time": datetime.now().isoformat()
        }
    
    def _build_pattern_model(self, observations: List[Dict]) -> Dict:
        """Build statistical model from patterns"""
        if not observations:
            return {"error": "No observations provided"}
        
        # Collect data points
        apps = {}
        times = []
        
        for obs in observations:
            timestamp = obs.get("timestamp")
            if timestamp:
                times.append(timestamp)
            
            screen = obs.get("sensors", {}).get("screen", {})
            if "active_window" in screen:
                app = screen["active_window"].get("app_name")
                apps[app] = apps.get(app, 0) + 1
        
        # Build model
        model = {
            "observation_count": len(observations),
            "app_distribution": apps,
            "time_span": f"{times[0]} to {times[-1]}" if times else "unknown",
            "most_used_app": max(apps, key=apps.get) if apps else None
        }
        
        return model
    
    def _create_improvement_suggestion(self, context: Dict) -> Dict:
        """Create actionable improvement suggestion"""
        suggestion = {
            "id": f"sugg_{datetime.now().timestamp()}",
            "title": context.get("title", "Improvement Suggestion"),
            "description": context.get("description", ""),
            "priority": context.get("priority", "medium"),
            "implementation_steps": context.get("steps", []),
            "expected_benefit": context.get("benefit", "Improvement in system efficiency"),
            "created_at": datetime.now().isoformat()
        }
        
        return suggestion
    
    def _validate_solution(self, solution: Dict, requirements: Dict) -> Dict:
        """Validate if solution meets requirements"""
        validation_results = {
            "solution_id": solution.get("id"),
            "valid": True,
            "checks": []
        }
        
        # Check each requirement
        for req_name, req_value in requirements.items():
            check = {
                "requirement": req_name,
                "expected": req_value,
                "actual": solution.get(req_name),
                "met": solution.get(req_name) == req_value
            }
            validation_results["checks"].append(check)
            if not check["met"]:
                validation_results["valid"] = False
        
        return validation_results
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict:
        """
        Call a registered tool
        
        Returns:
            Dict with result and metadata
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(self.tools.keys())
            }
        
        try:
            tool_func = self.tools[tool_name]
            result = tool_func(**kwargs)
            
            execution_record = {
                "tool": tool_name,
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "params": kwargs,
                "result": result
            }
            self.execution_history.append(execution_record)
            
            return {
                "success": True,
                "tool": tool_name,
                "result": result
            }
        
        except TypeError as e:
            return {
                "success": False,
                "error": f"Invalid parameters: {str(e)}",
                "schema": self.schemas.get(tool_name)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            }
    
    def get_tools(self, category: str = None) -> List[Dict]:
        """Get available tools, optionally filtered by category"""
        tools = []
        
        for tool_name, schema in self.schemas.items():
            if category is None or schema.get("category") == category:
                tools.append(schema)
        
        return tools
    
    def get_execution_history(self, limit: int = 10) -> List[Dict]:
        """Get recent tool execution history"""
        return self.execution_history[-limit:]
    
    def get_statistics(self) -> Dict:
        """Get statistics about tool usage"""
        tool_usage = {}
        
        for record in self.execution_history:
            tool = record["tool"]
            tool_usage[tool] = tool_usage.get(tool, 0) + 1
        
        return {
            "total_tools_registered": len(self.tools),
            "total_executions": len(self.execution_history),
            "tool_usage": tool_usage,
            "categories": list(set(s.get("category") for s in self.schemas.values()))
        }


class ToolExecutor:
    """Execute tool calls from the Brain's decisions"""
    
    def __init__(self, registry: ToolRegistry = None):
        self.registry = registry or ToolRegistry()
        self.execution_queue = []
        self.execution_results = []
    
    def queue_tool_call(self, tool_name: str, params: Dict) -> str:
        """Queue a tool call for execution"""
        call_id = f"call_{len(self.execution_queue)}_{datetime.now().timestamp()}"
        
        self.execution_queue.append({
            "id": call_id,
            "tool": tool_name,
            "params": params,
            "status": "queued"
        })
        
        return call_id
    
    def execute_queue(self) -> List[Dict]:
        """Execute all queued tool calls"""
        results = []
        
        for call in self.execution_queue:
            if call["status"] == "queued":
                result = self.registry.call_tool(call["tool"], **call["params"])
                call["status"] = "executed"
                call["result"] = result
                call["executed_at"] = datetime.now().isoformat()
                results.append(call)
        
        self.execution_results.extend(results)
        return results
    
    def get_result(self, call_id: str) -> Optional[Dict]:
        """Get result of a specific tool call"""
        for result in self.execution_results:
            if result.get("id") == call_id:
                return result
        return None


if __name__ == "__main__":
    # Test the tools system
    registry = ToolRegistry()
    
    print("🧠 BRAIN TOOLS SYSTEM TEST")
    print(f"\nRegistered {len(registry.tools)} tools\n")
    
    # Test tool categories
    categories = list(set(s.get("category") for s in registry.schemas.values()))
    print("Tool Categories:")
    for cat in categories:
        tools_in_cat = [t for t in registry.get_tools(cat)]
        print(f"  {cat}: {len(tools_in_cat)} tools")
    
    # Test calling a tool
    code_sample = """
for item1 in list1:
    for item2 in list2:
        if item1.id == item2.id:
            process(item1, item2)
"""
    
    print("\n\n📊 Testing analyze_code_performance tool:")
    result = registry.call_tool("analyze_code_performance", code=code_sample)
    print(f"Success: {result['success']}")
    print(f"Issues found: {result['result']['issues_found']}")
