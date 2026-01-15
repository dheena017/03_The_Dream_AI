"""Orchestrates a simple self-evolution cycle for Dream AI."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, Any, List

from .code_analyzer import CodeAnalyzer
from .performance_profiler import Profiler
from .self_modifier import SelfModifier

# Import new tools-based evolution system
try:
    from .evolution_tools import EvolutionToolEngine, DynamicImprover
except ImportError:
    EvolutionToolEngine = None
    DynamicImprover = None


class EvolutionOrchestrator:
    """Tie together analysis, profiling, and safe code modification."""

    def __init__(self, base_dir: Optional[str] = None, use_tools: bool = True) -> None:
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent.parent
        self.analyzer = CodeAnalyzer()
        self.profiler = Profiler()
        self.modifier = SelfModifier(base_dir=str(self.base_dir))
        
        # Initialize tools-based evolution engine if available
        self.use_tools = use_tools and EvolutionToolEngine is not None
        if self.use_tools:
            self.tool_engine = EvolutionToolEngine()
            self.improver = DynamicImprover(self.tool_engine)
        else:
            self.tool_engine = None
            self.improver = None

    def evolve_module(self, module_path: str, use_tools_enhancement: bool = True) -> dict:
        """Analyze, improve, and safely rewrite a module.

        Steps:
        1. Analyze the current code using traditional methods
        2. Use tools-based analysis for deep insights
        3. Produce improvements (with tools or templates)
        4. Validate and apply the change with backup
        """
        target = Path(module_path)
        if not target.exists():
            raise FileNotFoundError(f"Module not found: {module_path}")

        analysis = self.analyzer.analyze_file(str(target))
        
        original = target.read_text(encoding="utf-8")
        
        # Step 1: Traditional improvement (backward compatible)
        improved = "# Optimized by Dream AI\n" + original
        
        # Step 2: Use tools-based enhancement if available and enabled
        if use_tools_enhancement and self.use_tools:
            tool_improvement = self.improver.improve_function(original)
            if tool_improvement.get("applied"):
                improved = tool_improvement["improved"]
                analysis["tool_enhanced"] = True
                analysis["improvement_type"] = tool_improvement["improvement_type"]

        backup_path = self.modifier.rewrite_code(str(target), improved)

        return {
            "module": str(target),
            "analysis": analysis,
            "backup": backup_path,
            "status": "updated",
            "tools_used": self.use_tools and use_tools_enhancement
        }
    
    def evolve_from_observations(self, observations: List[Dict]) -> Dict[str, Any]:
        """Use observations to drive evolution decisions"""
        if not self.use_tools:
            return {"error": "Tools engine not initialized"}
        
        result = self.improver.improve_workflow(observations)
        
        return {
            "insights": result["insights_gained"],
            "suggestions": result["suggestions"],
            "models": result["models_created"],
            "next_steps": result["next_steps"],
            "timestamp": self.tool_engine.evolution_history[-1].get("timestamp") if self.tool_engine.evolution_history else None
        }
    
    def get_available_tools(self) -> List[Dict]:
        """Get available tools for evolution"""
        if not self.use_tools:
            return []
        
        return self.tool_engine.get_available_tools()
    
    def get_evolution_statistics(self) -> Dict[str, Any]:
        """Get statistics on evolution progress"""
        if not self.use_tools:
            return {"tools_enabled": False}
        
        report = self.tool_engine.get_evolution_report()
        return report


# 🧬 EVOLVED BY DREAM AI - Analysis: 3 complexity score
