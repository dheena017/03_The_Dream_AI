"""
CONFIDENCE CALCULATOR
Calculates confidence scores and risk assessments for optimizations
"""

from typing import Dict, List

class ConfidenceCalculator:
    """Handles confidence and risk calculations for optimizations"""
    
    @staticmethod
    def calculate_confidence(inefficiency: Dict, context: Dict) -> float:
        """
        Determine how confident we are in applying this optimization.
        Returns float between 0.0 and 1.0
        """
        confidence = 0.5  # Start neutral
        
        # Increase confidence based on inefficiency severity
        if inefficiency.get("severity") == "high":
            confidence += 0.3
        elif inefficiency.get("severity") == "medium":
            confidence += 0.15
        
        # Increase confidence if we have good context
        if context.get("function_length", 0) > 50:
            confidence += 0.15
        
        # Adjust based on optimization type
        pattern_type = inefficiency.get("type")
        if pattern_type == "nested_loops":
            confidence += 0.2
        elif pattern_type == "string_concat_in_loop":
            confidence += 0.25
        
        return min(1.0, confidence)
    
    @staticmethod
    def assess_risks(optimization_type: str) -> List[str]:
        """
        List potential risks for a given optimization type
        """
        risks_map = {
            "nested_loops": [
                "May change iteration order",
                "Could break if dictionary key doesn't exist",
                "Test with edge cases"
            ],
            "query_in_loop": [
                "Batch query might not match original semantics",
                "Need to verify output data matches",
                "Potential transaction issues"
            ],
            "string_concat_in_loop": [
                "Slight API change required",
                "Edge case: empty lists",
                "Unicode handling may differ"
            ],
            "list_to_generator": [
                "Can only iterate once",
                "Can't access by index",
                "May change memory profile"
            ],
            "cache_repeated_calls": [
                "Cache invalidation needed",
                "Thread-safety concerns",
                "Memory overhead from cache"
            ]
        }
        
        return risks_map.get(optimization_type, ["Unknown optimization type"])
