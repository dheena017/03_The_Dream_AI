"""
HUMAN-LIKE COGNITIVE ARCHITECTURE
Redesigns Dream AI to mimic human brain's cognitive processes

Human Brain Structure:
1. Sensory Input (Eyes) → Thalamus → Cortex
2. Working Memory (Prefrontal Cortex)
3. Long-term Memory (Hippocampus)
4. Pattern Recognition (Temporal Lobe)
5. Decision Making (Frontal Lobe)
6. Motor Output (Actions/Tasks)
7. Emotional/Priority System (Amygdala)
8. Learning & Adaptation (Neuroplasticity)
"""

import os
import sys
import json
import datetime
import threading
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
from collections import deque


class CognitiveArchitecture:
    """
    Human-like cognitive processing system
    Mimics how the human brain processes information
    """
    
    def __init__(self):
        # 1. SENSORY BUFFER (like Thalamus)
        self.sensory_buffer = deque(maxlen=100)  # Short-term sensory memory
        
        # 2. WORKING MEMORY (like Prefrontal Cortex)
        self.working_memory = {
            "current_focus": None,
            "active_goals": [],
            "context": {},
            "recent_actions": deque(maxlen=10)
        }
        
        # 3. LONG-TERM MEMORY (like Hippocampus)
        self.long_term_memory = {
            "episodic": [],  # Specific events/experiences
            "semantic": {},  # Facts and knowledge
            "procedural": {},  # How to do things
            "skills": []
        }
        
        # 4. ATTENTION SYSTEM (like Attention Network)
        self.attention = {
            "focus_level": 1.0,
            "current_priority": None,
            "distractions": 0
        }
        
        # 5. EMOTIONAL/PRIORITY SYSTEM (like Amygdala)
        self.emotional_state = {
            "urgency": 0.5,
            "importance": 0.5,
            "motivation": 0.8,
            "confidence": 0.5
        }
        
        # 6. LEARNING SYSTEM (Neuroplasticity)
        self.learning_state = {
            "pattern_strengths": {},
            "successful_strategies": [],
            "failed_strategies": [],
            "adaptation_rate": 0.1
        }
        
        self.is_online = True  # Assume online by default
        self._start_connectivity_check()

        print("🧠 HUMAN-LIKE COGNITIVE ARCHITECTURE INITIALIZED")
        print("   📥 Sensory Buffer: Ready")
        print("   🎯 Working Memory: Online")
        print("   💾 Long-term Memory: Active")
        print("   👁️  Attention System: Focused")
        print("   ❤️  Emotional System: Calibrated")
        print("   📚 Learning System: Adaptive")
    
    def perceive(self, observation: Dict) -> bool:
        """
        PERCEPTION STAGE (like Visual/Sensory Cortex)
        Filter and process incoming sensory data
        """
        # Add to sensory buffer (immediate perception)
        self.sensory_buffer.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "data": observation,
            "processed": False
        })
        
        # Attention filtering (what's worth focusing on?)
        if self._is_attention_worthy(observation):
            self._transfer_to_working_memory(observation)
            return True
        
        return False
    
    def _is_attention_worthy(self, observation: Dict) -> bool:
        """
        Decide if something deserves attention
        (like brain's saliency detection)
        """
        # Check for novelty
        if self._is_novel(observation):
            return True
        
        # Check for relevance to current goals
        if self._is_relevant_to_goals(observation):
            return True
        
        # Check for emotional significance
        if self._has_emotional_significance(observation):
            return True
        
        return False
    
    def _is_novel(self, observation: Dict) -> bool:
        """Check if this is something new/unexpected"""
        # Simple novelty detection
        obs_type = observation.get("type", "unknown")
        return obs_type not in self.long_term_memory.get("semantic", {})
    
    def _is_relevant_to_goals(self, observation: Dict) -> bool:
        """Check if observation relates to active goals"""
        if not self.working_memory["active_goals"]:
            return False
        
        # Check if observation contains keywords from goals
        obs_str = str(observation).lower()
        for goal in self.working_memory["active_goals"]:
            if any(keyword in obs_str for keyword in goal.get("keywords", [])):
                return True
        
        return False
    
    def _has_emotional_significance(self, observation: Dict) -> bool:
        """Check for emotional triggers (errors, success, etc)"""
        obs_str = str(observation).lower()
        emotional_triggers = ["error", "success", "fail", "complete", "urgent"]
        return any(trigger in obs_str for trigger in emotional_triggers)
    
    def _transfer_to_working_memory(self, observation: Dict):
        """Move important observations to working memory"""
        self.working_memory["current_focus"] = observation
        self.working_memory["context"]["last_update"] = datetime.datetime.now().isoformat()
    
    def think(self, task: str) -> Dict:
        """
        COGNITIVE PROCESSING (like Prefrontal Cortex)
        Multi-stage thinking process like human cognition
        """
        thought_process = {
            "task": task,
            "start_time": datetime.datetime.now().isoformat(),
            "stages": []
        }
        
        # STAGE 1: Comprehension (Understanding)
        comprehension = self._comprehend_task(task)
        thought_process["stages"].append({"stage": "comprehension", "result": comprehension})
        
        # STAGE 2: Memory Retrieval (Recall similar experiences)
        memories = self._retrieve_relevant_memories(task)
        thought_process["stages"].append({"stage": "memory_retrieval", "result": len(memories)})
        
        # STAGE 3: Pattern Matching (Find similar patterns)
        patterns = self._match_patterns(task, memories)
        thought_process["stages"].append({"stage": "pattern_matching", "result": patterns})
        
        # STAGE 4: Planning (How to solve this?)
        plan = self._generate_plan(task, comprehension, patterns)
        thought_process["stages"].append({"stage": "planning", "result": plan})
        
        # STAGE 5: Evaluation (Will this work?)
        evaluation = self._evaluate_plan(plan)
        thought_process["stages"].append({"stage": "evaluation", "result": evaluation})
        
        # STAGE 6: Decision (Commit to action)
        decision = self._make_decision(plan, evaluation)
        thought_process["stages"].append({"stage": "decision", "result": decision})
        
        thought_process["end_time"] = datetime.datetime.now().isoformat()
        return thought_process
    
    def _comprehend_task(self, task: str) -> Dict:
        """Understand what the task is asking for"""
        task_lower = task.lower()
        
        comprehension = {
            "intent": "unknown",
            "keywords": [],
            "complexity": "simple"
        }
        
        # Detect intent
        if "search" in task_lower or "google" in task_lower:
            comprehension["intent"] = "web_search"
            comprehension["keywords"] = ["search", "web", "internet"]
        elif "create" in task_lower or "write" in task_lower or "generate" in task_lower:
            comprehension["intent"] = "create"
            comprehension["keywords"] = ["create", "generate", "write"]
        elif "analyze" in task_lower or "check" in task_lower:
            comprehension["intent"] = "analyze"
            comprehension["keywords"] = ["analyze", "check", "examine"]
        elif "run" in task_lower or "execute" in task_lower:
            comprehension["intent"] = "execute"
            comprehension["keywords"] = ["run", "execute", "perform"]
        
        # Detect complexity
        word_count = len(task.split())
        if word_count > 15:
            comprehension["complexity"] = "complex"
        elif word_count > 8:
            comprehension["complexity"] = "moderate"
        
        return comprehension
    
    def _retrieve_relevant_memories(self, task: str) -> List[Dict]:
        """Retrieve similar past experiences"""
        relevant = []
        
        task_words = set(task.lower().split())
        
        # Search episodic memory (past experiences)
        for memory in self.long_term_memory.get("episodic", []):
            memory_words = set(str(memory).lower().split())
            overlap = len(task_words & memory_words)
            if overlap > 2:
                relevant.append(memory)
        
        return relevant[:5]  # Return top 5 most relevant
    
    def _match_patterns(self, task: str, memories: List[Dict]) -> Dict:
        """Find patterns in task and memories"""
        patterns = {
            "recognized_patterns": [],
            "confidence": 0.0
        }
        
        # Check procedural memory for known patterns
        task_lower = task.lower()
        for pattern_name, pattern_data in self.long_term_memory.get("procedural", {}).items():
            if any(keyword in task_lower for keyword in pattern_data.get("triggers", [])):
                patterns["recognized_patterns"].append(pattern_name)
                patterns["confidence"] += 0.2
        
        patterns["confidence"] = min(patterns["confidence"], 1.0)
        return patterns
    
    def _generate_plan(self, task: str, comprehension: Dict, patterns: Dict) -> Dict:
        """Create a plan to accomplish the task"""
        plan = {
            "approach": comprehension["intent"],
            "steps": [],
            "resources_needed": [],
            "estimated_difficulty": comprehension["complexity"]
        }
        
        # Generate steps based on intent
        if comprehension["intent"] == "web_search":
            plan["steps"] = [
                "Extract search query from task",
                "Use web search capability",
                "Parse and format results",
                "Save results to file"
            ]
            plan["resources_needed"] = ["internet", "search_library"]
        
        elif comprehension["intent"] == "create":
            plan["steps"] = [
                "Determine what to create",
                "Generate code/content",
                "Validate output",
                "Save to file"
            ]
            plan["resources_needed"] = ["code_templates", "file_system"]
        
        else:
            plan["steps"] = ["Analyze task", "Execute appropriate action"]
        
        return plan
    
    def _evaluate_plan(self, plan: Dict) -> Dict:
        """Evaluate if the plan is good"""
        evaluation = {
            "viable": True,
            "risks": [],
            "success_probability": 0.8
        }
        
        # Check if resources are available
        for resource in plan.get("resources_needed", []):
            if resource == "internet" and not self._has_internet():
                evaluation["risks"].append("No internet connection")
                evaluation["success_probability"] -= 0.3
        
        evaluation["viable"] = evaluation["success_probability"] > 0.5
        return evaluation
    
    def _start_connectivity_check(self):
        """Start a background thread to check internet connectivity"""
        self.connectivity_thread = threading.Thread(target=self._check_internet_connectivity_loop, daemon=True)
        self.connectivity_thread.start()

    def _check_internet_connectivity_loop(self):
        """Periodically check internet status"""
        while True:
            self.is_online = self._check_internet_status()
            time.sleep(60)  # Check every 60 seconds

    def _check_internet_status(self) -> bool:
        """The actual check for internet connectivity"""
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=1)
            return True
        except:
            return False

    def _has_internet(self) -> bool:
        """Check if internet is available (non-blocking)"""
        return self.is_online
    
    def _make_decision(self, plan: Dict, evaluation: Dict) -> Dict:
        """Decide whether to proceed"""
        decision = {
            "proceed": evaluation["viable"],
            "confidence": evaluation["success_probability"],
            "reasoning": ""
        }
        
        if evaluation["viable"]:
            decision["reasoning"] = "Plan appears viable, proceeding"
        else:
            decision["reasoning"] = f"Risks too high: {evaluation['risks']}"
        
        return decision
    
    def learn(self, experience: Dict, outcome: str):
        """
        LEARNING STAGE (Neuroplasticity)
        Strengthen or weaken connections based on outcomes
        """
        # Store episodic memory
        self.long_term_memory["episodic"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "experience": experience,
            "outcome": outcome
        })
        
        # Update pattern strengths
        if outcome == "success":
            # Strengthen successful patterns
            if "patterns" in experience:
                for pattern in experience["patterns"]:
                    current_strength = self.learning_state["pattern_strengths"].get(pattern, 0.5)
                    new_strength = min(current_strength + self.learning_state["adaptation_rate"], 1.0)
                    self.learning_state["pattern_strengths"][pattern] = new_strength
        
        elif outcome == "failure":
            # Weaken failed patterns
            if "patterns" in experience:
                for pattern in experience["patterns"]:
                    current_strength = self.learning_state["pattern_strengths"].get(pattern, 0.5)
                    new_strength = max(current_strength - self.learning_state["adaptation_rate"], 0.0)
                    self.learning_state["pattern_strengths"][pattern] = new_strength
        
        # Trim old memories (like sleep consolidation)
        if len(self.long_term_memory["episodic"]) > 1000:
            self._consolidate_memories()
    
    def _consolidate_memories(self):
        """Consolidate memories like brain does during sleep"""
        # Keep only the most important/recent memories
        sorted_memories = sorted(
            self.long_term_memory["episodic"],
            key=lambda x: (x.get("importance", 0.5), x.get("timestamp", "")),
            reverse=True
        )
        self.long_term_memory["episodic"] = sorted_memories[:500]
    
    def get_state_summary(self) -> Dict:
        """Get current cognitive state (like self-awareness)"""
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "working_memory": {
                "current_focus": self.working_memory["current_focus"] is not None,
                "active_goals": len(self.working_memory["active_goals"]),
                "recent_actions": len(self.working_memory["recent_actions"])
            },
            "long_term_memory": {
                "episodic_memories": len(self.long_term_memory["episodic"]),
                "skills": len(self.long_term_memory["skills"]),
                "patterns_learned": len(self.learning_state["pattern_strengths"])
            },
            "attention": self.attention,
            "emotional_state": self.emotional_state,
            "learning_progress": {
                "successful_strategies": len(self.learning_state["successful_strategies"]),
                "adaptation_rate": self.learning_state["adaptation_rate"]
            }
        }


