"""
OPTIMIZATION PATTERNS
Defines reusable optimization strategies for code improvement
"""

class OptimizationPatterns:
    """Encapsulates all known optimization patterns"""
    
    @staticmethod
    def get_all_patterns() -> dict:
        """Return all optimization patterns the AI knows"""
        return {
            "nested_loops": {
                "name": "Flatten Nested Loops",
                "description": "Convert nested loops to dictionary lookups",
                "complexity_reduction": "O(n²) → O(n)",
            },
            "query_in_loop": {
                "name": "Batch Database Queries",
                "description": "Replace multiple queries with single batched query",
                "complexity_reduction": "N queries → 1 query",
            },
            "string_concat_in_loop": {
                "name": "List Join Optimization",
                "description": "Use list + join instead of string concatenation",
                "complexity_reduction": "O(n²) → O(n)",
            },
            "list_to_generator": {
                "name": "Convert List to Generator",
                "description": "Use generators for memory efficiency",
                "complexity_reduction": "Immediate → Lazy evaluation",
            },
            "cache_repeated_calls": {
                "name": "Add Function Caching",
                "description": "Cache expensive function results",
                "complexity_reduction": "Repeated computation → O(1) lookup",
            }
        }