if __name__ == "__main__":
    # Test cognitive architecture
    cog = CognitiveArchitecture()
    
    print("\n🧪 TESTING HUMAN-LIKE COGNITION\n")
    
    # Test perception
    print("1. PERCEPTION TEST:")
    observation = {"type": "task", "content": "Search for Bitcoin price"}
    cog.perceive(observation)
    print(f"   ✅ Observation processed")
    
    # Test thinking
    print("\n2. THINKING TEST:")
    thought = cog.think("Search Google for latest Python version")
    print(f"   ✅ Completed {len(thought['stages'])} cognitive stages:")
    for stage in thought["stages"]:
        print(f"      - {stage['stage']}: ✓")
    
    # Test learning
    print("\n3. LEARNING TEST:")
    cog.learn({"task": "test", "patterns": ["search"]}, "success")
    print(f"   ✅ Experience stored in long-term memory")
    
    # Get state
    print("\n4. SELF-AWARENESS TEST:")
    state = cog.get_state_summary()
    print(f"   ✅ Cognitive State:")
    print(f"      - Working Memory Active Goals: {state['working_memory']['active_goals']}")
    print(f"      - Long-term Memories: {state['long_term_memory']['episodic_memories']}")
    print(f"      - Attention Focus: {state['attention']['focus_level']}")
    
    print("\n✅ HUMAN-LIKE COGNITIVE ARCHITECTURE WORKING!\n")
